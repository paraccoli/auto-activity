# GitHub Automation Scripts

## 概要
このリポジトリには、GitHubリポジトリに対して自動的にプルリクエストを作成し、自動マージ・クローズするスクリプトと、過去の活動を記録するコミットを自動的に作成するスクリプトが含まれています。

## ファイル内容
- `github-auto-pr.py`: 新しいブランチを作成し、ファイルを追加してプルリクエストを作成、自動マージ・クローズするスクリプト。
- `github-activity-bot.py`: 過去の活動を記録するコミットを自動的に作成するスクリプト。
- `run-activity-bot.sh`: activity botを実行するためのシェルスクリプト
- `run-auto-pr.sh`: auto PRを実行するためのシェルスクリプト
- `ecosystem.config.js`: PM2による自動実行設定

## 機能詳細

### github-auto-pr.py
このスクリプトは以下の機能を持っています:
- イシューを自動作成
- 新しいブランチを作成
- 新しいブランチにファイルを追加
- プルリクエストを作成（イシューと関連付け）
- **プルリクエストを自動マージ**
- **イシューを自動クローズ**
- **作業ブランチを自動削除**

### github-activity-bot.py
このスクリプトは以下の機能を持っています:
- 過去の活動を記録するコミットを作成
- activity.txtファイルを最新の日付で更新

## PM2による自動実行設定
- `github-activity-bot`: 毎日9時に実行
- `github-auto-pr`: 毎週月曜日10時に実行

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

### 3. PM2での起動
```bash
pm2 start ecosystem.config.js
pm2 save
```

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
```

### PM2での管理
```bash
# 状態確認
pm2 status

# ログ確認
pm2 logs github-activity-bot
pm2 logs github-auto-pr

# 停止
pm2 stop all

# 再起動
pm2 restart all
```

## 注意事項
- GitHub Personal Access Tokenには以下の権限が必要です：
  - `repo` (フルアクセス)
  - `write:packages` (パッケージ書き込み)
- 自動マージ機能により、作成されたプルリクエストは即座にマージされます
- 作業用ブランチは自動的に削除されます