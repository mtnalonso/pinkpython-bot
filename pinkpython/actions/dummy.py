from actions.action import Action


class Dummy(Action):
    def __init__(self):
        Action.__init__(self)
        self.responses = ['Alive and eating!']

    def execute(self, params=None):
        pass

