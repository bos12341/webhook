from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()
webhooks = []  # 웹훅을 저장할 리스트
is_sending = False  # 웹훅 전송 상태

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    global webhooks, is_sending  # 전역 변수로 선언

    if message.author == client.user:
        return

    if message.content.startswith('-웹훅추가'):
        webhook_url = message.content.split(' ')[1]  # 메시지에서 웹훅 주소 추출
        webhooks.append(webhook_url)  # 웹훅을 리스트에 추가
        with open('memo.txt', 'a') as f:
            f.write(webhook_url + '\n')  # memo.txt 파일에 웹훅 저장
        await message.channel.send('웹훅이 추가되었습니다.')

    elif message.content.startswith('-시작'):
        if is_sending:
            await message.channel.send('이미 웹훅을 전송 중입니다.')
        else:
            is_sending = True
            await start_sending_webhooks(message.channel)

    elif message.content.startswith('-중지'):
        if not is_sending:
            await message.channel.send('현재 웹훅 전송이 중지되어 있습니다.')
        else:
            is_sending = False
            await stop_sending_webhooks(message.channel)

async def start_sending_webhooks(channel):
    global webhooks, is_sending  # 전역 변수로 참조
    while is_sending:
        with open('memo.txt', 'r') as f:
            webhooks = f.read().splitlines()  # 메모장에서 웹훅 링크 읽어오기

        for webhook_url in webhooks:
            webhook = discord.Webhook.from_url(webhook_url)
            await webhook.send('@everyone https://discord.gg/prwCMs9HPm')  # 웹훅 전송
        await asyncio.sleep(3000)  # 50분(3000초) 대기

async def stop_sending_webhooks(channel):
    await channel.send('웹훅 전송이 중지되었습니다.')


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
