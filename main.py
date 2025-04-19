import discord
from discord.ext import commands, tasks
import os
import random
import aiohttp
import io
from datetime import datetime
from myserver import server_on

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.members = True  # เปิดใช้งาน Server Members Intent

bot = commands.Bot(command_prefix='!', intents=intents)

# ใช้ environment variable สำหรับ Token
TOKEN = os.getenv('TOKEN')
chat_channel_id = 1362748298858991778  # ใส่ ID ของช่องแชท
server_channel_id = 1363123342135132351  # ใส่ ID ของช่องเซิร์ฟเวอร์

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s) synced.")
    send_random_messages.start()

@tasks.loop(seconds=20)
async def send_random_messages():
    messages = [
   'มึงเข้ามาแล้วเหรอ? มาทำไม 🤨🔥',
    'มาดิไม่กลัวเลย เดี๋ยวขยี้ให้ดู 😎💥',
    'กูรออยู่, จะหนีไปไหน 🤡',
    'ไหน มึงกล้าพูดแบบนี้กับกูหรอ 😈💬',
    'มึงคิดว่ามากูจะกลัวหรอ? โทษที กูขำ 🤣',
    'มีอะไรจะบอก กูฟังอยู่ 😜👌',
    'มาดิ มาเล่นกับกูหน่อย 🔥',
    'เอ้า!! ทำไมไม่มาต่อสู้บ้าง 😤',
    'เข้ามาดิ!! 😎🔥',
    'เอาดิ ไม่กล้าเหรอ 😏',
    'มีไรก็มาดิครับ 💥',
    'ไหนใครแน่ 😈',
    'โอ้โห คิดว่ากลัวหรอ 🤣',
    'มาเล่นกันหน่อยไหมเพื่อน 😜',
    'ใจถึงพึ่งได้ 🔥',
    'มาท้าให้ได้กูไม่รอ 😤',
    'เล่นกันเถอะ อยากเห็นคนทำตาม 😜',
    'มึงมาทำไม 😏 หรือต้องให้กูท้าอีก? 🔥',
    'มาเล่นกันเถอะ จะได้ดูว่ากูเจ๋งขนาดไหน 😎💥',
    'อยากลองของจริงเหรอ? กูรออยู่ 😈',
    'กล้าเข้ามาเหรอ? กูแค่รอเวลาจัดการ 😈💀',
    'มึงจะหนีไปไหน? 😏🔥 อยู่ตรงนี้แหละ 😜',
    'เอาดิ ไม่กล้าเหรอ? 🤡 มาดูใครเจ๋งกว่า 😎💥',
    'มาเถอะ อยากเห็นว่ามึงจะทำได้ไหม 😈💥',
    'แค่นี้มึงก็คิดจะหยุดแล้วเหรอ? 😏 กูยังไม่เหนื่อยเลย 🔥',
    'เข้ามาเลย กูรออยู่ 😏 อย่าบอกนะว่ากลัว 😈',
    'พูดไปเรื่อยๆ แต่ทำไมไม่กล้ามาเลย 😎🔥',
    'เหยียบมาเหอะ แล้วกูจะโชว์ให้ดูว่าเจ๋งแค่ไหน 😈💥',
    'มึงคิดว่ากลัวหรอ? กูขำ 🤣🔥 มาเลย! 😜',
    'จะให้กูแสดงให้ดูไหม? กูรออยู่ 🔥💥',
    'ไม่ต้องกลัวไป กลัวไปก็ไม่น่าสนุก 😜🔥',
    'กูจะบอกให้มึงรู้เองว่าใครแน่ 🔥😈',
    'ไม่รู้เหรอว่ามึงทำอะไรมันก็ไม่พอสำหรับกู 😏💥',
    'มามิ รอดูหน่อยว่าคุณกล้าไหม 😜🔥',
    'จะวิ่งหนีเหรอ? ทำไมไม่สู้แบบแมนๆ ไปเลย 😈💥',
    'หายไปไหน? กูรอคำท้า 😏🔥',
    'ใครกล้าเข้ามา? หรือจะให้กูเชิญ 😜🔥',
    'มีอะไรอีกไหม? กูพร้อมทุกเวลา 😈💥',
    'คอยดูให้ดี มึงจะได้รู้เองว่าใครเจ๋ง 🔥😎'
    ]

    chat_channel = bot.get_channel(chat_channel_id)
    server_channel = bot.get_channel(server_channel_id)

    if chat_channel:
        random_message = random.choice(messages)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.imgflip.com/get_memes') as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data and 'memes' in data['data']:
                        meme = random.choice(data['data']['memes'])
                        async with session.get(meme['url']) as img_response:
                            if img_response.status == 200:
                                img_data = await img_response.read()
                                file = discord.File(io.BytesIO(img_data), 'meme.jpg')
                                await chat_channel.send(content=random_message, file=file)

    if server_channel:
        time_now = datetime.utcnow().strftime('%H:%M:%S')
        guild = server_channel.guild
        member_count = guild.member_count
        roles = '\n'.join([role.name for role in guild.roles]) or 'ไม่มีบทบาท'

        status_message = f"""
**🕒 เวลาปัจจุบัน:** {time_now}
**👥 จำนวนสมาชิกในเซิร์ฟ:** {member_count}
**📜 บทบาทในเซิร์ฟ:**
{roles}
        """
        await server_channel.send(status_message)

server_on()

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Token not found! Please set the TOKEN environment variable.")
