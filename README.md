# GitHub Automation Scripts

## 概要
このリポジトリには、GitHubリポジトリに対して自動的にプルリクエストを作成するスクリプトと、過去の活動を記録するコミットを自動的に作成するスクリプトが含まれています。

## ファイル内容
- `github-auto-pr.py`: 新しいブランチを作成し、ファイルを追加してプルリクエストを作成するスクリプト。
- `github-activity-bot.py`: 過去の活動を記録するコミットを自動的に作成するスクリプト。

### github-auto-pr.py
このスクリプトは以下の機能を持っています:
- 新しいブランチを作成
- 新しいブランチにファイルを追加
- プルリクエストを作成

### github-activity-bot.py
このスクリプトは以下の機能を持っています:
- 過去の活動を記録するコミットを作成

## 実行方法
### github-auto-pr.py
1. 必要なパッケージをインストールします。
    ```sh
    pip install PyGithub
    ```
2. スクリプトを実行します。
    ```sh
    python github-auto-pr.py
    ```

### github-activity-bot.py
1. 必要なパッケージをインストールします。
    ```sh
    pip install PyGithub
    ```
2. スクリプトを実行します。
    ```sh
    python github-activity-bot.py
    ```

## 環境変数の設定方法
両方のスクリプトはGitHubトークンを必要とします。以下の手順で環境変数を設定してください。

1. GitHubトークンを取得します。
2. 環境変数 `GITHUB_TOKEN` を設定します。
    - Windows:
        ```sh
        set GITHUB_TOKEN=your_github_token
        ```
    - macOS/Linux:
        ```sh
        export GITHUB_TOKEN=your_github_token
        ```

これでスクリプトを実行する準備が整いました。
