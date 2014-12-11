#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ts3
import re
import keys
import logging

logging.basicConfig(level=logging.INFO)


class ChangeNickName(object):
    def __init__(self, keys):
        self.config = keys.config
        self.msg = keys.config_nick_name_message

        try:
            self.server = ts3.TS3Server(self.config['server_ip'], self.config['server_port'])
            self.server.login(self.config['login'], self.config['password'])
            self.server.use(1)

            self.server.send_command('clientupdate', keys={'client_nickname': keys.config['nickname']})
        except EOFError as e:
            logging.error('Connection error :: %s' % e.message)
            exit()

    @staticmethod
    def check(nickname):
        matches = re.search(r'^([a-z0-9_][a-z0-9-_]{3,20})(.*)$', nickname, re.IGNORECASE | re.UNICODE)

        return True if not matches else False

    def run(self):

        text_msg = u'''
Привет друг, я робот. Я заметил что у тебя очень странное имя в TS3 и хочу попросить тебя его поменять.

Сделай чтобы оно было по формату "[B]Никнейм_в_танках (Реальное имя) всё_что_угодно_или_ничего[/B]"
Например:
    [B]Olewa1997 (Алексей) хочу в звот МС-1[/B]
    [B]ProtoNogib (Женя)[/B]

Указание ника как в танках, очень важно для тех, кто использует TessuMod:
    [URL]http://forum.worldoftanks.ru/index.php?/topic/1424400-093tessumod-wot-teamspeak-mod-overlay/[/URL]
    [URL]https://github.com/jhakonen/wot-teamspeak-mod[/URL]

Конечно ты можешь этого не делать, но тогда я буду постоянно тебе напоминать об этом.'''

        responce = self.server.send_command('clientlist')

        for user in responce.data:
            if int(user['client_type']) == 1:
                continue

            responce = self.server.send_command('servergroupsbyclientid', keys={'cldbid': user['client_database_id']})

            for group in responce.data:
                if int(group['sgid']) in self.msg['group_ids'] and self.check(user['client_nickname']):
                    self.server.send_command('sendtextmessage', keys={
                        'targetmode': 1,
                        'target': user['clid'],
                        'msg': text_msg
                    })

                    logging.info('Send message to: %s' % user['client_nickname'])


if __name__ == "__main__":
    f = ChangeNickName(keys)
    f.run()

