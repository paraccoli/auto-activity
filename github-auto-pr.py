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
        
        # PRの状態を待つ（最大30秒）
        max_attempts = 6
        for attempt in range(max_attempts):
            # PRの情報を再取得
            pull_request = repo.get_pull(pr_number)
            print(f"Attempt {attempt + 1}: PR state={pull_request.state}, mergeable={pull_request.mergeable}, mergeable_state={pull_request.mergeable_state}")
            
            # PRがクローズされている場合はスキップ
            if pull_request.state == 'closed':
                print(f"Pull request #{pr_number} is already closed")
                return False
            
            # mergeable状態をチェック
            if pull_request.mergeable is True:
                break
            elif pull_request.mergeable is False:
                print(f"Pull request #{pr_number} has merge conflicts")
                return False
            else:
                # mergeable状態がまだ決まっていない場合は少し待つ
                if attempt < max_attempts - 1:
                    print(f"Mergeable state not ready, waiting 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Mergeable state could not be determined after {max_attempts} attempts")
                    return False
          # マージを実行
        try:
            # まずデフォルトのmergeを試す
            merge_result = pull_request.merge(commit_title=commit_title, commit_message=commit_message, merge_method=merge_method)
            if merge_result.merged:
                print(f"Pull request #{pr_number} merged successfully with method '{merge_method}'")
                return True
            else:
                print(f"Failed to merge with method '{merge_method}', trying 'squash'...")
                # squash mergeを試す
                merge_result = pull_request.merge(commit_title=commit_title, commit_message=commit_message, merge_method="squash")
                if merge_result.merged:
                    print(f"Pull request #{pr_number} merged successfully with method 'squash'")
                    return True
                else:
                    print(f"Failed to merge pull request #{pr_number} with both methods: {merge_result}")
                    return False
        except Exception as merge_error:
            print(f"Error during merge operation: {merge_error}")
            # Squash mergeを最後の手段として試す
            try:
                print("Trying squash merge as fallback...")
                merge_result = pull_request.merge(commit_title=commit_title, commit_message=commit_message, merge_method="squash")
                if merge_result.merged:
                    print(f"Pull request #{pr_number} merged successfully with fallback squash method")
                    return True
            except Exception as fallback_error:
                print(f"Fallback squash merge also failed: {fallback_error}")
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
        
        issue = create_issue(repo, issue_title, issue_body)        # 新しいブランチを作成
        repo.create_git_ref(ref=f"refs/heads/{target_branch}", sha=sb.commit.sha)
        print(f"Created new branch: {target_branch}")

        # activity.txtファイルを更新（新しいファイルを作成しない）
        file_path = "activity.txt"
        file_content = f"""# Activity Log

Last maintenance: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Task ID: TASK-{timestamp}

## Recent Activities
- Repository maintenance performed at {timestamp}
- Automated pull request workflow executed
- System health check completed

## Status
All systems operational.
"""
        
        try:
            # 既存のファイルを取得して更新
            contents = repo.get_contents(file_path, ref=target_branch)
            repo.update_file(contents.path, f"Update activity log at {timestamp}", file_content, contents.sha, branch=target_branch)
            print("Updated existing activity.txt file")
        except:
            # ファイルが存在しない場合は新規作成
            repo.create_file(file_path, f"Create activity log at {timestamp}", file_content, branch=target_branch)
            print("Created new activity.txt file")        # プルリクエストを作成（イシューと関連付け）
        pr_title = f"Repository Maintenance - {timestamp}"
        pr_body = f"""# Repository Maintenance

This pull request updates the activity log with the latest maintenance information.

**Created at**: {timestamp}  
**Related issue**: #{issue.number if issue else 'N/A'}

## 変更内容
- `activity.txt` ファイルを最新の情報で更新
- リポジトリメンテナンス記録を追加
- システム状態を記録

## テスト
- 自動テストは不要（ログファイル更新のみ）

Closes #{issue.number if issue else 'N/A'}"""
        
        pull_request = create_pull_request(repo, pr_title, pr_body, target_branch, "main")

        if pull_request:
            # GitHub APIでPRの状態が安定するまで待機
            print("Waiting 10 seconds for PR to be ready for merging...")
            time.sleep(10)
            
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
