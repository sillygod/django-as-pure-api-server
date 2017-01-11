import ast
import os
import configparser
import logging
from .base import *


class NoDjangoSettingsException(Exception):
    pass


logger = logging.getLogger('django')


try:
    local_vars = locals()
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    # for case-sensitive
    env_path = os.path.join(local_vars['BASE_DIR'], 'core', 'settings', 'env.ini')
    config.read(env_path)

    if 'django settings' not in config:
        raise NoDjangoSettingsException

    for key, value in config['django settings'].items():
        if key == 'INSTALLED_APPS':
            local_vars[key] = local_vars[key] + ast.literal_eval(value)
        elif key == 'INSTALLED_APPS_RW':  # RW means overwrite
            local_vars[key] = ast.literal_eval(value)
        elif key == 'MIDDLEWARE_CLASSES':
            local_vars[key] = local_vars[key] + ast.literal_eval(value)
        else:
            local_vars[key] = ast.literal_eval(value)
except configparser.ParsingError:
    logger.error('syntax error in ini file')
except NoDjangoSettingsException as e:
    logger.warn('you forgot to put env.ini or no section -django settings- in the file')
except Exception as e:
    logger.exception(str(e))
