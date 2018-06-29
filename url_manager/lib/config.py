"""
Lib application configuration file.
"""
import os
from configparser import ConfigParser


from .__init__ import APP_DIR


class AppConf(ConfigParser):
    """
    App configuration object.
    Make app configuration filenames absolute paths and relative to app
    config dir. Then configure the conf object with data.
    The local app conf file is optional and in values in it will overwrite
    those set in the main app conf file.
    """

    def __init__(self):
        """
        Initialise instance of AppConf class.
        Read config files in three locations, expecting the first versioned
        file to always be present and the two optional files to either override
        the default values or be ignored silently if they are missing.
        """
        super().__init__()

        etc_conf_names = ('app.conf', 'app.local.conf')
        conf_paths = [os.path.join(APP_DIR, 'etc', c) for c in etc_conf_names]

        user_config_path = os.path.join(
            os.path.expanduser('~'),
            '.config',
            'url_manager.conf'
        )
        conf_paths.append(user_config_path)

        self.read(conf_paths)
        self.set('DEFAULT', 'app_dir', APP_DIR)


def test():
    """
    Display the values read in across the three conf file locations.
    """
    conf = AppConf()

    for section in conf.sections():
        print(section)
        for option, value in conf.items(section):
            print(" {option:15}: {value}".format(option=option, value=value))


if __name__ == '__main__':
    test()
