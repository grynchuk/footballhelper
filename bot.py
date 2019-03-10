import os
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
import logging
from lib.Settings import Settings


from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

settings = Settings()

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='FootballHelperBot',
    avatar='http://site.com/avatar.jpg',
    auth_token=settings.get_token()
))


@app.route('/sethook')
def sethook():
    mess = 'hook is set'
    try:
        viber.set_webhook(settings.get_url())
    except:
        mess = 'error'

    return mess


@app.route('/bot', methods=['POST'])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data().decode('utf-8'))

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


app.run(host='0.0.0.0', port=settings.get_port(), debug=True)

