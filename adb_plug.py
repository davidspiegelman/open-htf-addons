"""
Proof of Concept AdbPlug for OpenHTF

Limitations:
1) Only a single ADB method is implemented so far (more methods coming soon)

Requires adb_shell - https://github.com/JeffLIrion/adb_shell

pip import 'adb_shell[usb]'

"""

from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import os
from plugs.ez_base_plug import EZBasePlug
import psutil
import time


class AdbPlug(EZBasePlug):
    '''
    Communicate with DUT using adb protocol via USB
    '''

    def __init__(self):
        super().__init__()
        subclass_name = self.get_subclass_name()
        plug_config = self.get_plug_config()

        # set defaults here
        defaults = {'name': subclass_name,
                    'rsa_key_path': None,
                    'serial': None}

        # override defaults with plug config from station_config.yaml
        self._settings = dict(defaults, **plug_config)
        self.connected = False
        self.priv = None
        self.signer = None

        # check if adb server is running. If it is, terminate it.
        for proc in psutil.process_iter():
            if proc.name() == 'adb':
                proc.terminate()
                time.sleep(1)
                break

        if self._settings['rsa_key_path'] == 'default':
            self._settings['rsa_key_path'] = os.path.expanduser('~/.android/adbkey')

        if self._settings['rsa_key_path']:
            with open(self._settings['rsa_key_path']) as f:
                self.priv = f.read()
            self.signer = [PythonRSASigner('', self.priv)]

        self.device = AdbDeviceUsb(self._settings['serial'])

        self._connect()
        assert self.connected, "Unable to connect to Adb Usb device"

    def _connect(self):
        self.connected = self.device.connect(rsa_keys=self.signer, auth_timeout_s=0.1)

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
