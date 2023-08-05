
import os
from .application import runner
from .application import logger
from .application import configurator
from . import identity


class Main(runner.Runner):
    def main(self):
        print('Starting {}...'.format(identity.NAME))
        print('Provided by {}'.format(identity.PROVIDER))
        log = logger.setup(identity.ROOT)
        config_file = os.getenv('{}_CONFIG_FILE'.format(
                identity.NAME.upper()), 'config.json')
        log.info('Using "{}" configuration file'.format(config_file))
        try:
            configurator.Configurator(identity.NAME, 'config.json').load()
        except FileNotFoundError as e:
            log.warn('Failed to load configuration "{}" ({})'.format(
                    e.filename, e.strerror))
