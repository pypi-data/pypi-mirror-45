from protean.conf import active_config

from . import config

__version__ = '0.0.11'


# Update the config here so that loading the repo will load the config
active_config.update_defaults(config)
