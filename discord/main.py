import os
import discord

SECRET_KEY = os.getenv("TOKEN")
print(SECRET_KEY)

params = {
    'token': '',
    'provider': '',
    'region': ''
}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):

        if (message.author == self.user):
            return

        # await message.channel.send('Message from {0.author}: {0.content}'.format(message))

        if (message.content.startswith("~token ")):
            temp = message.content[7:]
            params['token'] = temp
            await message.channel.send('Your token is {0}'.format(temp))

        if (message.content.startswith("~provider ")):
            temp = message.content[10:]
            if temp != "DigitalOcean" or temp != "Google Cloud" or temp != "Amazon Web Services":
                await message.channel.send("Please choose DigitalOcean or Google Cloud or Amazon Web Services")
            else:
                params['provider'] = temp
                await message.channel.send('Your provider is {0}'.format(temp))

        if (message.content.startswith("~region ")):
            temp = message.content[8:]
            params['region'] = temp
            await message.channel.send('Your region is {0}'.format(temp))


client = MyClient()
client.run(SECRET_KEY)
