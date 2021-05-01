# Odin

ChatOps bot for fully automated Cloud Infrastructure deployments using Terraform, the popular IaC (Infrastructure as Code) tool.

## About

This pandemic has forced a change in the usual environment one would work in. It is evident that there is major lack of resources and to compensate for the situation, many companies have been forced to issue laptops and other essentials to create a working environment for the employees at comfort of their home. Some companies do not have the resources to avail each and every employee, adequate tools to create an efficient workspace resulting in them losing their jobs.
<br>
Even for major companies, there is a large strain on the IT department of companies, and also on the employees themselves to get accustomed to the new working environment, especially those in critical departments such as Operations, who need a machine to deploy these cloud resources from.
<br>
We found a solution which helps solve this problem entirely. It deploys cloud infrastructure simply with the help of a chat on a mobile phone. We are using Zulip as the chat platform making things even easier for employees, as it integrates it directly into their corporate workspace. The IT team can place restrictions on who can communicate with the bot using Zulip's built-in features.
<br>
The bot uses DialogFlow and processes natural language which makes it very simple for people to communicate with the bot. It proves to be secure, as the bot requires the user to give necessary details for it to work.
<br>
The deployment is generated using Terraform. It is a popular IaaC tool used commonly. It is quite efficient in preventing faulty deployments and gives an added advantage of integrating over 131 cloud providers, which includes providers with major market share, as well as several other smaller providers. Adding a provider is as simple as plug-and-play and this way it helps in aiding employees and companies to get an efficient workspace set in their homes.

## Features

- Deploy Cloud Infrastructure on the fly, using a simple chat interface. Sessions are isolated and stored securely in the Zulip (maybe Slack) bot storage. 

- Natural Language Processing: Understands natural human language.

- Abstract away complex terms involved with deploying infra, asks simple questions about the configuration.

- Completely automated deployments using Terraform. Rolls back all changes if errors occured. Verbose and crystal-clear error messages.

- Supports over 100 cloud providers! Just add a terraform config and you're good to go. Sample configs for a few major providers will be available.
