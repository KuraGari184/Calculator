import telebot
from telebot import types
import math

API_TOKEN = '6769708431:AAE_t6m1Z5CfknYsSyhwWnvIn2zr8-rUoGk'

bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store user data
user_data = {}


# Function to create the calculator keyboard
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [['C', 'DEL', '^', '%'], ['7', '8', '9', '/'],
               ['4', '5', '6', '*'], ['1', '2', '3', '-'],
               ['(', '0', ')', '+'], ['.', 'π', '=']]
    for row in buttons:
        keyboard.row(*[
            types.InlineKeyboardButton(text=char, callback_data=char)
            for char in row
        ])
    return keyboard


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = ''
    bot.send_message(
        message.chat.id,
        "Welcome to the Calculator Bot! Use /cal to use Calculator")


# Command to start the calculator
@bot.message_handler(commands=['cal'])
def cal(message):
    photo = "https://img.freepik.com/premium-vector/calculator-neon-sign-mathematics-lesson-banner_98480-1147.jpg"
    cal_text = "<a href='{}'><b>Enter to use your Calculator</b></a>".format(
        photo)
    buttons = [types.InlineKeyboardButton("Enter", callback_data='enter')]
    markup = types.InlineKeyboardMarkup()
    markup.add(buttons[0])
    bot.send_message(message.chat.id,
                     cal_text,
                     reply_markup=markup,
                     parse_mode="HTML")


# Handler for 'Enter' button press
@bot.callback_query_handler(func=lambda call: call.data == 'enter')
def handle_enter(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    photo = "https://img.freepik.com/premium-vector/calculator-neon-sign-mathematics-lesson-banner_98480-1147.jpg"
    enter_text = """<b>Use the buttons below to enter your <a href='{}'>calculation</a>.</b>\n<code>Press "=" to get the result, "C" to clear, and "DEL" to delete the last entry.</code>""".format(
        photo)
    user_data[chat_id] = ''
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=enter_text,
                          reply_markup=create_keyboard(),
                          parse_mode="HTML")


# Preprocess the expression to handle implicit multiplication and pi
def preprocess_expression(expression):
    result = ""
    i = 0
    while i < len(expression):
        if expression[i] == 'π':
            result += str(math.pi)
        elif i > 0 and expression[i] == '(' and (expression[i - 1].isdigit()
                                                 or expression[i - 1] == ')'):
            result += '*('
        elif expression[i] == '^':
            result += '**'
        else:
            result += expression[i]
        i += 1
    return result


# Callback query handler for calculator buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data
    photo = "https://img.freepik.com/premium-vector/calculator-neon-sign-mathematics-lesson-banner_98480-1147.jpg"
    thank_you_photo = "https://cdn.vectorstock.com/i/500p/87/41/neon-lettering-thank-you-on-a-dark-background-vector-40078741.jpg"

    if chat_id not in user_data:
        user_data[chat_id] = ''

    if data == 'C':
        user_data[chat_id] = ''
    elif data == 'DEL':
        user_data[chat_id] = user_data[chat_id][:-1]
    elif data == '=':
        try:
            # Preprocess the expression and replace ^ with ** for exponentiation
            expression = preprocess_expression(user_data[chat_id]).replace(
                '^', '**')
            result = str(eval(expression))
        except Exception as e:
            result = 'Error'
        user_data[chat_id] = result
        user_datas = user_data[chat_id]
        photo_text = """<b><a href='{}'>Result</a> : </b>""".format(
            thank_you_photo)
        final_text = photo_text + user_datas

        bot.edit_message_text(chat_id=chat_id,
                              message_id=call.message.message_id,
                              text=final_text,
                              parse_mode="HTML")
        user_data[chat_id] = ''  # Reset user data after showing result
        return
    else:
        user_data[chat_id] += data

    user_datas = user_data[chat_id] if user_data[chat_id] else '0'
    photo_text = """<b><a href='{}'>Your Calculation</a></b>\n<code>Press "=" to get the result, "C" to clear, and "DEL" to delete the last entry.</code>\n\n""".format(
        photo)
    final_text = photo_text + str(user_datas)

    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=final_text,
                          reply_markup=create_keyboard(),
                          parse_mode="HTML")


# Polling
bot.infinity_polling()
