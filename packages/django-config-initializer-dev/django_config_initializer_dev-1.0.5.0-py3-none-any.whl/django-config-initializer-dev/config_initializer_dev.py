import os

from swiss_common_utils.utils.log.log_utils import get_logger
from swiss_common_utils.utils.yml.yaml_utils import yaml_to_flat_dict


def load_config():
    profile = os.environ.get('SWISS_PROFILE', 'dev')

    logger = get_logger()
    logger.info('Initializing environment variables for profile: {}'.format(profile))

    config_file_name = '.'.join(['-'.join(['config', profile]), 'yml'])
    config_path = os.path.join('config', config_file_name)
    if not os.path.isfile(config_path):
        logger.error('Cannot find config file: {}'.format(config_path))
        return

    var_dict = yaml_to_flat_dict(src_file=config_path)
    for k, v in var_dict.items():
        key = '_'.join(['CONFIG_SERVICE', k.upper()])
        logger.debug('setting environment variable: {}={}'.format(key, v))
        os.environ[key] = str(v)

