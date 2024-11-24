import os
import random
from datetime import datetime, timedelta
from github import Github

def create_commit(repo, file_path, commit_message, content, branch="main"):
    try:
        contents = repo.get_contents(file_path, ref=branch)
        repo.update_file(contents.path, commit_message, content, contents.sha, branch=branch)
    except Exception as e:
        print(f"File not found, creating new file: {e}")
        repo.create_file(file_path, commit_message, content, branch=branch)

def main():
    # GitHubトークンを環境変数から取得
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    # GitHubクライアントを初期化
    g = Github(github_token)

    # ユーザー名とリポジトリ名を指定
    username = "USERNAME"
    repo_name = "REPO_NAME"

    try:
        # 対象のリポジトリを取得
        repo = g.get_repo(f"{username}/{repo_name}")
    except Exception as e:
        print(f"Error accessing repository: {e}")
        return

    # コミットを作成する日数（例：過去30日間）
    days = 7

    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        
        # ランダムな回数のコミットを作成（0-5回）
        for _ in range(random.randint(0, 5)):
            commit_message = f"Auto commit on {date.strftime('%Y-%m-%d')}"
            file_path = "activity.txt"
            
            try:
                # 既存のファイルの内容を取得
                try:
                    contents = repo.get_contents(file_path, ref="main")
                    file_content = contents.decoded_content.decode("utf-8")
                except:
                    file_content = ""

                # 新しいログエントリを作成
                new_log_entry = f"Activity logged on {date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                # 既存の内容の先頭に新しいログを追加
                updated_content = new_log_entry + file_content

                create_commit(repo, file_path, commit_message, updated_content)
                print(f"Commit created: {commit_message}")
            except Exception as e:
                print(f"Error creating commit: {e}")

if __name__ == "__main__":
    main()