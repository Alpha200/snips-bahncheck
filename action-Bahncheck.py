#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from traincheck import TrainCheck
import io


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {
            section: {option_name: option for option_name, option in self.items(section)} for section in self.sections()
        }


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()


def intent_callback(hermes, intent_message):
    result_sentence = traincheck.check_train()
    hermes.publish_end_session(intent_message.session_id, result_sentence)


if __name__ == "__main__":
    conf = read_configuration_file(CONFIG_INI)
    traincheck = TrainCheck(conf['secret']['station_from'], conf['secret']['station_via'])
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("Alpha200:checkTrainStatus", intent_callback)
        h.start()
