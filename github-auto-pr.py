from github import Github
import os
from datetime import datetime

def create_pull_request(repo, title, body, head, base):
    try:
        pull_request = repo.create_pull(title=title, body=body, head=head, base=base)
        print(f"Pull request created: {pull_request.html_url}")
    except Exception as e:
        print(f"Error creating pull request: {e}")

def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    g = Github(github_token)
    repo = g.get_repo("USERNAME/REPO_NAME")

    # 現在の日時を使用してユニークなブランチ名を生成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    target_branch = f"new-feature-branch-{timestamp}"

    source_branch = "main"
    sb = repo.get_branch(source_branch)

    try:
        # 新しいブランチを作成
        repo.create_git_ref(ref=f"refs/heads/{target_branch}", sha=sb.commit.sha)
        print(f"Created new branch: {target_branch}")

        # 新しいブランチにファイルを追加
        file_content = f"This is a new file created for the pull request at {timestamp}."
        repo.create_file(f"new_file{timestamp}.txt", f"Add new file at {timestamp}", file_content, branch=target_branch)
        print("Added new file to the branch")

        # プルリクエストを作成
        title = f"New Feature Addition - {timestamp}"
        body = f"This pull request adds a new feature to the project. Created at {timestamp}."
        create_pull_request(repo, title, body, target_branch, "main")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
