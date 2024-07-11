from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from datetime import datetime

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile, InputMedia 
from aiogram.utils.deep_linking import get_start_link

import bot.config.config as cfg
from bot.design.buttons import *
from db import Database
from aiogram.types import Message



bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database(r"db.db")


#функции в приватных сообщениях бота
@dp.message_handler()
async def check(message : types.Message):
		if message.text[:6] == "/start":
			if message.chat.type == "private":

				if db.user_exists(message.from_user.id) == False:

					start_command = message.text

					reffer_id = int(start_command[7:])
					refferals = 0
					balance = 0
					users = db.get_data_users()
					for row in users:
						if reffer_id == row[0]:
							refferals = row[5]
							balance = row[4]

					if str(reffer_id) != "":

						if int(reffer_id) != int(message.from_user.id):
							print(True)
							db.add_user(message.from_user.id, message.from_user.username, reffer_id)
							db.set_money(reffer_id, int(balance) + 3000)
							new_refferals = refferals + 1
							db.set_ref_user(reffer_id, new_refferals)

						else:
							await bot.send_message(int(message.from_user.id),
												   "Нельзя регистрироваться по своей ссылке")

					else:
						db.add_user(message.from_user.id, message.from_user.username)
				
				for t in db.get_data_users():
					if t[0] == message.from_user.id:
						background_photo = InputFile(r'assets/bg.jpg')
						if t[6] == "en":
							await bot.send_photo(message.from_user.id, caption="MENU", photo = background_photo, reply_markup = start_markup_en)

						elif t[6] == "ru":
							await bot.send_photo(message.from_user.id, caption="Главное меню", photo = background_photo, reply_markup = start_markup_ru)

@dp.callback_query_handler(lambda c: c.data.startswith('profile'))
async def profile(call: types.CallbackQuery):
	await bot.delete_message(chat_id=call.message.chat.id, message_id = call.message.message_id)
	for user in db.get_data_users():
		if user[0] == call.from_user.id:
			if user[6] == "en":
				
				await bot.send_photo(call.from_user.id, InputFile(r'assets/bg_profile.jpg'), caption = f'''<b>💾Profile @{call.from_user.username}</b>\n◼◼◼◼◼\n<b>♟Experience</b> <b><i>{user[4]}</i></b>\n<b>📓Rank <i>{db.get_user_rank_by_balance(call.from_user.id)}</i></b>''', reply_markup = back_markup_en, parse_mode=types.ParseMode.HTML)
			elif user[6] == "ru":
				await bot.send_photo(call.from_user.id, InputFile(r'assets/bg_profile.jpg'), caption = f'''<b>💾Profile @{call.from_user.username}</b>\n◼◼◼◼◼\n<b>♟Очки</b> {user[4]}\n<b>📓Место в топе <i>{db.get_user_rank_by_balance(call.from_user.id)}</i></b>''', reply_markup = back_markup_ru, parse_mode=types.ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data.startswith('quests'))
async def col1(call: types.CallbackQuery):
	await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
	for user in db.get_data_users():
		if user[0] == call.from_user.id:
			if user[6] == "en":
				markup_tasks = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "Subscription telegram channel #1", callback_data = "subscripition1")).add(InlineKeyboardButton(text = "Subscription telegram channel #2", callback_data = "subscripition2")).add(InlineKeyboardButton(text = "Subscription on twitter", callback_data = "subscripition_twitter")).add(InlineKeyboardButton(text = "↩️Rerurn back", callback_data = "return_back"))
				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_quests.jpg'), caption = "<b>🔽Below are availiable quests for you🔽</b>", reply_markup = markup_tasks, parse_mode=types.ParseMode.HTML)
			elif user[6] == "ru":
				markup_tasks = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "Подписка на телеграмм #1", callback_data = "subscripition1")).add(InlineKeyboardButton(text = "Подписка на телеграмм #2", callback_data = "subscripition2")).add(InlineKeyboardButton(text = "Подписка на твиттер", callback_data = "subscripition_twitter")).add(InlineKeyboardButton(text = "↩️Вернуться назад", callback_data = "return_back"))

				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_quests.jpg'), caption = "<b>🔽Ниже есть доступные задания для тебя🔽</b>", reply_markup = markup_tasks, parse_mode=types.ParseMode.HTML)




