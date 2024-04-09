# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /opt/lava_field_penetrometer

# Update packages, install python and git
RUN apt update && apt -y upgrade && apt install -y git sudo
