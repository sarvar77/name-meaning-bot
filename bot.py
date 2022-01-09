import requests
from bs4 import BeautifulSoup
import telebot
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"😀 <b>Assalomu alaykum, {name}!\n\n"
                                      f"🤖 Botimizga xush kelibsiz!\n\n"
                                      f"📄 Sizga kerakli ismning ma'nosini bilish uchun botga ismni text formatida yuboring!</b>\n\n"
                                      f"<i>Masalan: Sarvar</i>", parse_mode="html")


@bot.message_handler(content_types=["text"])
def parser(message):
    user_text = message.text
    headers = {
        "accept": "/*/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    search_query = f"https://ismlar.com/name/{user_text}"

    try:
        response = requests.get(search_query, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        meaning = soup.find("div", class_="text-size-5") # block
        paragraph = meaning.find("p").get_text(strip=True)
        li = meaning.find("ul", class_="list-inline").get_text(strip=True).replace(",", ", ")
        bot.send_message(message.chat.id, f"<b>❓ Siz so'ragan ism:</b> {user_text}\n\n"
                                          f"<b>📄 Ma'nosi:</b> {paragraph}\n\n"
                                          f"<b>🎭 Shakllari:</b> {li}", parse_mode="html")
    except:
        bot.send_message(message.chat.id, "😕 Afsus, bunday ism topilmadi. Hato yozgan bo'lishingiz mumkin, yana bir bor urinib ko'ring!")


bot.polling(none_stop=True)