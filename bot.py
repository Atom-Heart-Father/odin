from dotenv import dotenv_values
from main import father

config = dotenv_values(".env")

import json
import discord

# SECRET_KEY = os.getenv("TOKEN")
SECRET_KEY = config["TOKEN"]

params = None
countries = None

with open("./../../params.json", "r") as read_file:
    params = json.load(read_file)

with open("./../../countries.json", "r") as read_file:
    countries = json.load(read_file)["countries"]


async def make_child():
    details = {
        "os": params["OS"],
        "name": params["name"],
        "memory": params["RAM"],
        "region": params["region"],
        "processor": params["CPUs"],
    }

    if await father(details):
        return True
    else:
        return False



class MyClient(discord.Client):

    help_message = """```To get started, enter  ‘~create <InstanceName>’.
Certain necessary questions pop up which will help set up the necessary VM.
To stop the process at any stage please enter ‘~cancel’.
Follow the instructions prompted by the bot to finish the set-up.```"""

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

    OS_string = "\n1. Fedora\n2. Ubuntu 16"

    async def find(self, queries, string):
        for q in queries:
            if q in string:
                return True
        return False

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def send_error(self, message):
        await message.channel.send("Sorry couldn't get that, please try again")

    async def handle_provider(self, message):
        success = False
        if (await self.find(["google", "gcp", "3"], message.content.lower())):
                params["provider"] = "Google Cloud Platform"
                success = True

        elif (await self.find(["amazon", "web", "services", "aws", "2"], message.content.lower())):
            params["provider"] = "AWS"
            success = True

        elif (await self.find(["digital", "ocean", "1"], message.content.lower())):
            params["provider"] = "DigitalOcean"
            success = True

        if success:
            await message.channel.send(f"You have selected {params['provider']} as your provider")
            self.current_prompt = 1
            await message.channel.send("Where would your VM like to live?" + self.regions_string)
            return True

        return False

    async def handle_region(self, message):
        success = False
        if (await self.find(["us", "states", "unitedstates", "united states", "america", "1"], message.content.lower())):
            params["region"] = "nyc3"
            success = True
            await message.channel.send("Thing will be made at NYC-3")

        elif (await self.find(["uk", "kingdom", "unitedkingdom", "united kingdom", "england", "britian", "2"], message.content.lower())):
            params["region"] = "lon1"
            success = True
            await message.channel.send("Thing will be made at LON-1")

        elif (await self.find(["india", "in", "bharat", "3"], message.content.lower())):
            params["region"] = "blr1"
            success = True
            await message.channel.send("Thing will be made at BLR-1")

        if success:
            await message.channel.send(f"You have selected {params['region']} as your region")
            self.current_prompt = 2
            await message.channel.send("What OS would you like to use" + self.OS_string)
            return True

    async def handle_os(self, message):
        success = False
        if (await self.find(["ubuntu", "2"], message.content.lower())):
                params["OS"] = "ubuntu-16-04-x64"
                success = True

        elif (await self.find(["fedora", "1"], message.content.lower())):
            params["OS"] = "fedora-34-x64"
            success = True

        if success:
            await message.channel.send(f"You have selected {params['OS']} as your operating system")
            self.current_prompt = 3
            await message.channel.send("How many CPUs would you like to use?")
            return True

        return False

    async def handle_cpu(self, message):
        success = False

        try:
            number = int(message.content.lower()[1:])
            if 0 < number <= 64 and  (number & (number-1) == 0):
                params["CPUs"] = number
                success = True
            else:
                await message.channel.send("The number of CPUs should be between 1 and 64 and should be a power of 2")
                return 69
        except:
            await message.channel.send("Couldn't parse the number of CPUs, are you sure you entered a number (eg: ~55)")
            return 70
        if success:
            await message.channel.send(f"You have selected {params['CPUs']} CPU cores for your VM, seems like you have a lot of money")
            self.current_prompt = 4
            await message.channel.send("How much RAM would you like? (in GBs)")
            return True

        return False

    async def handle_ram(self, message):
        success = False

        try:
            number = int(message.content.lower()[1:])
            if 0 < number <= 128:
                params["RAM"] = number
                success = True
            else:
                await message.channel.send("The storage should be between 10 and 128")
                return 69
        except:
            await message.channel.send("Couldn't parse the amount of RAM, are you sure you entered a number (eg: ~55)")
            return 70
        if success:
            await message.channel.send(f"You have selected {params['RAM']} GB(s) of RAM")
            self.current_prompt = 5
            await message.channel.send("How much storage would you like? (in GBs)")
            return True

        return False

    async def handle_storage(self, message):
        success = False

        try:
            number = int(message.content.lower()[1:])
            if 9 < number <= 1000:
                params["Storage"] = number
                success = True
            else:
                await message.channel.send("The storage should be between 10 and 1000")
                return 69
        except:
            await message.channel.send("Couldn't parse the amount of storage, are you sure you entered a number (eg: ~55)")
            return 70
        if success:
            await message.channel.send(f"You have selected {params['Storage']} GBs of storage")
            self.current_prompt = 6
            await message.channel.send(f"Looks like things are done! Have a cup of coffee, your VM, {params['name']},  will be ready in about a minute!")
            self.mode = 0
            if await make_child():
                return True
            else:
                await message.channel.send("Sorry an error occured")
                return False

        return False

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
                await self.send_error(message)
            return

        elif self.current_prompt == 1:
            if not await self.handle_region(message):
                await self.send_error(message)
            return

        elif self.current_prompt == 2:
            if not await self.handle_os(message):
                await self.send_error(message)
            return
        elif self.current_prompt == 3:
            if not await self.handle_cpu(message):
                await self.send_error(message)
            return

        elif self.current_prompt == 4:
            if not await self.handle_ram(message):
                await self.send_error(message)
            return

        elif self.current_prompt == 5:
            if not await self.handle_storage(message):
                await self.send_error(message)
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
            await message.channel.send(self.help_message)
            return

        if (command == 'create'):
            params["name"] = contents[1]
            self.mode = 1
            await message.channel.send("You will now be prompted with questions to select the specs for " + params["name"])
            await message.channel.send("Send ~cancel to cancel your subscription to NORD VPN")
            await message.channel.send("Remember to prefix your replies with ~")
            await message.channel.send("Please select one of the following providers:\n1. DigitalOcean\n2. AWS\n3. GoogleCloudPlatform")
            self.current_prompt = 0

client = MyClient()
client.run(SECRET_KEY)
