import os
import discord

SECRET_KEY = os.getenv("TOKEN")
print(SECRET_KEY)

params = {
    'token': '',
    'provider': 'DigitalOcean',
    'region': 'USA',
    'distribution': 'Arch'
}

countries = [
    "us",
    "uk",
    "in"
]

distributions = [
    "ubuntu 16",
    "ubuntu 18",
    "ubuntu 20",
    "fedora 33",
    "fedora 34",
    "winhoes",
]


def handle_dig_ocean():
    params['provider'] = "DigitalOcean"


def handle_provider(provider):
    valid = ["digitalocean", "google cloud", "amazon web services"]
    if (not provider.lower() in valid):
        return False
    if provider == 'DigitalOcean':
        return handle_dig_ocean()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if (message.author == self.user or not message.content.startswith("~")):
            return

        contents = message.content.split(" ")  # split the message by spaces

        # the first thing iz command
        command = contents[0][1:]  # discard the first character
        # errthing else is args
        arguments = " ".join(contents[1:])  # 2nd thing is args

        if (command == "token"):
            params['token'] = arguments
            await message.channel.send(f"Your token is {params['token']}")

        if (command == "region"):
            if arguments.lower() in countries:
                params['region'] = arguments
                await message.channel.send(f"Your region is {params['region']}")
            else:
                question = "Please choose one of these country codes:\n" + "\n".join(countries)
                await message.channel.send(question)

        # if(command == "ram"):


        if (command == "distro"):
            if arguments.lower() in distributions:
                params['distribution'] = arguments
                await message.channel.send(f"Your distro is {params['distribution']}")
            else:
                question = "Please choose one of these distributions:\n" + "\n".join(distributions)
                await message.channel.send(question)
            # await message.channel.send(f"imma distribute yo mamma in tha hood")

        if (command == "provider"):
            if handle_provider(arguments):
                await message.channel.send(f"Your provider is {params['provider']}")
            else:
                await message.channel.send(f"We do not support this provider yet")

        if (command == "default"):
            if (len(arguments) == 0):
                await message.channel.send(f"try again noob")
            else:
                question = "Setting things up default\n"
                for key in params.keys:
                    question = question + "\n" + key + ": " + params[key]
                await message.channel.send(question)


client = MyClient()
client.run(SECRET_KEY)
