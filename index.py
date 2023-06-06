from skpy import SkypeEventLoop, SkypeNewMessageEvent
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('CHAT_GPT_KEY')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
print(openai.api_key)

class SkypePing(SkypeEventLoop):
    def __init__(self, username, password):
        super(SkypePing, self).__init__(username, password)
        print("initialized! watching for events")

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) \
            and not event.msg.userId == self.userId :
            print(event.msg)
            # sending automated reply
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You're name is Pawan."},
                    {"role": "user", "content": event.msg.content},
                ]
            )['choices'][0]['message']['content']
            event.msg.chat.sendMsg(response)

sk = SkypePing(username,password)
sk.loop()
