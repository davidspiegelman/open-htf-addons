"""
Base class for all ezhtf plugs

Inherits from openhtf.plugs.BasePlug
"""
from openhtf.plugs import BasePlug
from openhtf.util import conf


class EZBasePlug(BasePlug):
    @classmethod
    def get_subclass_name(cls):
        return cls.__name__

    @classmethod
    def get_plug_config(cls):
        if 'plugs' in conf:
            if cls.__name__ in conf.plugs:
                return conf.plugs[cls.__name__]
        return dict()

    @property
    def name(self):
        if 'name' in self._settings:
            return self._settings['name']
        else:
            return self.get_subclass_name()
