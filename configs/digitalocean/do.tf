terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 1.0"
    }
  }
}

variable "do_token" {
    description = "DigitalOcean API Token"
    default = "f0270deb9068cbc836ba3280418743bce416ece6f693e189c762baf42a3c2fff"
}

variable "name" {
    description = "Name of the droplet to create"
}
variable "region" {
    description = "Datacenter region to create the droplet in"
}
variable "size" {
    description = "Specs for the droplet to create"
}

variable "image" {
  description = "OS Image to use for setting up droplet"
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "droplet" {
  image = var.image
  name   = var.name
  region = var.region
  size = var.size
}
