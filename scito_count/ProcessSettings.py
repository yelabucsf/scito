import configparser
from typing import Dict

def process_settings(config_file: str, config_section: str, settings_scope: str) -> Dict:

    scopes = {
        's3_settings': ['bucket', 'key', 'profile'],
        'read_settings': ['technology', 'read start', 'read end'],
        'whitelist_settings': ['cell barcodes', 'batch barcodes']
    }

    if settings_scope not in scopes:
        raise ValueError(f'processSettings(): {settings_scope} is not a supported type of configuration')

    config_init = configparser.ConfigParser()
    config_init.read(config_file)
    config = config_init[config_section]
    scope = scopes[settings_scope]
    return {x: config[x] for x in scope}


