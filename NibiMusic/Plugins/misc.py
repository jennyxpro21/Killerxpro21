import os
import asyncio
import requests
import aiohttp
import yt_dlp
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from NibiMusic.Modules.helpers.decorators import authorized_users_only
from NibiMusic.Modules.cache.clientbot import client as user
from NibiMusic.config import BOT_USERNAME, STRING_SESSION as SESSION_NAME
from NibiMusic.Modules.helpers.get_file_id import get_file_id
from youtube_search import YoutubeSearch

# ×=======================> ᴜsᴇʀʙᴏᴛ ᴊᴏɪɴ ᴄᴏᴍᴍᴀɴᴅ <==================================× #



@Client.on_message(filters.command(["join", "userbotjoin"], prefixes=["/", "!"]))
@authorized_users_only
async def join_chat(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        invite_link = await m.chat.export_invite_link()
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
            await user.join_chat(f"https://t.me/joinchat/{link_hash}")
        await m.chat.promote_member(
            (await user.get_me()).id,
            can_manage_voice_chats=True
        )
        return await user.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ.​")
    except UserAlreadyParticipant:
        admin = await m.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            await m.chat.promote_member(
                (await user.get_me()).id,
                can_manage_voice_chats=True
            )
            return await user.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ.​")
        return await user.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ.​")


# ×=======================> sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ <==================================× #

@Client.on_message(filters.command(["search", "lol"], prefixes=["/", "!"]))
async def ytsearch(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    try:
        if len(message.command) < 2:
            return await message.reply_text("» ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴀʀᴄʜ ʙᴀʙʏ !")
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎")
        results = YoutubeSearch(query, max_results=4).to_dict()
        i = 0
        text = ""
        while i < 4:
            text += f"✨ ᴛɪᴛʟᴇ : {results[i]['title']}\n"
            text += f"⏱ ᴅᴜʀᴀᴛɪᴏɴ : `{results[i]['duration']}`\n"
            text += f"👀 ᴠɪᴇᴡs : `{results[i]['views']}`\n"
            text += f"📣 ᴄʜᴀɴɴᴇʟ : {results[i]['channel']}\n"
            text += f"🔗 ʟɪɴᴋ : https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ᴄʟᴏsᴇ",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await m.edit_text(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await message.reply_text(str(e))

# ×=======================> ɪɴғᴏ <==================================× #

@Client.on_message(filters.command(["id", "stickerid"], prefixes=["/", "!"]))
async def showid(_, message: Message):
    await message.delete()
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(f"<code>{user_id}</code>")

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += "<b>ᴄʜᴀᴛ ɪᴅ</b>: " f"<code>{message.chat.id}</code>\n"
        if message.reply_to_message:
            _id += (
                "<b>ʀᴇᴩʟɪᴇᴅ ᴜsᴇʀ ɪᴅ</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += "<b>ᴜsᴇʀ ɪᴅ</b>: " f"<code>{message.from_user.id}</code>\n"
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(_id)


# ×=======================> sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ <==================================× #


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@Client.on_message(filters.command(["song", "music"], prefixes=["/", "!"]))
def song(client, message):
    message.delete()
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    chutiya = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("🔎")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "» ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ ᴛʜᴇ sᴏɴɢ ɴᴀᴍᴇ."
        )
        print(str(e))
        return
    m.edit(f"» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴏɴɢ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ sᴇʀᴠᴇʀ.")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**➠ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ​ » [ɴɪsᴛʜᴀ ᴍᴜsɪᴄ](t.me/{BOT_USERNAME}) 🍄\n➠ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ​ » {chutiya}\n➠ sᴇᴀʀᴄʜᴇᴅ ғᴏʀ » {query}**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit("**» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴇʀʀᴏʀ, ʀᴇᴩᴏʀᴛ ᴛʜɪs ᴀᴛ​ » [ʙᴏᴛ ʜᴜʙ](t.me/TheBothub)**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
