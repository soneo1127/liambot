from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

from liam_chatbot import interact

app = Flask(__name__)

#環境変数取得
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
# YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi("yrWOodcO6KND8OjvD/HdoyM8bbJD3MlwYyArbJelDXaOEpBvHoZ9FOx/SYTYy3xNJNLjl2VQt7HkPE9U3YD/KS32ZXUbYlpyqzXGmXW91oWQ4jq+Y8g64IFLS6u81P/5rOeaEJaIGiYl0732KUTMHAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("052e52425012cf50b9b386ffc004a61c")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = interact.reply(event.message.text)
    print(reply)
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text = reply))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
