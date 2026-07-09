import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Bot sozlamalari
BOT_TOKEN = '8988913587:AAFnXQYlUAgGJe_qZWFTMK1c16y6sR65-Kg'
ADMIN_ID = '7575052801'
WEB_APP_URL = 'https://keldibot-prodection.up.railway.app/index.html'

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
# Railway-dagi loyihangizning umumiy manzili (Domeni)
SERVER_URL = "https://boxoviddin-bot1-production.up.railway.app"  

def send_message(chat_id, text, keyboard=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")

# Webhook-ni avtomatik sozlash
def set_webhook():
    webhook_url = f"{BASE_URL}/setWebhook?url={SERVER_URL}/"
    try:
        response = requests.get(webhook_url).json()
        print(f"Webhook sozlamasi: {response}")
    except Exception as e:
        print(f"Webhook o'rnatishda xato: {e}")

@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    if update and 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text')

        if text == '/start':
            keyboard = {
                "keyboard": [
                    [{"text": "BRON QILISH", "web_app": {"url": WEB_APP_URL}}],
                    [{"text": "ADMIN BILAN BOGLANISH"}],
                    [{"text": "GAME CLUB JOYLASHUVI"}]
                ],
                "resize_keyboard": True
            }
            send_message(chat_id, "Keldi Botga xush kelibsiz! Quyidagilardan birini tanlang:", keyboard)
        
        elif text == 'ADMIN BILAN BOGLANISH':
            send_message(chat_id, "👤 Admin: Zuxriddinov Boxoviddin\n📞 Telefon: +998886577553\nSavollaringiz bo'lsa, bog'lanishingiz mumkin.")
            
        elif text == 'GAME CLUB JOYLASHUVI':
            info = (
                "Xush kelibsiz! Bizning Game Club — bu sizning eng yaxshi hordiq maskaningiz! \n\n"
                "Bizda eng so'nggi rusumdagi kuchli kompyuterlar va ultra tezkor internet marxat. \n"
                "Qulay kreslolar va yumshoq muhit sizga haqiqiy geymerlik zavqini taqdim etadi. \n"
                "Do'stlaringiz bilan birga o'yin o'ynash uchun eng ideal joy. \n"
                "Sifatli servis va doimo yordamga tayyor operatorlarimiz sizni kutmoqda. \n"
                "Biz har kuni 24/7 sizning xizmatingizdamiz. \n"
                "Joylashuvimiz juda qulay: Andijon viloyati, Shahrixon tumani. \n"
                "Tojmahal to'yxonasi yonida joylashganmiz, kirib kelishingizni kutamiz! \n"
                "Shunchaki o'yin emas, balki sifatli dam olishni tanlang. \n"
                "Biz bilan o'yindan olingan zavq yanada yuqori darajada bo'ladi!"
            )
            send_message(chat_id, info)
            
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    set_webhook()
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
