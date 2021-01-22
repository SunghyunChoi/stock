import json
import requests
# import time
from datetime import datetime
from pandas.io.json import json_normalize


# json_slack_path = "./token.json"
# with open(json_slack_path, 'r') as json_file:
#     slack_dict = json.load (json_file)

# slack_token = slack_dict['token']

# 채널 찾기
# ChannelName = "주식-웹사이트-만들기"
# URL = 'https://slack.com/api/conversations.list'
# params = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'token': slack_token
#           }
# res = requests.get(URL, params = params)
# channel_list = json_normalize(res.json()['channels'])
# channel_id = list(channel_list.loc[channel_list['name'] == ChannelName, 'id'])[0]
# print(f"""
# # 채널 이름: {ChannelName}
# # 채널 id: {channel_id}
# # """)
class slack_bot:
        def __init__(self):
                self.token = "xoxb-1543956691168-1628388530791-qmoRZSziF3fD0csLF4O2XjYV"
                self.channel_id = "G01HZ0FBL9J"
        def send(self, message):
                self.data = {'Content-Type': 'application/x-www-form-urlencoded',
                        'token': self.token,
                        'channel': self.channel_id, 
                        'message': message
                }

                URL = "https://slack.com/api/chat.postMessage"
                res = requests.post(URL, data=self.data)
                print(res)

# {datetime.today().strftime("%m/%d %H:%M")}
message ="""
{
        "bot_id": "B01JXATM7AP",
        "type": "message",
        "text": "test",
        "user": "U01JGBEFLP9",
        "ts": "1611189923.000500",
        "team": "T01FZU4LB4Y",
        "bot_profile": {
            "id": "B01JXATM7AP",
            "deleted": false,
            "name": "eco",
            "updated": 1610759123,
            "app_id": "A01KLV7KSJC",
            "icons": {
                "image_36": "https://a.slack-edge.com/80588/img/plugins/app/bot_36.png",
                "image_48": "https://a.slack-edge.com/80588/img/plugins/app/bot_48.png",
                "image_72": "https://a.slack-edge.com/80588/img/plugins/app/service_72.png"
            },
            "team_id": "T01FZU4LB4Y"
        },
        "attachments": [
            {
                "fallback": "680x448px image",
                "image_url": "https://newsimg.hankookilbo.com/cms/articlerelease/2019/04/29/201904291390027161_3.jpg",
                "image_width": 680,
                "image_height": 448,
                "image_bytes": 170105,
                "text": "text-world",
                "pretext": "pre-hello",
                "id": 1
            }
        ]
    }

"""
test = slack_bot()
test.send(message)