#!/bin/bash

# Update and install ffmpeg
sudo apt update
sudo apt install -y ffmpeg

# Start Flask with Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
