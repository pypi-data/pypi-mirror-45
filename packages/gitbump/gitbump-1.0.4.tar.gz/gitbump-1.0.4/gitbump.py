"""
Autoversioning for Git repos

This app is based on the script that can be found here:
https://gitlab.com/threedotslabs/ci-scripts/blob/master/common/gen-semver
"""

import os
import sys
import subprocess
import re
import semver

BUMP_METHODS = {
    'minor': semver.bump_minor,
    'major': semver.bump_major,
    'patch': semver.bump_patch
}

def git(*args):
    return subprocess.check_output(["git"] + list(args)).decode().strip()


def get_repo_url():
    """Get the remote repository URL"""
    url = git("config", "remote.origin.url")

    # Example input: https://gitlab-ci-token:xxxxxxxxxxxxxxxxxxxx@gitlab.com/xxx/project.git
    # Example output: git@gitlab.com:xxx/project.git
    if 'gitlab-ci-token' in url:
        return re.sub(r'.+@([^/]+)/', r'git@\1:', url)

    return url

def tag_repo(tag):
    push_url = get_repo_url()
    git("remote", "set-url", "--push", "origin", push_url)
    git("tag", tag)
    git("push", "origin", tag)

def bump(latest, commands):
    if not commands:
        return semver.bump_patch(latest)

    for cmd in commands:
        latest = BUMP_METHODS[cmd](latest)

    return latest


def check_commit_msg():
    msg = git("log", "-1")
    return re.findall(r'#bump_(minor|major|patch)', msg)


def main():
    try:
        latest = git("describe", "--tags")
    except subprocess.CalledProcessError:
        # No tags in the repository
        version = "1.0.0"
    else:
        # Skip already tagged commits
        if '-' not in latest:
            print(latest)
            return 0

        commands = check_commit_msg()
        version = bump(latest, commands)

    tag_repo(version)
    print(version)

    return 0

if __name__ == '__main__':
    sys.exit(main())