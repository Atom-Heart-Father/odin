import os

from dotenv import dotenv_values

config = dotenv_values(".env")

print(config)
import json
import discord

# SECRET_KEY = os.getenv("TOKEN")
SECRET_KEY = config["TOKEN"]

params = None
countries = None

with open("params.json", "r") as read_file:
    params = json.load(read_file)

with open("countries.json", "r") as read_file:
    countries = json.load(read_file)["countries"]

class MyClient(discord.Client):

    # 0 is normal mode
    # 1 is create mode
    # in create mode, the bot starts interrogating you
    mode = 0

    create_commands = [
        "provider",
        "region",
        "os",
        "cpu",
        "ram",
        "storage",
        "token"
    ]

    regions_string = "\n1. USA\n2. UK\n3. IN"
    current_prompt = -1

    async def find(self, queries, string):
        for q in queries:
            if q in string:
                return True

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def handle_provider(self, message):
        success = False
        if (await self.find(["google", "gcp", "3"], message.content.lower())):
                params["provider"] = "Google Cloud Platform"
                success = True

        if (await self.find(["amazon", "web", "services", "aws", "2"], message.content.lower())):
            params["provider"] = "AWS"
            success = True

        if (await self.find(["digital", "ocean", "1"], message.content.lower())):
            params["provider"] = "DigitalOcean"
            success = True

        if success:
            await message.channel.send(f"You have selected {params['provider']} as your provider")
            current_prompt = 1
            await message.channel.send("Where would your VM like to live?" + self.regions_string)
            return True

        return False

    async def handle_regions(self, message):
        ...

    async def create_mode(self, message):
        if message.content == "~cancel":
            await message.channel.send("All settings have been discarded, returning to normal mode")
            self.mode = 0
            return

        if message.content == "~create":
            await message.channel.send("You are already in create mode")
            return

        if self.current_prompt == 0:
            if not await self.handle_provider(message):
                await message.channel.send("Sorry couldn't understand that, please try again")
            return

        if self.current_prompt == 1:
            if not self.handle_provider(message):
                await message.channel.send("Sorry couldn't understand that, please try again")
            return



    async def on_message(self, message):
        if (message.author == self.user or not message.content.startswith("~")):
            return

        contents = message.content.split(" ")  # split the message by spaces

        # the first thing iz command
        command = contents[0][1:]  # discard the first character
        if self.mode == 1:
            await self.create_mode(message)
            return

        if (command in self.create_commands):
            await message.channel.send("You need to switch to create mode. Try typing in ~create")
            return

        if (command != 'create'):
            await message.channel.send("Help is on its way")
            return

        if (command == 'create'):
            self.mode = 1
            await message.channel.send("You will now be prompted with questions to select the specs for yo vm")
            await message.channel.send("Send ~cancel to cancel your subscription to NORD VPN")
            await message.channel.send("Remember to prefix your replies with ~")
            await message.channel.send("Please select one of the following providers:\n1. DigitalOcean\n2. AWS\n3. GoogleCloudPlatform")
            self.current_prompt = 0


client = MyClient()
client.run(SECRET_KEY)
