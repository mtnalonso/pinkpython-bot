
class Message:
    def __init__(self, text, query ='', action='', parameters={},
                 language='en', platform=None, original=None):
        self.text = text
        self.query = query
        self.action = action
        self.parameters = parameters
        self.language = language
        self.generated_response = ''
        self.platform = platform
        self.original = original

    def __repr__(self):
        return ('action:\t' + str(self.action) + '\nquery:\t' +
                str(self.query) + '\nparams:\t' + str(self.parameters))

    def get_tweet_reply(self):
        try:
            reply_id, username = self.__get_tweet_params()
            tweet = self.__build_tweet(username)
        except Exception:
            raise NotImplementedError
        return reply_id, tweet

    def __get_tweet_params(self):
        reply_id = self.original.id
        username = self.original.user.screen_name
        return reply_id, username

    def __build_tweet(self, username):
        return ('@' + username + ' ' + self.generated_response)
