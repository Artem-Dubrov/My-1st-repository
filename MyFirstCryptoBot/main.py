import telebot
from extensions import APIException,CurrencyConverter
from config import TOKEN,currency_list

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text=('Чтобы начать работу с ботом, введите команду в следующем формате: \n <Название валюты>  '
    '<В какую валюту перевести>  <Количество переводимой валюты>\n Список доступных валют по команде: /values ')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values',])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency_list.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'], )
def convert(message: telebot.types.Message):
    values = message.text.lower().split(' ')
    try:
        if len(values)!=3:
            raise APIException ('Неверное количестов аргументов')
        base, quote, amount = values
        total_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}', parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} равна {total_amount:.2f}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