@dp.callback_query_handler(lambda c: c.data.startswith('return_back'))
async def turning_back(call: types.CallbackQuery):
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	for t in db.get_data_users():
		if t[0] == call.from_user.id:
			background_photo = InputFile(r'assets/bg.jpg')
			if t[6] == "en":
				
				await bot.send_photo(call.from_user.id, caption="MENU", photo = background_photo, reply_markup = start_markup_en)
			elif t[6] == "ru":
				await bot.send_photo(call.from_user.id, caption="Главное меню", photo = background_photo, reply_markup = start_markup_ru)


@dp.callback_query_handler(lambda c: c.data.startswith('invites'))
async def invites(call: types.CallbackQuery):
	referral_link = f"https://t.me/dfddfdfdffddf_bot?start={call.from_user.id}"
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	
	for user in db.get_data_users():
		if user[0] == call.from_user.id:
			if user[6] == "en":
				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_invites.jpg'), caption = f"<b>👤@{call.from_user.username}</b>\n🔽Your Refferal link🔽\n<b>{referral_link}</b>\n\n<b>Refferals: <i>{user[5]}</i></b>", reply_markup =back_markup_en, parse_mode=types.ParseMode.HTML)
			elif user[6] == "ru":
				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_invites.jpg'), caption = f"<b>👤@{call.from_user.username}</b>\n🔽Ваша Рефферальная ссылка🔽\n{referral_link}\n\n<b>К-во реффералов: <i>{user[5]}</i></b>", reply_markup =back_markup_ru, parse_mode=types.ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data.startswith('top') or c.data.startswith('reload_top'))
async def ranking(call: types.CallbackQuery):
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	top_users = db.get_top_10_users()
	text = ""
	for rank, (username, balance) in enumerate(top_users, start=1):
		text += f"<b>{rank}</b>. <i>@{username}</i> - {balance}\n"
	
	for user in db.get_data_users():
		if user[0] == call.from_user.id:
			if user[6] == "en":
				markup_top = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "🔃Reload", callback_data = "reload_top")).add(InlineKeyboardButton(text = "↩️Rerurn back", callback_data = "return_back"))
				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_top.jpg'), caption=f"TOP-10\n\n{text}\n<b>Your place {db.get_user_rank_by_balance(call.from_user.id)}</b>", reply_markup = markup_top, parse_mode=types.ParseMode.HTML)
			elif user[6] == "ru":
				markup_top = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "🔃Перезапустить", callback_data = "reload_top")).add(InlineKeyboardButton(text = "↩️Вернуться назад", callback_data = "return_back"))
				await bot.send_photo(call.from_user.id, photo = InputFile(r'assets/bg_top.jpg'), caption=f"TOP-10\n\n{text}\n<b>Ваше место {db.get_user_rank_by_balance(call.from_user.id)}</b>", reply_markup = markup_top, parse_mode=types.ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data.startswith('settings'))
async def settings(call: types.CallbackQuery):
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	for user in db.get_data_users():
		if user[0] == call.from_user.id:
			markup_language = InlineKeyboardMarkup()
			markup_language.add(InlineKeyboardButton(text="🇷🇺Russian", callback_data="ru_lang_change")).add(InlineKeyboardButton(text="🇺🇸English", callback_data="en_lang_change"))
			if user[6] == "en":
				markup_language.add(InlineKeyboardButton(text = "↩️Вернуться назад", callback_data = "return_back"))
				await bot.send_message(call.from_user.id, "🏴Choose language:", reply_markup = markup_language)
			elif user[6] == "ru":
				markup_language.add(InlineKeyboardButton(text = "↩️Return Back", callback_data = "return_back"))
				await bot.send_message(call.from_user.id, "🏴Выберите язык:", reply_markup = markup_language)

@dp.callback_query_handler(lambda c: c.data.startswith('ru_lang_change') or c.data.startswith('en_lang_change'))
async def settings(call: types.CallbackQuery):
	db.set_user_lang(call.from_user.id, call.data.split("_")[0])
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	

	for t in db.get_data_users():
		if t[0] == call.from_user.id:
			background_photo = InputFile(r'assets/bg.jpg')
			if t[6] == "en":
				await bot.send_photo(call.from_user.id, caption="MENU", photo = background_photo, reply_markup = start_markup_en)

			elif t[6] == "ru":
				await bot.send_photo(call.from_user.id, caption="Главное меню", photo = background_photo, reply_markup = start_markup_ru)


if __name__ == "__main__":
	try:
		executor.start_polling(dp, skip_updates=True)
	
	except Exception:
		pass
