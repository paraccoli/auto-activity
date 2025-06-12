# GitHub Automation Scripts

## 概要
このリポジトリには、GitHubリポジトリに対して自動的にプルリクエストを作成し、自動マージ・クローズするスクリプトと、過去の活動を記録するコミットを自動的に作成するスクリプトが含まれています。

## ファイル内容
- `github-auto-pr.py`: 新しいブランチを作成し、activity.txtを更新してプルリクエストを作成、自動マージ・クローズするスクリプト。
- `github-activity-bot.py`: 過去の活動を記録するコミットを自動的に作成するスクリプト。
- `cleanup-repo.py`: 不要なファイル（new_file*.txt、maintenanceフォルダ）をクリーンアップするスクリプト。
- `run-activity-bot.sh`: activity botを実行するためのシェルスクリプト
- `run-auto-pr.sh`: auto PRを実行するためのシェルスクリプト
- `run-cleanup.sh`: リポジトリクリーンアップを実行するためのシェルスクリプト
- `ecosystem.config.js`: PM2による自動実行設定
- `github-activity-bot.service`: systemd用activity botサービスファイル
- `github-auto-pr.service`: systemd用auto PRサービスファイル
- `github-activity-bot.timer`: systemd用activity botタイマーファイル
- `github-auto-pr.timer`: systemd用auto PRタイマーファイル
- `setup-systemd.sh`: systemd自動起動設定スクリプト

## 機能詳細

### github-auto-pr.py
このスクリプトは以下の機能を持っています:
- イシューを自動作成
- 新しいブランチを作成
- **activity.txtファイルを更新（新しいファイルは作成しない）**
- プルリクエストを作成（イシューと関連付け）
- **プルリクエストを自動マージ（状態チェック機能付き）**
- **イシューを自動クローズ**
- **作業ブランチを自動削除**

### github-activity-bot.py
このスクリプトは以下の機能を持っています:
- 過去の活動を記録するコミットを作成
- activity.txtファイルを最新の日付で更新

### cleanup-repo.py
このスクリプトは以下の機能を持っています:
- **不要なnew_file*.txtファイルを自動削除**
- **maintenanceフォルダとその中身を自動削除**
- リポジトリの整理とクリーンアップ

## systemdによる自動実行設定
- `github-activity-bot.timer`: 毎日実行（ランダム遅延あり）
- `github-auto-pr.timer`: 毎週実行（ランダム遅延あり）

## セットアップ手順

### 1. 仮想環境の作成
```bash
cd /home/paraccoli/apps/auto-activity
python3 -m venv venv
source venv/bin/activate
pip install PyGithub
deactivate
```

### 2. 実行権限の付与
```bash
chmod +x run-activity-bot.sh
chmod +x run-auto-pr.sh
```

### 3. systemdでの自動起動設定
```bash
# セットアップスクリプトに実行権限を付与
chmod +x setup-systemd.sh

# 自動セットアップを実行
./setup-systemd.sh
```

このスクリプトは以下の処理を自動で行います：
- GitHubの認証情報を入力プロンプトで取得
- サービスファイルを適切な場所にコピー・設定
- systemdサービスとタイマーの有効化
- タイマーの開始

## 環境変数の設定方法
両方のスクリプトはGitHubトークンを必要とします。`.env`ファイルに以下の形式で設定してください：

```
GITHUB_TOKEN=your_github_token_here
```

## 実行方法

### 手動実行
```bash
# Activity botの実行
./run-activity-bot.sh

# Auto PR botの実行
./run-auto-pr.sh

# リポジトリクリーンアップの実行
./run-cleanup.sh
```

### systemdでの管理
```bash
# タイマー状態確認
sudo systemctl status github-activity-bot.timer
sudo systemctl status github-auto-pr.timer

# 次回実行予定確認
sudo systemctl list-timers github-*

# ログ確認
sudo journalctl -u github-activity-bot.service
sudo journalctl -u github-auto-pr.service

# タイマー停止
sudo systemctl stop github-activity-bot.timer
sudo systemctl stop github-auto-pr.timer

# タイマー開始
sudo systemctl start github-activity-bot.timer
sudo systemctl start github-auto-pr.timer

# 手動実行
sudo systemctl start github-activity-bot.service
sudo systemctl start github-auto-pr.service

# サービス無効化（自動起動停止）
sudo systemctl disable github-activity-bot.timer
sudo systemctl disable github-auto-pr.timer
```

## 注意事項
- GitHub Personal Access Tokenには以下の権限が必要です：
  - `repo` (フルアクセス)
  - `write:packages` (パッケージ書き込み)
- 自動マージ機能により、作成されたプルリクエストは即座にマージされます
- 作業用ブランチは自動的に削除されます