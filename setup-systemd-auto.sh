#!/bin/bash
# GitHub Automation Systemd Setup Script (Auto mode with .env)

set -e

echo "GitHub Automation Scripts - Systemd Setup"
echo "=========================================="

# 変数設定
SERVICE_USER=$(whoami)
SCRIPT_DIR=$(pwd)
SERVICE_DIR="/etc/systemd/system"

# .envファイルから認証情報を読み込み
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file with GITHUB_TOKEN, GITHUB_USERNAME, and GITHUB_REPO"
    exit 1
fi

# .envファイルをソース
source .env

# 必要な変数が設定されているかチェック
if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_USERNAME" ] || [ -z "$GITHUB_REPO" ]; then
    echo "Error: Missing required environment variables in .env file"
    echo "Required: GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO"
    exit 1
fi

echo "Using GitHub credentials from .env file:"
echo "Username: $GITHUB_USERNAME"
echo "Repository: $GITHUB_REPO"
echo "Token: ${GITHUB_TOKEN:0:10}..."

# サービスファイルをコピーして設定を更新
echo "Setting up service files..."

# Activity Bot Service
sudo cp github-activity-bot.service ${SERVICE_DIR}/
sudo sed -i "s|your_username|${SERVICE_USER}|g" ${SERVICE_DIR}/github-activity-bot.service
sudo sed -i "s|/home/your_username/apps/auto-activity|${SCRIPT_DIR}|g" ${SERVICE_DIR}/github-activity-bot.service
sudo sed -i "s|your_github_token_here|${GITHUB_TOKEN}|g" ${SERVICE_DIR}/github-activity-bot.service
sudo sed -i "s|your_github_username|${GITHUB_USERNAME}|g" ${SERVICE_DIR}/github-activity-bot.service
sudo sed -i "s|your_repo_name|${GITHUB_REPO}|g" ${SERVICE_DIR}/github-activity-bot.service

# Auto PR Service
sudo cp github-auto-pr.service ${SERVICE_DIR}/
sudo sed -i "s|your_username|${SERVICE_USER}|g" ${SERVICE_DIR}/github-auto-pr.service
sudo sed -i "s|/home/your_username/apps/auto-activity|${SCRIPT_DIR}|g" ${SERVICE_DIR}/github-auto-pr.service
sudo sed -i "s|your_github_token_here|${GITHUB_TOKEN}|g" ${SERVICE_DIR}/github-auto-pr.service
sudo sed -i "s|your_github_username|${GITHUB_USERNAME}|g" ${SERVICE_DIR}/github-auto-pr.service
sudo sed -i "s|your_repo_name|${GITHUB_REPO}|g" ${SERVICE_DIR}/github-auto-pr.service

# Timer files
sudo cp github-activity-bot.timer ${SERVICE_DIR}/
sudo cp github-auto-pr.timer ${SERVICE_DIR}/

# systemdを再読み込み
echo "Reloading systemd..."
sudo systemctl daemon-reload

# サービスを有効化
echo "Enabling services..."
sudo systemctl enable github-activity-bot.service
sudo systemctl enable github-auto-pr.service
sudo systemctl enable github-activity-bot.timer
sudo systemctl enable github-auto-pr.timer

# タイマーを開始
echo "Starting timers..."
sudo systemctl start github-activity-bot.timer
sudo systemctl start github-auto-pr.timer

echo ""
echo "Setup completed successfully!"
echo ""
echo "Service status:"
sudo systemctl status github-activity-bot.timer --no-pager -l
sudo systemctl status github-auto-pr.timer --no-pager -l

echo ""
echo "Next scheduled runs:"
sudo systemctl list-timers github-*

echo ""
echo "Useful commands:"
echo "  sudo systemctl status github-activity-bot.timer"
echo "  sudo systemctl status github-auto-pr.timer" 
echo "  sudo journalctl -u github-activity-bot.service"
echo "  sudo journalctl -u github-auto-pr.service"
echo "  sudo systemctl stop github-activity-bot.timer"
echo "  sudo systemctl stop github-auto-pr.timer"
