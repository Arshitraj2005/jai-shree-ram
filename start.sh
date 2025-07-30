#!/bin/bash

# 🌐 Start Flask uptime thread
python3 main.py &

# 📡 Start streaming
python3 stream.py
