# plugins/aria-git-advanced/main.py
import os
import subprocess
import sys

def git_flow(args):
    if len(args) < 1:
        print("Usage: git-flow <feature|bugfix> [name]")
        return
    flow_type = args[0]
    branch_name = args[1] if len(args) > 1 else None
    if flow_type == "feature":
        prefix = "feature/"
    elif flow_type == "bugfix":
        prefix = "bugfix/"
    else:
        print(f"Unknown flow type: {flow_type}")
        return
    if not branch_name:
        branch_name = input("Branch name: ")
    branch = prefix + branch_name
    subprocess.run(["git", "checkout", "-b", branch])

def git_stats():
    # Show quick commit stats
    import datetime
    out = subprocess.check_output(["git", "log", "--oneline"]).decode()
    lines = out.strip().split('\n') if out.strip() else []
    print(f"Total commits: {len(lines)}")
    # author stats
    authors = {}
    for line in lines:
        commit_hash = line.split()[0]
        author = subprocess.check_output(["git", "show", "-s", "--format=%an", commit_hash]).decode().strip()
        authors[author] = authors.get(author, 0) + 1
    print("Commits per author:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        print(f"  {author}: {count}")

def git_blame_ai():
    file = input("File to blame: ")
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return
    # This would call AI, but for now just regular blame
    subprocess.run(["git", "blame", file])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <git-flow|git-stats|git-blame-ai>")
    else:
        cmd = sys.argv[1]
        if cmd == "git-flow":
            git_flow(sys.argv[2:])
        elif cmd == "git-stats":
            git_stats()
        elif cmd == "git-blame-ai":
            git_blame_ai()
        else:
            print(f"Unknown command: {cmd}")
