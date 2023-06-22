from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import requests
import asyncio
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()
webhooks = []  # 웹훅을 저장할 리스트
admin_id = 934815826983395358  # 관리자 아이디

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-웹훅추가') and message.author.id == admin_id:
        webhook_url = message.content.split(' ')[1]  # 메시지에서 웹훅 주소 추출
        webhooks.append(webhook_url)  # 웹훅을 리스트에 추가
        with open('memo.txt', 'a') as f:
            f.write(webhook_url + '\n')  # memo.txt 파일에 웹훅 저장
        await message.channel.send('웹훅이 추가되었습니다.')

    elif message.content.startswith('-시작') and message.author.id == admin_id:
        await start_sending_webhooks(message.channel)

    elif message.content.startswith('-중지') and message.author.id == admin_id:
        await stop_sending_webhooks(message.channel)

async def start_sending_webhooks(channel):
    while True:
        for webhook_url in webhooks:
            try:
                response = requests.post(webhook_url, json={'content': '@everyone https://discord.gg/prwCMs9HPm'})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f'웹훅 전송 중 오류 발생: {e}')
        await asyncio.sleep(3000)  # 50분(3000초) 대기

async def stop_sending_webhooks(channel):
    webhooks.clear()  # 웹훅 리스트 초기화
    await channel.send('웹훅이 중지되었습니다.')


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
