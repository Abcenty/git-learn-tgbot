import requests
from time import time, sleep
from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '6023265531:AAGNNCEPU1jSqHli7DnkeqZrl7ztWCj5vP0'
TIMEOUT: int = 60


def request_for_bot_info() -> None:
    num_info = requests.get("https://api.telegram.org/bot6023265531:AAGNNCEPU1jSqHli7DnkeqZrl7ztWCj5vP0/getMe")
    if num_info.status_code == 200:
        print(num_info.text)
    else:
        print(num_info.status_code)


def parrot_func() -> None:

    offset: int = -2
    chat_id: int
    message = 'You are amazing!)'

    while True:
        start_time = time()
        updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={TIMEOUT}').json()

        if updates['result']:
            for result in updates['result']:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}')

        sleep(3)
        end_time = time()
        print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')


def send_a_cat_func() -> None:

    compliments: dict = {'1': 'You are amazing:3!', '2': 'You are perfect!)', '3': 'You are beautiful!)',
                         '4': 'You are sunny)', '5': 'You are cool)'}
    error_text: str = 'Здесь должна была быть картинка с котиком :('
    api_cats_url: str = 'https://api.thecatapi.com/v1/images/search'
    offset: int = -2
    cat_response: requests.Response
    cat_link: str

    while True:
        compliment_num = randint(1, 5)
        compliment_num = str(compliment_num)
        print(compliment_num)
        start_time = time()
        updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={TIMEOUT}').json()

        if updates['result']:
            for result in updates['result']:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                cat_response = requests.get(api_cats_url)
                if cat_response.status_code == 200:
                    cat_link = cat_response.json()[0]['url']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}'
                                 f'&text={compliments[compliment_num]} Take a cat)')
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={error_text}')
        sleep(3)
        end_time = time()
        print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')


bot: Bot = Bot(token='6023265531:AAGNNCEPU1jSqHli7DnkeqZrl7ztWCj5vP0')
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


def main():
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
