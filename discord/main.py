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
        if (message.author == self.user or  not message.content.startswith("~")):
            return

        contents = message.content.split(" ") # split the message by spaces

        # the first thing iz command
        command = contents[0][1:] # discard the first character
        # errthing else is args
        arguments = " ".join(contents[1:]) # 2nd thing is args

        if (command == "token "):
            params['token'] = arguments
            await message.channel.send(f"Your token is {params['token']}")

        if (command == "provider" ):
            params['provider'] = arguments
            temp = params['provider']
            print(temp)

            valid = ["digitalocean", "google cloud", "amazon web services"]

            if (temp.lower() in valid):
                await message.channel.send(f"Your provider is {temp}")
            else:
                await message.channel.send(f"We do not support this provider yet")


        if (message.content.startswith("~region ")):
            temp = arguments
            params['region'] = temp
            await message.channel.send(f"Your region is {temp}")


client = MyClient()
client.run(SECRET_KEY)
