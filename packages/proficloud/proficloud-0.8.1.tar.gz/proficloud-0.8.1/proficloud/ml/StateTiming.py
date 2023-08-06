import pandas as pd
import numpy as np
from enum import Enum

class State:
    state_id = ""
    transitions = {}
    signal_thresholds = {}

    def __init__(self, state_id, transitions, signal_thresholds):
        self.state_id = state_id
        self.transitions = transitions
        self.signal_thresholds = signal_thresholds
    
    def __repr__(self):
        return str(self.__dict__)

class Transition:
    source_state = ""
    target_state = ""
    min_time = float("inf")
    max_time = 0
    def __init__(self, source_state, target_state, min_time=float("inf"), max_time=0):
        self.source_state = source_state
        self.target_state = target_state
        self.min_time = min_time
        self.max_time = max_time
    
    def __repr__(self):
        return str(self.__dict__)

class SignalThreshold:
    signal_name = ""
    min_value = float("inf")
    max_value = 0

    def __init__(self, signal_name, min_value=float("inf"), max_value=0):
        self.signal_name = signal_name
        self.min_value = min_value
        self.max_value = max_value
    
    def __repr__(self):
        return str(self.__dict__)

class AnomalyTypeEnum(Enum):
    NOT_TESTED = -1
    NO_ANOMALY = 0
    TIME_ANOMALY = 1
    STATE_ANOMALY = 2
    UNKNOWN_STATE = 3
    VALUE_ERROR = 4

class ValueErrorAnomaly():
    signal_name = ""
    signal_value = 0
    signal_min_value = 0
    signal_max_value = 0

    def __init__(self, signal_name, signal_value, signal_min_value, signal_max_value):
        self.signal_name = signal_name
        self.signal_min_value = signal_min_value
        self.signal_max_value = signal_max_value
        self.signal_value = signal_value

    def __repr__(self):
        return str(self.__dict__)

class StateTimingModelAnomaly():

    def __init__(self):
        self.timestamp = 0
        self.anomaly = False
        self.anomalytype =  AnomalyTypeEnum.NOT_TESTED
        self.source_state = None
        self.target_state = None
        self.relative_time = None
        self.transition = None
        self.value_error = []

    def __repr__(self):
        return str(self.__dict__)

