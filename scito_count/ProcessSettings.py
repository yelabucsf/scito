from typing import Union
from io import StringIO
import configparser

class ProcessSettings(object):
    def __init__(self, config_file: Union[str, StringIO], config_section: str):
        config = configparser.ConfigParser()
        config_type = type(config_file).__name__
        if config_type == 'StringIO':
            config.read_file(config_file)
        elif config_type == 'str':
            config.read(config_file)
        else:
            raise ValueError(f'init_config(): {config_type} is not a supported input type')
        self._section_settings = config[config_section]

class S3Settings(ProcessSettings):
    def __init__(self, config_file: Union[str, StringIO], config_section: str):
        super().__init__(config_file, config_section)
        relevant_attr = ['bucket', 'key', 'profile']
        self.bucket, self.object_key, self.profile = [self._section_settings[x] for x in relevant_attr]


class ReadSettings(ProcessSettings):
    def __init__(self, config_file: Union[str, StringIO], config_section: str):
        super().__init__(config_file, config_section)
        relevant_attr = ['technology', 'read start', 'read end']
        self.technology, self.start, self.end = [self._section_settings[x] for x in relevant_attr]


class S3SettingsWhitelist(S3Settings):
    def __init__(self, config_file: Union[str, StringIO], config_section: str):
        super().__init__(config_file, config_section)
        wl_attributes = ['cell barcodes', 'batch barcodes']
        self.cbc, self.bbc = [self._section_settings[x] for x in wl_attributes]

