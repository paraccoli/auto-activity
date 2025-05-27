from github import Github
import os
from datetime import datetime
import time

def create_issue(repo, title, body):
    try:
        issue = repo.create_issue(title=title, body=body)
        print(f"Issue created: {issue.html_url}")
        return issue
    except Exception as e:
        print(f"Error creating issue: {e}")
        return None

def close_issue(repo, issue_number, close_comment="自動クローズ: 関連するプルリクエストがマージされました。"):
    try:
        issue = repo.get_issue(issue_number)
        issue.create_comment(close_comment)
        issue.edit(state='closed')
        print(f"Issue #{issue_number} closed successfully")
    except Exception as e:
        print(f"Error closing issue #{issue_number}: {e}")

def create_pull_request(repo, title, body, head, base):
    try:
        pull_request = repo.create_pull(title=title, body=body, head=head, base=base)
        print(f"Pull request created: {pull_request.html_url}")
        return pull_request
    except Exception as e:
        print(f"Error creating pull request: {e}")
        return None

def merge_pull_request(repo, pr_number, commit_title="Auto merge", commit_message="プルリクエストを自動マージしました", merge_method="merge"):
    try:
        pull_request = repo.get_pull(pr_number)
        # プルリクエストがマージ可能かチェック
        if pull_request.mergeable:
            merge_result = pull_request.merge(commit_title=commit_title, commit_message=commit_message, merge_method=merge_method)
            if merge_result.merged:
                print(f"Pull request #{pr_number} merged successfully")
                return True
            else:
                print(f"Failed to merge pull request #{pr_number}")
                return False
        else:
            print(f"Pull request #{pr_number} is not mergeable")
            return False
    except Exception as e:
        print(f"Error merging pull request #{pr_number}: {e}")
        return False

def delete_branch(repo, branch_name):
    try:
        ref = repo.get_git_ref(f"heads/{branch_name}")
        ref.delete()
        print(f"Branch {branch_name} deleted successfully")
    except Exception as e:
        print(f"Error deleting branch {branch_name}: {e}")

def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    github_username = os.environ.get("GITHUB_USERNAME")
    github_repo = os.environ.get("GITHUB_REPO")
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    if not github_username:
        raise ValueError("GITHUB_USERNAME environment variable not set")
    if not github_repo:
        raise ValueError("GITHUB_REPO environment variable not set")

    g = Github(github_token)
    repo = g.get_repo(f"{github_username}/{github_repo}")

    # 現在の日時を使用してユニークなブランチ名を生成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    target_branch = f"new-feature-branch-{timestamp}"

    source_branch = "main"
    sb = repo.get_branch(source_branch)

    try:
        # イシューを作成
        issue_title = "機能改善タスク"
        issue_body = f"""# 機能改善タスク
このイシューは自動生成されました。

## 概要
- 作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- タスクID: TASK-{timestamp}

## 詳細
リポジトリの定期的なメンテナンスを行います。"""
        
        issue = create_issue(repo, issue_title, issue_body)

        # 新しいブランチを作成
        repo.create_git_ref(ref=f"refs/heads/{target_branch}", sha=sb.commit.sha)
        print(f"Created new branch: {target_branch}")

        # 新しいブランチにファイルを追加
        file_content = f"This is a new file created for the pull request at {timestamp}."
        repo.create_file(f"new_file{timestamp}.txt", f"Add new file at {timestamp}", file_content, branch=target_branch)
        print("Added new file to the branch")

        # プルリクエストを作成（イシューと関連付け）
        pr_title = f"New Feature Addition - {timestamp}"
        pr_body = f"""This pull request adds a new feature to the project. Created at {timestamp}.

Related issue: #{issue.number if issue else 'N/A'}

## 変更内容
- 新しいファイル `new_file{timestamp}.txt` を追加
- 自動生成されたコンテンツを含む

## テスト
- 自動テストは不要（自動生成ファイル）

Closes #{issue.number if issue else 'N/A'}"""
        
        pull_request = create_pull_request(repo, pr_title, pr_body, target_branch, "main")

        if pull_request:
            # 少し待ってからマージ（GitHub APIの同期のため）
            print("Waiting 5 seconds before merging...")
            time.sleep(5)
            
            # プルリクエストを自動マージ
            merge_success = merge_pull_request(
                repo, 
                pull_request.number,
                f"Auto merge: {pr_title}",
                f"自動マージ: {timestamp} に作成されたプルリクエストをマージしました"
            )
            
            if merge_success:
                # ブランチを削除
                delete_branch(repo, target_branch)
                
                # イシューを自動クローズ（プルリクエストのマージ後）
                if issue:
                    close_issue(repo, issue.number, f"自動クローズ: プルリクエスト #{pull_request.number} がマージされました。")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
