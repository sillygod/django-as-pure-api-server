import os
import logging


logger = logging.getLogger('django')

env = os.environ.get("env", "dev")

try:
    if env == "dev":
        from .dev import *
    else:
        from .prod import *
except Exception as e:
    logger.error(str(e))