#!/usr/bin/python3

import WXBizMsgCrypt
from flask import Flask
from flask import request
import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    sToken = config.TOKEN
    sEncodingAESKey = config.ENCODINGAESKEY
    sCorpID = config.CORPID
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    wxcpt = WXBizMsgCrypt.WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    return sEchoStr


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVERPORT, debug=True)
