import paho.mqtt.client as mqtt


class MindConnectIot:

    def __init__(self, device_id: str, region: str, tenant_name: str, mcio_extension_username: str, password: str,
                 domain: str = 'mindsphere.io') -> None:
        self.mqtt_client = mqtt.Client(client_id=device_id)

        username = '%s/%s' % (tenant_name, mcio_extension_username)
        self.mqtt_client.username_pw_set(username=username, password=password)

        host = 'mciotextension.%s-central.%s' % (region, domain)
        self.mqtt_client.connect(host=host)


    ### MEASUREMENTS
    def sendMeasurement(self, fragment, series, value, unit, time=None):
        arguments = [fragment, series, value, unit]

        if time is not None:
            arguments.append(time)

        self.sendCommand(200, arguments)

    ### ALARMS
    def sendCriticalAlarm(self, alarm_type: str, text: str = None, time=None):
        self._sendPredefinedAlarm(301, alarm_type, text, time)

    def sendMajorAlarm(self, alarm_type: str, text: str = None, time=None):
        self._sendPredefinedAlarm(302, alarm_type, text, time)

    def sendMinorAlarm(self, alarm_type: str, text: str = None, time=None):
        self._sendPredefinedAlarm(303, alarm_type, text, time)

    def sendWarningAlarm(self, alarm_type: str, text: str = None, time=None):
        self._sendPredefinedAlarm(304, alarm_type, text, time)

    def _sendPredefinedAlarm(self, code: int, alarm_type: str, text: str = None, time=None):
        arguments = [alarm_type]

        if text is not None:
            arguments.append(text)

        if time is not None:
            arguments.append(time)

        self.sendCommand(code, arguments)

    def sendAlarm(self, alarm_type: str, severety: str):
        self.sendCommand(305, [alarm_type, severety])

    def clearAlarmType(self, alarm_type: str):
        self.sendCommand(306, [alarm_type])

    ### EVENTS
    def updateLocation(self, latitude, longitude, altitude, accuracy, time=None, inventoryUpdate: bool = False):
        arguments = [latitude, longitude, altitude, accuracy]

        if time is not None:
            arguments.append(time)

        self.sendCommand(402 if inventoryUpdate else 401, arguments)

    ### Generic
    def sendCommand(self, command_id: int, arguments: list):
        self.mqtt_client.publish('s/us', ",".join(map(str, [command_id] + arguments)))
