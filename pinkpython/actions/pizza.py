from actions.action import Action


responses = [
        'PIZZAAAAA!!!',
]


class Pizza(Action):
    def __init__(self, responses=responses):
        self.responses=responses

    def execute(self, params=None):
        pass

    def get_response_message(self):
        return self.responses[0]