class StateTimingModel():
    
    signal_names = None
    state_signal_name = ""
    timestamp_signal_name = ""
    states = {}
    accepting_states = {}
    maxValueOffsetFactor = 1.0
    minValueOffsetFactor = 1.0
    maxTimeOffset = 1.0
    minTimeOffset = 1.0
    initial_state = None

    debug = False

    current_state = -1
    current_time = -1
    start_time = -1

    def train(self, data, state_signal_name, timestamp_signal_name, filter_zero_variance=False, initial_state=None, accepting_states={}, minValueOffsetFactor=1.0, maxValueOffsetFactor=1.0, minTimeOffset=0, maxTimeOffset=0):
        
        data = data.dropna()
        
        if filter_zero_variance:
            variance = data.var(axis=0)
            zero_variance = variance == 0.0
            zero_variance = np.insert(zero_variance.values, 0, False)
            if sum(zero_variance) > 0:
                data = data.loc[:,~zero_variance]
        
        self.signal_names = data.columns.values.tolist()
        self.signal_names.remove(timestamp_signal_name)
        self.state_signal_name = state_signal_name
        self.timestamp_signal_name = timestamp_signal_name
        self.accepting_states = accepting_states
        self.minValueOffsetFactor = minValueOffsetFactor
        self.maxValueOffsetFactor = maxValueOffsetFactor
        self.minTimeOffset = minTimeOffset
        self.maxTimeOffset = maxTimeOffset
        self.initial_state = initial_state

        #state_keys = data.groupby([state_signal_name]).groups.keys()

        self.states = {}
        current_time = -1
        start_time = -1
        current_state = None

        for index, row in data.iterrows():
            timestamp = row[timestamp_signal_name]
            state = row[state_signal_name]

            if start_time < 0:
                #Initial setup
                start_time = timestamp
                current_state = state
                if self.initial_state is None:
                    self.initial_state = state

                self.states[str(current_state)] = State(current_state, {}, {})

            current_time = timestamp - start_time

            if state != current_state:
                #Transition happened
                if state not in self.states[str(current_state)].transitions:
                    self.states[str(current_state)].transitions[str(state)] = Transition(current_state, state)
                
                if self.states[str(current_state)].transitions[str(state)].min_time > current_time:
                    self.states[str(current_state)].transitions[str(state)].min_time = current_time
                
                if self.states[str(current_state)].transitions[str(state)].max_time < current_time:
                    self.states[str(current_state)].transitions[str(state)].max_time = current_time                    

                start_time = timestamp

            current_state = state

            if str(current_state) not in self.states:
                #Entered new state for the first time
                self.states[str(current_state)] = State(current_state, {}, {})

            #Update boundary values:
            for signal in self.signal_names:
                if signal == self.state_signal_name or signal == self.timestamp_signal_name:
                    continue
                
                if signal not in self.states[str(current_state)].signal_thresholds:    
                    self.states[str(current_state)].signal_thresholds[signal] = SignalThreshold(signal)
                
                val = row[signal]
                if val < self.states[str(current_state)].signal_thresholds[signal].min_value:
                    self.states[str(current_state)].signal_thresholds[signal].min_value = val
            
                if val > self.states[str(current_state)].signal_thresholds[signal].max_value:
                    self.states[str(current_state)].signal_thresholds[signal].max_value = val
        

    def resetPrediction(self):
        self.current_state = -1
        self.current_time = -1
        self.start_time = -1

    def predict(self, row, raw=False):

        result = StateTimingModelAnomaly()

        timestamp = row[self.timestamp_signal_name]
        state = row[self.state_signal_name]

        result.timestamp = timestamp

        if self.start_time < 0:
            #Initial setup
            self.start_time = timestamp
            if str(state) in self.states:
                self.current_state = state
            else:
                if str(self.initial_state) in self.states: 
                    self.current_state = self.initial_state
                    self.state = self.current_state
                else:
                    self.current_state = list(self.states)[0]
                    self.state = self.current_state

        self.current_time = timestamp - self.start_time

        if state != self.current_state:
            #Transition happened             
            if str(state) not in self.states[str(self.current_state)].transitions:
                if self.debug: print("STATE ANOMALY!")
                result.anomaly = True
                result.anomalytype = AnomalyTypeEnum.STATE_ANOMALY
                result.source_state = self.current_state
                result.target_state = state
                result.relative_time = self.current_time
            else:
                if ((self.states[str(self.current_state)].transitions[str(state)].min_time + self.minTimeOffset) > self.current_time
                or (self.states[str(self.current_state)].transitions[str(state)].max_time + self.maxTimeOffset) < self.current_time):
                    
                    if str(self.current_state) not in self.accepting_states:
                        if self.debug: print("TIME ANOMALY")
                        result.anomaly = True
                        result.anomalytype = AnomalyTypeEnum.TIME_ANOMALY

                result.source_state = self.current_state
                result.target_state = state
                result.relative_time = self.current_time
                result.transition = self.states[str(self.current_state)].transitions[str(state)]                    

            self.start_time = timestamp
            self.current_state = state

            if not result.anomaly:
                if str(self.current_state) not in self.states:
                    if self.debug: print("WAITING IN UNKNOWN STATE")
                    result.anomaly = True
                    result.anomalytype = AnomalyTypeEnum.UNKNOWN_STATE
                    result.source_state = self.current_state
                    result.target_state = self.current_state
                    result.relative_time = self.current_time

            #Check boundary values if there is no other anomaly detected:
            if not result.anomaly:
                for signal in self.signal_names:
                    if signal == self.state_signal_name or signal == self.timestamp_signal_name:
                        continue
                                
                    val = row[signal]
                    if (val < (self.states[str(self.current_state)].signal_thresholds[signal].min_value * self.minValueOffsetFactor)
                    or val > (self.states[str(self.current_state)].signal_thresholds[signal].max_value * self.maxValueOffsetFactor)):
                        if self.debug: print("VALUE ERROR")
                        result.anomaly = True
                        result.anomalytype = AnomalyTypeEnum.VALUE_ERROR
                        result.source_state = self.current_state
                        result.target_state = self.current_state
                        result.relative_time = self.current_time

                        result.value_error.append(
                            ValueErrorAnomaly(signal,
                                val, 
                                self.states[str(self.current_state)].signal_thresholds[signal].min_value, 
                                self.states[str(self.current_state)].signal_thresholds[signal].max_value
                                )
                            )
        else:
            result.source_state = self.current_state
            result.target_state = self.current_state
            result.relative_time = self.current_time


        if not result.anomaly:
            result.anomalytype = AnomalyTypeEnum.NO_ANOMALY

        return result
        
    def summary(self):
        return "Simple State timing and value threshold learning and anomaly detection"
    