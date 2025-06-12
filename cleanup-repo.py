#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from github import Github
import os
import re
from datetime import datetime

def cleanup_repository_files(repo):
    """
    リポジトリから不要なファイルを削除する
    - new_file*.txt ファイル
    - maintenance フォルダ
    """
    try:
        contents = repo.get_contents("")
        files_to_delete = []
        
        for content in contents:
            # new_file*.txt パターンのファイルを削除対象に追加
            if content.type == "file" and re.match(r'^new_file\d+\.txt$', content.name):
                files_to_delete.append(content)
                print(f"Found file to delete: {content.name}")
            
            # maintenance フォルダを削除対象に追加
            elif content.type == "dir" and content.name == "maintenance":
                # maintenance フォルダ内のファイルも取得
                maintenance_contents = repo.get_contents(content.path)
                for maintenance_file in maintenance_contents:
                    files_to_delete.append(maintenance_file)
                    print(f"Found maintenance file to delete: {maintenance_file.path}")
                files_to_delete.append(content)
                print(f"Found maintenance folder to delete: {content.name}")
        
        if not files_to_delete:
            print("No files to delete found.")
            return
        
        # 削除を実行
        for file_content in files_to_delete:
            try:
                if file_content.type == "file":
                    repo.delete_file(
                        file_content.path,
                        f"Cleanup: Remove {file_content.name}",
                        file_content.sha
                    )
                    print(f"Deleted file: {file_content.path}")
            except Exception as e:
                print(f"Error deleting {file_content.path}: {e}")
                
    except Exception as e:
        print(f"Error during cleanup: {e}")

def main():
    # 環境変数を取得
    github_token = os.environ.get("GITHUB_TOKEN")
    github_username = os.environ.get("GITHUB_USERNAME")
    github_repo = os.environ.get("GITHUB_REPO")
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    if not github_username:
        raise ValueError("GITHUB_USERNAME environment variable not set")
    if not github_repo:
        raise ValueError("GITHUB_REPO environment variable not set")

    # GitHubクライアントを初期化
    g = Github(github_token)
    
    try:
        repo = g.get_repo(f"{github_username}/{github_repo}")
        print(f"Starting cleanup for repository: {github_username}/{github_repo}")
        cleanup_repository_files(repo)
        print("Cleanup completed successfully!")
        
    except Exception as e:
        print(f"Error accessing repository: {e}")

if __name__ == "__main__":
    main()
