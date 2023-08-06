import os

from swiss_common_utils.yml.yaml_utils import yaml_to_flat_dict
from swiss_logger.log_utils import get_logger


def load_config():
    profile = os.environ.get('CONFIG_SERVICE_SWISS_CLOUD_PLATFORM_METADATA_ENVIRONMENT', 'dev')

    logger = get_logger('config_initializer_dev_logger')
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

