from enum import Enum
import os
from slack_sdk.web import WebClient

class SlackUtil:
    
    SLACK_LF="\n"
    
    def __init__(self):
        # clientのセットアップ
        self.client = WebClient(token=os.environ["SLACK_API_TOKEN"])
        
    # Slack投稿メッセージをBoldにする
    def bold(message):
        return "*" + message + "*"
    
    # Slack投稿メッセージをコードブロックにする
    def code(message):
        return " ```" + message + "``` "
        
    # 指定したチャンネルに投稿する
    def postMessage(self, message, channel):
        response = self.client.chat_postMessage(text=message, channel=channel)
    