A small client to connect with MindConnect IoT using the MindConnect IoT Extension

## How to use
First initialise a new `MindConnectIot` object for your device:
```python
from mindconnectiot import MindConnectIot

mindconnect = MindConnectIot(device_name, mindconnect_region, tenant_name, 
        mcio_extension_username, password)
```

Afterwards you can send data to the cloud, e.g. to send a measurement:
```python
mindconnect.sendMeasurement('Temperature', 'Celsius', 23.4, '*C')
```