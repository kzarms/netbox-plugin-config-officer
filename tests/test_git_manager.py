"""Tests for git_manager.py"""

import pytest
# from git_manager import *

import time
import os
from datetime import datetime
from pydriller import RepositoryMining, GitRepository

def get_device_config(directory, hostname, config_type="running"):
    """Get data from text file according to config source."""
    try:
        with open(f"{directory}/{hostname}_{config_type}.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None


def get_days_after_update(directory, hostname, config_type="running"):
    """Get days after last update."""
    try:
        create_time = os.stat(f"{directory}/{hostname}_{config_type}.txt").st_ctime        
        return round((time.time() - create_time) / 86400)
    except:
        return -1

def get_config_update_date(directory, hostname, config_type="running"):
    """Get date of last update device config file."""

    try:
        create_time = os.stat(f"{directory}/{hostname}_{config_type}.txt").st_ctime   
        return datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M")       
    except:
        return "unknown"

def get_file_repo_state(repository_path, filename):
    """Get commits and diffs for file."""

    git_repo = GitRepository(repository_path)
    repo_state = {}
    repo_state["commits_count"] = 0
    try:
        file_commits_list = git_repo.git.log("--format=%H", filename).split("\n")
        file_commits = list(RepositoryMining(repository_path, only_commits=file_commits_list).traverse_commits())
        file_commits.reverse()
        repo_state["commits_count"] = len(file_commits)
    except:
        pass
        
    if repo_state["commits_count"] > 0:
        repo_state["last_commit_date"] = file_commits[0].author_date.strftime("%d %b %Y %H:%M")
        repo_state["first_commit_date"] = file_commits[-1].author_date.strftime("%d %b %Y %H:%M")
        repo_state["commits"] = []
        for commit in file_commits:
            print(commit.hash)
            for mod in commit.modifications:
                if mod.filename == filename:
                    diff = mod.diff
            repo_state["commits"].append(
                {"hash": commit.hash, "msg": commit.msg, "diff": diff, "date": commit.author_date}
            )
    else:
        repo_state["comment"] = "no commits changes for {filename}"
    return repo_state


##################################

@pytest.fixture(scope="module")
def createTestFile():
    # Create demo dir and file inside with simple text
    demoDir = "demo"
    os.mkdir(demoDir)
    fname = demoDir + "/r9_running.txt"
    f = open(fname,"w+")
    f.write("Hello World")
    f.close()
    # Read the file from the function
    yield
    # Cleanup
    os.remove(fname)
    os.rmdir(demoDir)


### Test functions for get_device_config
def test_get_device_config_exeption_noFileFound():
    assert get_device_config('', '') == None


def test_get_device_config_exeption_NormalRead(createTestFile):
    assert get_device_config('demo', 'r9', 'running') == "Hello World"


### Test functions for get_days_after_update
def test_get_days_after_update_ok(createTestFile):
    assert get_days_after_update('demo', 'r9', 'running') == 0

def test_get_days_after_update_error():
    assert get_days_after_update('', 'r9', 'running') == -1


### Test functions for get_days_after_update
def test_get_config_update_date_ok(createTestFile):
    filetime = datetime.today().strftime("%Y-%m-%d %H:%M")
    assert get_config_update_date('demo', 'r9', 'running') == filetime


def test_get_config_update_date_error(createTestFile):
    assert get_config_update_date('', 'r9', 'running') == "unknown"