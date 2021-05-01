variable "name" {
    description = "Name of Instance"
}

variable "region" {
    description = "Region where to deploy resources to"
}

variable "access_key" {
    description = "Access key for AWS service account"
    default = ""
}

variable "secret_key" {
  description = "Secret key for AWS service account"
  default = ""
}

data "aws_ami" "image" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

provider "aws" {
    region = var.region
    access_key = var.access_key
    secret_key = var.secret_key
}

resource "aws_instance" "app_server" {
  ami = data.aws_ami.image.id
  instance_type = "t2.micro"

  tags = {
    Name = var.name
  }
}