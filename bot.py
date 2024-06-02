import telebot
import requests
import random 

bot = telebot.TeleBot('Your-Bot-Token')



@bot.message_handler(commands=['start'])
def greetings(message):
    bot.reply_to(message, f"Hello myself Doggie I'm a dog finder bot!\nType /breeds to get started!!")    

def get_breed(message):
    rnd = random.randint(0, 9)
    try:
        response = requests.get(f'https://dog.ceo/api/breed/{message.text.casefold()}/images')
        status = response.raise_for_status()
        print(status)
        breeds = response.json()['message'][rnd]
        bot.send_photo(message.chat.id, breeds)
    except requests.HTTPError as http_err:
        print(f"Error occured{http_err}")
        bot.send_message(message.chat.id, f'The image you are trying to find is unavailable')
    except Exception as exp:
        print(f"Another exception occurred{exp}")
             

@bot.message_handler(commands=['breeds'])
def img_handler(message):
    text = f"Enter the breed name to get the image of the particular dog breed:\neg: Pug, Boxer, Labrador etc:"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, get_breed)
    
    
bot.infinity_polling()