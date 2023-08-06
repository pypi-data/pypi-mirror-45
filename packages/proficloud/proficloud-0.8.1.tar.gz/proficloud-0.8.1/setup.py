from setuptools import setup, find_packages

setup(name='proficloud',
    version='0.8.1',
    description='Easy access for PROFICLOUD',
    url='http://www.proficloud.net',
    author='Proficloud',
    author_email='proficloud@proficloud.net',
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'numpy', 'streamz', 'ntplib', 'somoclu', 'sklearn', 'bokeh', 'matplotlib', 'paho-mqtt'],
    zip_safe=False)
