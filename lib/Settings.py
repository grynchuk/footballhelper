import os

class Settings():

    DEV     = 'dev'
    PROD    = 'prod'
    __state = ''

    def __init__(self):
        self.__state = os.environ['DEV_STATE'] if 'DEV_STATE' in os.environ else self.PROD

        if self.__state == self.DEV:
            self.init_dev()

        self.__check_envs()

    def get_token(self):
        return os.environ['VIBER_TOKEN']

    def get_port(self):
        return os.environ['PORT']

    def get_url(self):
        return os.environ['BOT_URL']

    def init_dev(self):
        os.environ['BOT_URL']  = 'https://a404b794.ngrok.io/bot'
        os.environ['PORT']     = '8080'

    def __check_envs(self):
        to_check = ['BOT_URL', 'PORT', 'VIBER_TOKEN']
        for var in to_check:
            if var not in os.environ:
                raise Exception(' Env var {} have to bee set '.format(var))