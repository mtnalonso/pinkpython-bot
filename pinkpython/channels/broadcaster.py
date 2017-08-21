

class Broadcaster:
    def __init__(self):
        self.channels = {}

    def send_message(self, message):
        # TODO: select channel type according to message and send it
        print(message)

    def add_channel(self, channel_name, channel_instance):
        self.channels[channel_name] = channel_instance
