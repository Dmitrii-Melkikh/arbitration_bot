from aiogram import types
from aiogram.dispatcher.filters import Text
import asyncio
import bot_config.data
from arbitr_parser import kad
from arbitr_parser import url_processing
import random
import time

def Buttoms(dp, bot, chat_id, access_id):

    loop = asyncio.get_event_loop()
    @dp.message_handler(commands="start")
    async def tap1(message: types.Message):
        if message.from_user.id in chat_id:
            await message.answer("Добро пожаловать в бота!")
            if len(bot_config.data.mail_list) == 0:
                bot_config.data.mail_list.append(message.from_user.id)
                loop.create_task(mail())
            elif (message.from_user.id) not in bot_config.data.mail_list:
                bot_config.data.mail_list.append(message.from_user.id)
        else:
            await message.answer("Нет доступа")


    @dp.message_handler(commands="stop")
    async def tap2(message: types.Message):
        bot_config.data.mail_list.remove(message.from_user.id)
        await message.answer("Рассылка остановлена")

    @dp.message_handler(commands="continue")
    async def tap3(message: types.Message):
        if message.from_user.id in chat_id:
            await message.answer("Рассылка возобовлена")
            if len(bot_config.data.mail_list) == 0:
                bot_config.data.mail_list.append(message.from_user.id)
                loop.create_task(mail())
            elif (message.from_user.id) not in bot_config.data.mail_list:
                bot_config.data.mail_list.append(message.from_user.id)


# """while True:
#     if time == "12;00":
#         scrapper = kad.DriverScrapping()
#         scrapper.scrap()
#     if time == '9;00':
#         url_var = url_processing.Processing()
#         urls = url_var.scrap_checked_case()
#         #[[ссылка на страницу на кад.арбитр, ссылка на пдф], [], [],..]
# """
    async def mail():
        while bot_config.data.mail_list:
            await asyncio.sleep(5)
            scrapper = kad.DriverScrapping()
            await scrapper.scrap()
            await scrapper.driver.quit()
            # url_var = url_processing.Processing()
            # urls = await url_var.scrap_checked_case()
            # url_var.driver.quit()
            for j in bot_config.data.mail_list:
                if j in bot_config.data.mail_list:
                    if bot_config.data.mail_list:
                        # for i in urls:
                        #     message=f"Ссылка на дело: {str(i[0])}\n"
                        #     message+=f"Ссылка на документ: {str(i[1])}\n"
                        message=''
                        await bot.send_message(chat_id=j, text=message)

    dp.register_message_handler(tap1, commands="start")
    dp.register_message_handler(tap2, commands="stop")
    dp.register_message_handler(tap3, commands="continue")



