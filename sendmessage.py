#!/usr/bin/env python3

import json
import os.path
import pickle
import time
import requests
import config


class SendMessage(object):

    def __init__(self, agentid, corpsecret, corpid):
        self.agentid = agentid
        self.corpsecret = corpsecret
        self.corpid = corpid
        if config.USEREDIS:
            import redis
            self.r = redis.Redis()
        else:
            self.token_file = 'token'
            self.init_token_file(self.token_file)
        self.token_name = 'access_token'
        self.token = self.get_token()

    def init_token_file(self, token_file):
        if not os.path.exists(token_file):
            with open(token_file, 'wb') as f:
                pickle.dump({}, f)
            return
        with open(token_file, 'r') as f:
            f_content = f.read()
        try:
            pickle.loads(f_content)
        except Exception as e:
            with open(token_file, 'wb') as f:
                pickle.dump({}, f)

    def get_token(self):
        if config.USEREDIS:
            token = self.r.get(self.token_name)
            if not token:
                return self.get_new_token()
            return token
        else:
            with open(self.token_file, 'rb') as f:
                if self.token_name in pickle.load(f):
                    token = pickle.load(f)[self.token_name]
                    if time.time() < token['expire']:
                        return token['value']
                    else:
                        return self.get_new_token()
                else:
                    return self.get_new_token()

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
            if config.USEREDIS:
                self.r.set(self.token_name, new_token, ex=token_expire)
                return new_token
            else:
                tokens = None
                with open(self.token_file, 'rb') as f:
                    tokens = pickle.load(f)
                tokens[self.token_name] = {}
                tokens[self.token_name]['value'] = new_token
                tokens[self.token_name]['expire'] = int(time.time()) + int(token_expire)
                with open(self.token_file, 'wb') as f:
                    pickle.dump(tokens, f)
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
                requests.post(url, params=params, data=msg_data)
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

