import os

from twisted.internet import reactor

from src import JsonConfigurationDecoder, ConfigurationLoader
from src.election_component.tuda_election_component import TudaElectionComponent
from src.logger import Logger


def setup_election_component():
    election_component = TudaElectionComponent()
    election_component.start_election()


def start_network_listeners(environment_function=None):
    """Start the reactor and let the remaining functions run on another thread"""

    Logger().info('Setup done, starting network listeners', location='SETUP')
    if environment_function is not None:
        reactor.callFromThread(environment_function)
    reactor.run()


def main():
    Logger().info('Setting up train environment', location='SETUP')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    ConfigurationLoader(JsonConfigurationDecoder()).load_config(dir_path + '/main_config.json')
    configuration_loader = JsonConfigurationDecoder()
    configuration_loader.decode_config('../configuration')

    Logger().info('Loaded train environment config', location='SETUP')

    # TODO: remove this, this is a mockup object and should not be present in the setup!
    from src import EventListener
    class MockUpOccupancyModel(EventListener):
        def __init__(self):
            from src import Broker
            super().__init__()
            self.set_message_type_callback('camera_handler', self.generate_occupancy)
            self.broker = Broker()
            self.broker.subscribe(self, "camera_handler")

        def generate_occupancy(self, _):
            from src import Event
            import random

            Logger().info("received @ occupancy_model", location=self.__class__.__name__)
            self.broker.publish(Event('occupancy', {str(i + 1): random.random() for i in range(280)}))

    # MockUpOccupancyModel()

    setup_election_component()

    Logger().info('Setup election components', location='SETUP')

    start_network_listeners()


if __name__ == '__main__':
    # TODO: get arguments here
    # The arguments should contain the streaming file
    main()
