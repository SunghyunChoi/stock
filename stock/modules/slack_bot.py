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
                self.token = "xoxb-1543956691168-1628388530791-lJRTT2tj5oSpJ3ouHGbB31Cv"
                self.channel_id = "G01HZ0FBL9J"
        def send(self, message):
                self.headers = {
                        "Content-type": "application/json; charset=utf-8",
                        "Authorization": f"Bearer {self.token}"
                }
                self.data = {
                        "token": self.token,
                        "channel": self.channel_id,
                        "text": "test",
                        "attachments": [
                                {
                                "fallback": "680x448px image",
                                "image_url": "https://newsimg.hankookilbo.com/cms/articlerelease/2019/04/29/201904291390027161_3.jpg",
                                "text": "text-world",
                                "pretext": "pre-hello"
                                }
                        ]
                }
                URL = "https://slack.com/api/chat.postMessage"
                res = requests.post(URL, headers=self.headers,data=json.dumps(self.data))
                # res = requests.post(URL, data=self.data)

                print(res)
                print(res.json())


# {datetime.today().strftime("%m/%d %H:%M")}
# message ="""

message = "타이푼은 태풍입니다"
test = slack_bot()
test.send(message)