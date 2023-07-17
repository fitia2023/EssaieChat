import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EAALhMN4WnIoBAFis5GmagnKAZCKaU8yJezFU8ex8ZAyrOE3oSC9DQGUSozs4wAQtGDZA1izIGefXmU2Cl9jA9sLkAduv1g7Fc6TlpcRGLBxZCAsPIth25GCz0nlpnlju6oiuHN2nRxeJB8TVinGcDqZC3ZBbWqrQtgqKB4AD3M5rBjVISCUpeC"
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    # Webhook verify
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "merci":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "hello word its fitia", 200


@app.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messagin_event in entry['messaging']:
                sender_id = messagin_event['sender']['id']
                recipient_id = messagin_event['recipient']['id']

                if messagin_event.get('message'):
                    if 'text' in messagin_event['message']:
                        messagin_text = messagin_event['message']['text']
                    else:
                        messagin_text = 'no text'

                    response = messagin_text
                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)
