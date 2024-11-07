# Use Ubuntu Base Image
FROM ubuntu:20.04

# Set environment variables to prevent timezone prompt
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip

RUN apt update && apt install -y git

RUN pip install mfem