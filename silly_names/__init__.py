""" Silly Names """

from eventmanager import Evt
from filtermanager import Flt
from RHUI import UIField, UIFieldType
import random

class SillyNames():
    def __init__(self, rhapi):
        self._rhapi = rhapi

    def startup(self, _args):
        self._rhapi.filters.add(Flt.EMIT_PHONETIC_DATA, 'silly-name-filter', self.replace_silly_name)

    def replace_silly_name(self, data):
        silly_name_frequency = self._rhapi.db.option('silly_name_frequency', as_int=True)
        if silly_name_frequency and random.randrange(0, 99, 1) < silly_name_frequency:
            silly_name = self._rhapi.db.pilot_attribute_value(data['pilot_id'], 'silly_name', default_value=None)
            if silly_name:
                data['callsign'] = silly_name
        return data


def initialize(rhapi):
    sillyplugin = SillyNames(rhapi)
    rhapi.fields.register_pilot_attribute(UIField(
        'silly_name',
        'Silly Name (Phonetic)',
        UIFieldType.TEXT
    ))
    rhapi.ui.register_panel('silly_name_panel', 'Silly Names', 'settings')
    rhapi.fields.register_option(UIField(
        'silly_name_frequency',
        'Usage Frequency (percent)',
        UIFieldType.BASIC_INT,
        5,
        '0–100'
    ), 'silly_name_panel')
    rhapi.events.on(Evt.STARTUP, sillyplugin.startup)

