terraform {
  required_version = "~>1.0.0"

  #  backend "s3" {
  #    bucket                  = "apmechev-tfm-remote-state"
  #    region                  = "eu-central-1"
  #    key                     = "cakedays.tfstate"
  #    encrypt                 = "true"
  #    shared_credentials_file = "~/.aws/credentials"
  #    profile                 = "ci-glbl-auto"
  #  }

  required_providers {
    archive = {
      source = "hashicorp/archive"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.44.0"
    }
    external = {
      source = "hashicorp/external"
    }
    null = {
      source = "hashicorp/null"
    }
    template = {
      source = "hashicorp/template"
    }
  }
}


provider "aws" {
  region                  = var.region
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "cakedays"
}