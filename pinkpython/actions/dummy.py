from actions.action import Action


class Dummy(Action):
    def __init__(self):
        pass

    def execute(self, params={}):
        pass

    def get_response_message(self):
        return 'Alive and eating!'
