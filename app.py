#Импортируем необходимые библиотеки
import telebot
#Импорт валют и токена телеграмм бота из файла config.py
from config import values, TOKEN
#Импорт необходимых классов из файла extensions.py
from extensions import APIException, TelebotConverter

#Приветствие в консоли
print(f'Wellcom to TeleBot v 1.o !!!')
#Инициализация бота
bot = telebot.TeleBot(TOKEN)

#Обрабатываем комманды /start и /help
@bot.message_handler(commands=['start', 'help',])
def echo_tests(message: telebot.types.Message):
    messageText = '''Чтобы начать работать введите комманду боту в следующем формате:
<Имя валюты> <В какую валюту перевести> <Количество переводимой валюты>
Чтобы увидеть весь список валют, наберите /values'''
    bot.reply_to(message, messageText)

#Обрабатываем комманду /values
@bot.message_handler(commands=['values',])
def echo_tests(message: telebot.types.Message):
    messageText = 'Доступные валюты:'
    for key in values.keys():
        messageText = '\n'.join((messageText, key,))
    bot.reply_to(message, messageText)

#Обрабатываем текстовые сообщения
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        command_bot = message.text.split(' ')
        
        if len(command_bot) != 3:
            raise APIException(f'Слишком много параметров.')

        quote, base, amount = command_bot
        total_Base = TelebotConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ощибка пользователя: {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду: {e}')

    else:
        messageText = f'Цена {amount} {quote} в {base} = {total_Base}'
        bot.send_message(message.chat.id, messageText)

#Запуск бота
bot.polling()