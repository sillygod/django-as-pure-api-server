import ast
import os
import configparser
from .base import *


try:
    local_vars = locals()
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    env_path = os.path.join(local_vars['BASE_DIR'], 'core', 'settings', 'env.ini')
    config.read(env_path)
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
    print('syntax error in ini file')
except:
    print('unknown error, maybe you forgot to put env.ini in the settings directory')
    pass
