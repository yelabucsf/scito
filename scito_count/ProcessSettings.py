import configparser
import re
from warnings import warn

class ProcessSettings(object):
    def __init__(self, config_file: str, config_section: str):
        config = configparser.ConfigParser()
        config.read(config_file)
        self._section_settings = config[config_section]

class S3Settings(ProcessSettings):
    def __init__(self, config_section: str, config_file: str):
        super().__init__(config_section, config_file)
        relevant_attr = ['bucket', 'key', 'profile']
        self.bucket, self.key, self.profile = [self._section_settings[x] for x in relevant_attr]


class ReadSettings(ProcessSettings):
    def __init__(self, config_section: str, config_file: str):
        super().__init__(config_section, config_file)
        relevant_attr = ['technology', 'read start', 'read end']
        self.technology, self.start, self.end = [self._section_settings[x] for x in relevant_attr]

