#!/usr/bin/env python3

import json
import requests
import redis
import config


class SendMessage(object):

    def __init__(self, agentid, corpsecret, corpid):
        self.agentid = agentid
        self.corpsecret = corpsecret
        self.corpid = corpid
        self.r = redis.Redis()
        self.token_name = 'access_token'
        self.token = self.get_token()

    def get_token(self):
        token = self.r.get(self.token_name)
        if not token:
            return self.get_new_token()
        return token

    def get_new_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        response = requests.get(url, params=params).text
        j = json.loads(response)
        if not j['errcode']:
            new_token = j['access_token']
            token_expire = j['expires_in']
            self.r.set(self.token_name, new_token, ex=token_expire)
            return new_token

    def send_message(self, to, content):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        params = {
            'access_token': self.token        
        }
        if len(content) > config.MESSAGELENGTH:
            message_count = len(content) / config.MESSAGELENGTH + 1
            message_number = 1
            while len(content) > 0:
                cut = content[:config.MESSAGELENGTH]
                msg_data = json.dumps({
                    'touser': to,
                    'msgtype': 'text',
                    'agentid': self.agentid,
                    'text': {
                        'content': 'msg({number}/{count})\n'.format(number=message_number, count=message_count) + cut
                    }
                })
                requests.post(url, data=msg_data)
                content = content[config.MESSAGELENGTH:]
                message_number += 1
        else:
            msg_data = json.dumps({
                'touser': to,
                'msgtype': 'text',
                'agentid': self.agentid,
                'text': {
                    'content': content
                }
            })
            requests.post(url, params=params, data=msg_data)


if __name__ == '__main__':
    pass

