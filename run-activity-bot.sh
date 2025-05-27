#!/bin/bash
cd /home/paraccoli/apps/auto-activity
source venv/bin/activate
source .env
export GITHUB_TOKEN
export GITHUB_USERNAME
export GITHUB_REPO
python3 github-activity-bot.py
deactivate