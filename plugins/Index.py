# ====================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠====================================================
START_MSG="Hi {},\nThis is a simple bot to forward all messages from one channel to other\n\n⚠️Warning\nYour account may get banned if you forward more files(from private channels). Use at Own Risk!!"
HELP_MSG="Available commands:-\n\n/index - To index a channel\n/forward - To start forwarding\n/total - Count total messages in DB\n/status - Check Current status\n/help - Help data\n/stop - To stop all running processes. \n/cleardb - clear all files in database.\n\nUse /index to index messages from a channel to database.\n\nAfter indexing you can start forwarding by using /forward.\n\n<b>Note:</b>\nYou will require the following data to index a channel:-\n\n<b>Channel Invite Link</b>:- If channel is a Private channel User needs to join channel to acces the messages. Please note that do not leave channel until forwarding completes.\n\n<b>Channel ID</b>:- If channel is a private channel you may need to enter Channel ID. Get it from @ChannelidHEXbot.\n\n<b>SKIP_NO</b>:-From where you want to start Forwarding files.Give 0 if from starting\n\n<b>Caption</b>:- Custom Caption for forwarded files. Use 0 to use default captions."
ABOUT_TXT=""" #sOoN"""
# ====================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠========================================================================================================================================================================================================================≠====================================================

import pytz
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import InviteHashExpired, UserAlreadyParticipant
from config import Config
import re
from bot import Bot
from asyncio.exceptions import TimeoutError
from database import save_data
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)

limit_no=""               
skip_no=""
caption=""
channel_type=""
channel_id_=""
IST = pytz.timezone('Asia/Kolkata')
OWNER=int(Config.OWNER_ID)


@Client.on_message(filters.private & filters.command(["index"]))
async def run(bot, message):
    if message.from_user.id != OWNER:
        await message.reply_text("🤫 wHo thE hElL aRe YoU!!")
        return
    while True:
        try:
            chat = await bot.ask(text = "To Index a channel you may send me the channel invite link, so that I can join channel and index the files.\n\nIt should be something like <code>https://t.me/xxxxxx</code> or <code>https://t.me/joinchat/xxxxxx</code>", chat_id = message.from_user.id, filters=filters.text, timeout=30)
            channel=chat.text
            await chat.delete()
        except TimeoutError:
            await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return

        pattern=".*https://t.me/.*"
        result = re.match(pattern, channel, flags=re.IGNORECASE)
        if result:
            print(channel)
            break
        else:
            await chat.reply_text("Wrong URL")
            continue

    if 'joinchat' in channel:
        global channel_type
        channel_type="private"
        try:
            await bot.USER.join_chat(channel)
        except UserAlreadyParticipant:
            pass
        except InviteHashExpired:
            await chat.reply_text("Wrong URL or User Banned in channel.")
            return
        while True:
            try:
                id = await bot.ask(text = "Since this is a Private channel I need Channel id, Please send me channel ID\n\nIt should be something like <code>-100xxxxxxxxx</code>", chat_id = message.from_user.id, filters=filters.text, timeout=30)
                channel=id.text
            except TimeoutError:
                await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
                return
            channel=id.text
            if channel.startswith("-100"):
                global channel_id_
                channel_id_=int(channel)
                break
            else:
                await chat.reply_text("Wrong Channel ID")
                continue

            
    else:
        #global channel_type
        channel_type="public"
        channel_id = re.search(r"t.me.(.*)", channel)
        #global channel_id_
        channel_id_=channel_id.group(1)

    while True:
        try:
            SKIP = await bot.ask(text = "Send me from where you want to start forwarding\nSend 0 for from beginning.", chat_id = message.from_user.id, filters=filters.text, timeout=30)
            print(SKIP.text)
        except TimeoutError:
            await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return
        try:
            global skip_no
            skip_no=int(SKIP.text)
            break
        except:
            await SKIP.reply_text("Thats an invalid ID, It should be an integer.")
            continue
    while True:
        try:
            LIMIT = await bot.ask(text = "Send me from Upto what extend(LIMIT) do you want to Index\nSend 0 for all messages.", chat_id = message.from_user.id, filters=filters.text, timeout=30)
            print(LIMIT.text)
        except TimeoutError:
            await bot.send_message(message.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return
        try:
            global limit_no
            limit_no=int(LIMIT.text)
            break
        except:
            await LIMIT.reply_text("Thats an invalid ID, It should be an integer.")
            continue

    buttons=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 ALL MEDIA", callback_data="all")
            ],
            [
                InlineKeyboardButton("🗃️ DOCUMENT", callback_data="docs"),
                InlineKeyboardButton("🖼️ PHOTOS", callback_data="photos")
            ],
            [
                InlineKeyboardButton("🎦 VIDEOS", callback_data="videos"),
                InlineKeyboardButton("🎵 AUDIOS", callback_data="audio")
            ]
        ]
        )
    await LIMIT.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Ok,\nNow choose what type of messages you want to forward.",
        reply_markup=buttons
        )

