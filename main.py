from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep
import dotenv
from os import environ

dotenv.load_dotenv('.env')
bot_token = environ['tlg_token']
MYBOT = Bot(bot_token)
dp = Dispatcher(MYBOT)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	username = message.from_user.username
	msg = f"<b>Hello</b>, <i>{username}!</i>\nВведите /help - для справки"
	await MYBOT.send_message(message.chat.id, msg, parse_mode='html')


@dp.message_handler(commands=['whoami'])
async def whoami(message: types.Message):
	first_name = message.from_user.first_name
	last_name =message.from_user.last_name
	username = message.from_user.username
	id = message.from_user.id
	whoami_msg = f"first name: {first_name}\nlast name: {last_name}\nuser name: {username}\nid: {id}"
	await MYBOT.send_message(message.chat.id, whoami_msg)


@dp.message_handler(commands=['qr'])
async def photo(message: types.Message):
	photo = open('qr-gith.png', 'rb')
	await MYBOT.send_photo(message.chat.id, photo)


@dp.message_handler(content_types=['dice'])
async def dice_game(message: types.Message):
	usr_point = message['dice']['value']
	usr_msg_id = message.message_id
	await sleep(5)
	bot_data = await MYBOT.send_dice(message.chat.id, reply_to_message_id=usr_msg_id)
	bot_point = bot_data['dice']['value']
	await sleep(5)
	if usr_point > bot_point:
		await MYBOT.send_message(message.chat.id, f'Поздравляю! Ты выиграл!\nТвой счёт: {usr_point}\nМой счёт: {bot_point}', reply_to_message_id=usr_msg_id)
	elif usr_point < bot_point:
		await MYBOT.send_message(message.chat.id, f"Ура! Я выиграл!\nТвой счёт: {usr_point}\nМой счёт: {bot_point}", reply_to_message_id=usr_msg_id)
	else:
		await MYBOT.send_message(message.chat.id, "Ничья!\nТвой счёт:{usr_point}\nМой счёт: {bot_point}", reply_to_message_id=usr_msg_id)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	text_help = f'Введите одну из следующих команд:\n' \
	            f'<b>Основные команды:</b>\n' \
	            f'/start - Для начала работы\n' \
	            f'/whoami - Вывести имя пользователя\n' \
	            f'/help - Вывести справку о командах\n' \
	            f'/qr - Получить QR-код ссылку на разработчика\n' \
	            f'\n<b>Игра:</b>\n' \
	            f'Отправьте боту cмайлик 🎲 "игральные кости" для начала игры\n' \
	            f'<i>Created by:</i> <b>EPluribusNEO</b>'
	await MYBOT.send_message(message.chat.id, text_help, parse_mode='html')



if __name__ == '__main__':
	executor.start_polling(dp, loop=True)


