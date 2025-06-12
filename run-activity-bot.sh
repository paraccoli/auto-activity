#!/bin/bash

# 環境変数を読み込み
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# 仮想環境をアクティベート（存在する場合）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Pythonスクリプトを実行
python3 github-activity-bot.py

# 仮想環境を非アクティベート（アクティベートしていた場合）
if [ -d "venv" ]; then
    deactivate
fi
