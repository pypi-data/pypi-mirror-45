import pandas as pd
import numpy as np
import somoclu
from sklearn.preprocessing import MinMaxScaler

class SomReconstructionError():
    scaler = None
    som = None
    threshold = None
    signal_names = None
    
    def train(self, data, sideLength=30, epochs=25, learningRate=0.1):
        
        data = data.dropna()
        #print(data)
        variance = data.var(axis=0)
        zero_variance = variance == 0.0
        zero_variance = np.insert(zero_variance.values, 0, False)
        if sum(zero_variance) > 0:
            data = data.loc[:,~zero_variance]
        
        self.scaler = MinMaxScaler(feature_range=[0,1], copy=True)
        self.scaler.fit(data.values)
        
        self.signal_names = data.columns.values.tolist()
        
        transformed_data = self.scaler.transform(data)
        data = pd.DataFrame(transformed_data, columns=self.signal_names)
        
        self.som = somoclu.Somoclu(sideLength, sideLength, compactsupport=False, initialization="pca")
        self.som.train(data.values, scale0=learningRate, epochs=epochs)
        
        self.threshold = self.som.get_surface_state().min(axis=1).max()
        del self.som.activation_map
        
        
    def predict(self, sample, raw=False):
        scaled = self.scaler.transform(sample.reshape(1,-1))
        prediction = self.som.get_surface_state(scaled).min(axis=1)
        
        if not raw:
            anomaly = prediction - self.threshold
            if anomaly < 0:
                anomaly = 0
            else:
                anomaly = anomaly[0]
            return anomaly
        else:
            return prediction
        
    def summary(self):
        return "Non-Linear, Multivariate Time Series Anomaly Detection\n"
        +"Based on Self-Organizing Map neural network."
        +"Side length: "+str(self.som._n_columns)+"x"+str(self.som._n_rows)
        +"Detection threshold: "+str(self.threshold)
        +"Signals: "+str(list(self.signal_names))
    