#!/usr/bin/env python3

import xml.etree.cElementTree as ET
from flask import Flask
from flask import request
import WXBizMsgCrypt
import config

app = Flask(__name__)


def parse_message(message):
    xml_tree = ET.fromstring(message)
    items = map(lambda x: x.tag, xml_tree.getchildren())
    parsed = {}
    for item in items:
        parsed[item] = xml_tree.find(item).text
    return parsed


@app.route('/', methods=['GET', 'POST'])
def main():
    sToken = config.TOKEN
    sEncodingAESKey = config.ENCODINGAESKEY
    sCorpID = config.CORPID
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    reqData = request.data # POST data payload

    # 对消息体解密
    wxcpt = WXBizMsgCrypt.WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
    ret, sMsg = wxcpt.DecryptMsg(reqData, msg_signature, timestamp, nonce)
    parsed = parse_message(sMsg)

    # Anything needs to do...



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVERPORT, debug=True)
