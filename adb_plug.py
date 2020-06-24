"""
Proof of Concept AdbPlug for OpenHTF

Limitations:
1) Only a single ADB method is implemented so far (more methods coming soon)

Requires adb_shell - https://github.com/JeffLIrion/adb_shell

pip install 'adb_shell[usb]'

"""
import openhtf
from openhtf.util import conf
from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import os


class AdbPlug(openhtf.plugs.BasePlug):
    '''
    Communicate with DUT using ADB over USB
    '''

    @classmethod
    def get_subclass_name(cls):
        return cls.__name__

    def __init__(self, plug_config):
        super().__init__()
        subclass_name = self.get_subclass_name()

        # set defaults here
        defaults = {'name': subclass_name,
                    'rsa_key_path': os.path.expanduser('~/.android/adbkey'),
                    'serial': None}

        # override defaults with plug config from station_config.yaml
        self._settings = dict(defaults, **plug_config)
        self.connected = False
        with open(self._settings['rsa_key_path']) as f:
            self.priv = f.read()
        self.signer = PythonRSASigner('', self.priv)
        self.device = AdbDeviceUsb(self._settings['serial'])

        self._connect()
        assert self.connected, "Unable to connect to AdbUsb device"

    def _connect(self):
        self.connected = self.device.connect(rsa_keys=[self.signer], auth_timeout_s=0.1)

    def _close(self):
        self.device.close()
        self.connected = False

    def command(self, cmd):
        response = self.device.shell(cmd)
        return response

    Shell = command

    def tearDown(self):
        if self.connected:
            self._close()

class AdbPlug1(AdbPlug):
    def __init__(self):
        super().__init__(dict())
