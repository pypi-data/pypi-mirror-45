import importlib
import os

from src.broker import Broker, EventListener, Event
from src.configuration_store import ConfigurationStore, ConfigurationLoader, ConfigurationDecoder, \
    JsonConfigurationDecoder
from src.data_container import DataTypes, DataContainer, OccupancyData
from src.setup import main
from src.singleton import Singleton

name = "openspace-train-environment"

__all__ = ["Broker", "ConfigurationStore", "ConfigurationLoader", "ConfigurationDecoder", "JsonConfigurationDecoder",
           "EventListener", "Event", "DataTypes", "DataContainer", "OccupancyData", "Singleton"]

dir_path = os.path.dirname(os.path.realpath(__file__))

store = ConfigurationStore()
ConfigurationLoader(JsonConfigurationDecoder(), store).load_config(dir_path + '/main_config.json')


def init_as_main():
    import sys

    tree = os.listdir(dir_path + '/../plugin')

    sys.path.insert(0, '../plugin')
    for plugin in tree:
        if os.path.isdir(os.path.join(dir_path, '..', 'plugin', plugin)):
            importlib.import_module('plugin.{}'.format(plugin))

    main()


if __name__ == '__main__':
    init_as_main()