@Client.on_callback_query()
async def cb_handler(bot: Client, query: CallbackQuery):
    filter=""
    if query.data == "docs":
        filter="document"
    elif query.data == "all":
        filter="empty"
    elif query.data == "photos":
        filter="photo"
    elif query.data == "videos":
        filter="video"
    elif query.data == "start":
        await query.message.edit_text(
            text=START_MSG.format(query.from_user.first_name),
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("ℹ️ HELP", callback_data="help"),
                InlineKeyboardButton("💫 ABOUT", callback_data="abt")
                ],[
                InlineKeyboardButton("🍂 SUPPORT 🍂", url="https://t.me/PYRO_BOTZ_CHAT")
                ]]
                )
            )
    elif query.data == "help":
        await query.message.edit_text(
            text=HELP_MSG,
            reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
                 InlineKeyboardButton("↩️ BACK", callback_data="start")
                 ]]
                 )
            )

    elif query.data == "abt":
        await query.message.edit_text(
            text=ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
                 InlineKeyboardButton("↩️ BACK", callback_data="start")
                 ]]
                 )
            )
    elif query.data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif query.data == "audio":
        filter="audio"
    caption=None


    await query.message.delete()
    while True:
        try:
            get_caption = await bot.ask(text = "Do you need a custom caption?\n\nIf yes , Send me caption \n\nif No send '0'", chat_id = query.from_user.id, filters=filters.text, timeout=30)
        except TimeoutError:
            await bot.send_message(query.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /index")
            return
        input=get_caption.text
        if input == "0":
            caption=None
        else:
            caption=input
        break
    
    sdatetime_ist = datetime.now(IST)
    SSTIME = sdatetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
    m = await bot.send_message(
        text="<b>✓ Indexing Started</b>",
        chat_id=query.from_user.id
    )
    total_files = 0
    duplicate = 0
    errors = 0
    msg_count = 0
    mcount = 0
    FROM=channel_id_
    try:
        async for MSG in bot.USER.search_messages(chat_id=FROM,offset=skip_no,limit=limit_no,filter=filter):
            if channel_type == "public":
                methord="bot"
                channel=FROM
                msg=await bot.get_messages(FROM, MSG.message_id)
            elif channel_type == "private":
                methord="user"
                channel=str(FROM)
                msg=await bot.USER.get_messages(FROM, MSG.message_id)
            msg_caption=""
            if caption is not None:
                msg_caption=caption
            elif msg.caption:
                msg_caption=msg.caption
            if filter in ("document", "video", "audio", "photo"):
                for file_type in ("document", "video", "audio", "photo"):
                    media = getattr(msg, file_type, None)
                    if media is not None:
                        file_type = file_type
                        id=media.file_id
                        break
            if filter == "empty":
                for file_type in ("document", "video", "audio", "photo"):
                    media = getattr(msg, file_type, None)
                    if media is not None:
                        file_type = file_type
                        id=media.file_id
                        break
                else:
                    id=f"{FROM}_{msg.message_id}"
                    file_type="others"
            
            message_id=msg.message_id
            try:
                aynav, vnay = await save_data(id, channel, message_id, methord, msg_caption, file_type)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
            except Exception as e:
                print(e)
                errors += 1
               # await bot.send_message(OWNER, f"LOG-Error-{e}")
                pass
            msg_count += 1
            mcount += 1
            new_skip_no=str(skip_no+msg_count)
            print(f"Total Indexed : {msg_count} - Current SKIP_NO: {new_skip_no}")
            if mcount == 5:
                try:
                    datetime_ist = datetime.now(IST)
                    ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                    await m.edit_text(f"<b><u>INDEXING RESULTS</u>\n\nTotal messages fetched : {msg_count}\nTotal Indexed : {total_files}\nDuplicate files : {duplicate}\nErrors : {errors}\nCurrent skip no : {new_skip_no}\n\nIndexing From : {FROM}\n\nIndex started at : {SSTIME}\nLast indexed : {ISTIME}</b>")
                    mcount -= 5
                except FloodWait as e:
                    print(f"Floodwait {e.x}")
                    pass
                except Exception as e:
                   # await bot.send_message(chat_id=OWNER, text=f"LOG-Error: {e}")
                    print(e)
                    pass
        await m.edit(f"<b><u>INDEXED RESULTS</u>\n\n💫 Succesfully Indexed : {total_files} Files.\nIndexed from : {FROM}\nDuplicate files : {duplicate}\nErrors : {errors}\nCurrent skip no : {new_skip_no}\n\nIndex started at : {SSTIME}\nIndexing Ended : {ISTIME}</b>")
    except Exception as e:
        print(e)
        await m.reply_text(f"Error: {e}")
        pass
