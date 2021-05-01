from logging import error
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

async def make_child():
    details = {
        "os": params["OS"],
        "name": params["name"],
        "region": params["region"],
    }

    if params["Package"] == 1:
        details["memory"] = "1"
        details["processor"] = "1"
    elif params["Package"] == 2:
        details["memory"] = "2"
        details["processor"] = "1"
    elif params["Package"] == 3:
        details["memory"] = "2"
        details["processor"] = "2"
    elif params["Package"] == 4:
        details["memory"] = "4"
        details["processor"] = "2"
    elif params["Package"] == 5:
        details["memory"] = "8"
        details["processor"] = "4"

    if await father(details):
        return True
    else:
        return False
    print(details)

class MyClient(discord.Client):

    help_message = """```To get started, enter  ‘~create <InstanceName>’.
Certain necessary questions pop up which will help set up the necessary VM.
To stop the process at any stage please enter ‘~cancel’.
Follow the instructions prompted by the bot to finish the set-up.```"""

    # 0 is normal mode
    # 1 is create mode
    # in create mode, the bot starts interrogating you
    mode = 0

    regions_string = "\n1. USA\n2. UK\n3. IN"
    current_prompt = -1

    OS_string = "\n1. Fedora\n2. Ubuntu 16"

    packages_list = [
        "1. 1 CPU, 1 GB RAM, 25 GB SSD",
        "2. 1 CPU, 2GB RAM, 50GB SSD",
        "3. 2 CPU, 2GB RAM, 60GB SSD",
        "4. 2 CPU, 4GB RAM, 80GB SSD",
        "5. 4 CPU, 8GB RAM, 160GB SSD"
    ]

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

        elif (await self.find(["uk", "kingdom", "unitedkingdom", "united kingdom", "england", "britian", "2"], message.content.lower())):
            params["region"] = "lon1"
            success = True

        elif (await self.find(["india", "in", "bharat", "3"], message.content.lower())):
            params["region"] = "blr1"
            success = True

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
            await message.channel.send("What package would you like to use?\n" + "\n".join(self.packages_list))
            return True

        return False


    async def handle_package(self, message):
        success = False

        try:
            number = int(message.content.lower()[1:])
            if 0 < number <= 5:
                success = True
            else:
                await message.channel.send("Invalid package selected")
                return 69
        except:
            await message.channel.send("Couldn't parse the package number, are you sure you entered a number (eg: ~55)")
            return 70
        if success:
            params["Package"] = number
            await message.channel.send(f"You have selected package {self.packages_list[number-1]}, seems like you have a lot of money")
            self.current_prompt = 4
            await message.channel.send(f"Looks like things are done! Have a cup of coffee, your VM, {params['name']},  will be ready in about a minute!")
            self.mode = 0
            if await make_child():
                return True
            else:
                await message.channel.send("Sorry an error occured")
                return 60

        return False

    async def create_mode(self, message):
        if message.content == "~cancel":
            await message.channel.send("All settings have been discarded, returning to normal mode")
            self.mode = 0
            return

        if message.content.startswith("~create "):
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
            if not await self.handle_package(message):
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

        if (command == 'cancel'):
            await message.channel.send("Too late!")
            return

        if (command != 'create'):
            await message.channel.send(self.help_message)
            return

        if (command == 'create'):
            try:
                params["name"] = contents[1]
            except:
                params["name"] = "myVM"

            self.mode = 1
            first_message = f"""You will now be prompted with questions to select the specs for {params['name']}
Send ~cancel to stop anytime and discard the changes
Remember to prefix your replies with ~
Please select one of the following providers:\n1. DigitalOcean\n2. AWS\n3. GoogleCloudPlatform"""

            await message.channel.send(first_message)
            self.current_prompt = 0

client = MyClient()
client.run(SECRET_KEY)
