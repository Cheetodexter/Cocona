import discord
import os
import sys
from cleverbot_free.cbaio import CleverBot
import signal


#def sigint_handler(signum, frame):
#     message.channel.send('Closing bot')
#     exit()
#
#signal.signal(signal.SIGINT, sigint_handler)

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #channel = client.get_channel(secret)
    #await channel.send('I live')
    chatstarted = False

@client.event
async def on_message(message):
    #print(message.content)
    global chatstarted
    global cb
    if message.author == client.user:
        return
    #if message.content.startswith('<@secret> '):
    if 'secret' in message.content:
        print("bot mentioned")
        if (chatstarted == False):
            await message.channel.send('Error: chat not started')
        else:
            response = message.content.replace('< ', '')
            response = response.replace('>', '')
            response = response.replace('secret', '')
            response.replace('@', '')
            response.replace('&', '')
            response.replace('!', '')
            response = cb.getResponse(response)
            #response = message.content.replace('$bot','')
            await message.channel.send(response)
    if message.content.startswith('$help'):
        await message.channel.send('My functions are: "@Cocona " text / talk to me | $help / this | $resetchat / resets the bot | $endchat / ends the chat | $startchat / starts the chat (do not do while chat is running)')
    if message.content.startswith('$resetbot'):
        await message.channel.send('Resetting...')
        os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
    if message.content.startswith('$startchat'):
        await message.channel.send('Attempting to open chat...')
        if (chatstarted):
            await message.channel.send('Chat is already open!')
        else:
            try:
                cb = CleverBot()
                cb.init()
                await message.channel.send('Opened chat')
                chatstarted = True
            except:
                await message.channel.send('Chat failed to start, try restarting the bot or waiting???')
    if message.content.startswith('$endchat'):
        if (not chatstarted):
            await message.channel.send('Chat is already closed!')
        else:
            cb.close()
            await message.channel.send('Closed chat')
            chatstarted = False
def main():
    global chatstarted
    global cb
    cb = CleverBot()
    chatstarted = False
    client.run("secret")
main()


