from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

cv_model = json.load(open('cv.json'))
sms_history = json.load(open('sms_history.json'))


def get_message(from_, message):
    msg = message.strip().lower()
    cv = cv_model.cv['data']

    if from_ not in sms_history:
        sms_history.append(from_)
        return cv['introduction']

    elif msg == 'experience':
        return cv['experience']['index']
    elif msg == 'references':
        return cv['references']

    elif msg in cv['experience']:
        return cv['experience'][msg]

    else:
        return ['Thanks for your message!']


@app.route('/cvilio', methods=['POST'])
def sms_reply():
    from_ = request.values.get('From')
    message = request.values.get('Body')

    outbound_messages = get_message(from_, message)
    resp = MessagingResponse()
    resp.message('\n'.join(outbound_messages))

    outfile = open('sms_history.json', 'w')
    outfile.write(json.dumps(sms_history))

    return str(resp)


if __name__ == '__main__':
    app.run()
