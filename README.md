# Odin

ChatOps bot for fully automated Cloud Infrastructure deployments using Terraform, the popular IaC (Infrastructure as Code) tool.

## Features

- Deploy Cloud Infrastructure on the fly, using a simple chat interface. Sessions are isolated and stored securely in the Zulip (maybe Slack) bot storage. 

- Natural Language Processing: Understands natural human language.

- Abstract away complex terms involved with deploying infra, asks simple questions about the configuration.

- Completely automated deployments using Terraform. Rolls back all changes if errors occured. Verbose and crystal-clear error messages.

- Supports over 100 cloud providers! Just add a terraform config and you're good to go. Sample configs for a few major providers will be available.
