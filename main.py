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

app = Flask(__name__)

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = "4s8YFCt+o+xQn1/y1L//cvcZMx7ROzqYgwyoRQj5CqKMmQaHg2hjoQlfedKBMi6yw/aCrDiXuqzydU95u02WjgVLNaP2Pdr20liRmI/sHe+G2Mpo5wQCbKf7hbrlFOCBaRDtQlVbPNV2ftCSJme/uAdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "66a4d2043b7fdc13bd5ebb03ff80b71f"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
# 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
# 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
# handleの処理を終えればOK
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)