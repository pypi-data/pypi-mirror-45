# -*- coding: utf-8 -*-
"""Read JACK presets and their settings from QjackCtl's configuration file."""

import configparser
import logging


log = logging.getLogger(__name__)
PARAM_MAPPING = {
    'driver': ('engine', 'driver'),
    'realtime': ('engine', 'realtime'),
    'priority': ('engine', 'realtime-priority'),
    'verbose': ('engine', 'verbose'),
    'timeout': ('engine', 'client-timeout'),
    'portmax': ('engine', 'port-max'),
    'samplerate': 'rate',
    'frames': 'period',
    'periods': 'nperiods',
    'interface': 'device',
    'indevice': 'capture',
    'outdevice': 'playback',
    'chan': 'channels',
    'inlatency': 'input-latency',
    'outlatency': 'output-latency',
    'mididriver': 'midi',
    # 'snoop': '???'
}


def get_qjackctl_presets(qjackctl_conf):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(qjackctl_conf)

    presets = []
    if 'Presets' in config:
        presets = [v for k, v in sorted(config['Presets'].items())
                   if k != 'DefPreset']

    try:
        default_preset = config.get('Presets', 'DefPreset')
    except configparser.Error:
        default_preset = presets[0] if presets else '(default)'

    settings = {}
    if 'Settings' in config:
        if not presets:
            presets = [default_preset]

        for name in config['Settings']:
            try:
                preset, setting = name.split('\\', 1)
            except ValueError:
                # only the default preset was saved
                setting = name
                preset = default_preset

            setting = setting.lower()
            value = config.get('Settings', name)

            if preset in presets:
                setting = PARAM_MAPPING.get(setting, setting)
                if isinstance(setting, tuple):
                    component, setting = setting
                else:
                    component = 'driver'

                if preset not in settings:
                    settings[preset] = {}

                if component not in settings[preset]:
                    settings[preset][component] = {}

                if value == 'false':
                    value = False
                elif value == 'true':
                    value = True
                elif value == '':
                    value = None
                else:
                    try:
                        value = int(value)
                    except (TypeError, ValueError):
                        pass

                settings[preset][component][setting] = value
            else:
                log.warning("Unknown preset: %s" % preset)

    return presets, settings, default_preset


def _test():
    from xdg import BaseDirectory as xdgbase

    qjackctl_conf = xdgbase.load_first_config('rncbc.org/QjackCtl.conf')

    if qjackctl_conf:
        presets, _, default_preset = get_qjackctl_presets(qjackctl_conf)
        for preset in presets:
            print(preset, "*" if preset == default_preset else '')


if __name__ == '__main__':
    _test()
