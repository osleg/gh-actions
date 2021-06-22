import os
import re
import sys
import subprocess

from datetime import date
from pprint import pprint as pp

from atlassian import Jira


class TagNotFoundException(Exception):
    pass


def get_jira(uname: str, token: str) -> Jira:
    return Jira(
        url="https://cycognito.atlassian.net",
        username=uname,
        password=token,
        cloud=True)


def build_current_tag_tupple(offset: int = 0) -> str:
    # This assumes tags are in form YY.WW
    # Week is starting from 0, for our case it will represent last week number
    cur_year, last_week = date.today().strftime("%y %W").split(" ")
    if offset > int(last_week):
        cur_year = int(cur_year) - 1
        offset = int(last_week) - offset
        last_week = str(53)

    return (cur_year, int(last_week)-offset)


def build_current_tag(offset: int = 0):
    cur_year, last_week = build_current_tag_tupple(offset)
    return f"{cur_year}.{int(last_week)-offset}"


def build_next_tag():
    cur_year, last_week = build_current_tag_tupple(0)
    return f"V{cur_year}.{int(last_week)+1}"


def get_last_tag(offset: int = 0) -> str:
    tt = build_current_tag(offset)
    # We are gettings all tags since last version release
    cmd_log_tags = ["git", "log", "--tags",
                    "--simplify-by-decoration", "--pretty=\"format:%d\"" f"{tt}.."]
    tags = subprocess.check_output(cmd_log_tags)
    reg = re.compile(f"{tt}\.?\d+?")
    res = reg.findall(tags.decode())
    print(tags)
    if len(res) == 0:
        raise TagNotFoundException()
    if not res[0]:
        if offset >= 10:  # if we can't find 10 tags we doing something wrong
            raise TagNotFoundException()
        res = get_last_tag(offset+1)
    return res[0]  # This is the latest tag for given week


def get_glog(jira: Jira, tag: str) -> set:
    cmd_log = ["git", "log", "--simplify-by-decoration",
               "--pretty=\"format:%d\"", f"{tag}.."]
    log = subprocess.check_output(cmd_log)
    reg = re.compile("cyco-\d+", flags=re.RegexFlag.I)
    return set(reg.findall(log.decode()))


def get_jql(project: str, key: str) -> str:
    return f"project = {project} AND issueKey = {key}"

def get_jira_issues(jira: Jira, keys: set) -> dict:
    return {key: jira.issue(key) for key in keys}

def update_jira_issues(jira: jira, issues: dict):
    next_tag = build_next_tag()
    upd = {"fixversions": next_tag}
    pp(issues)
    for k, issue in issues.items():
        fixver = issue.get("fixversions")
        if not fixver:
            jira.update_issue_field(k, upd)

if __name__ == '__main__':
uname = os.getenv('JIRA_USERNAME')
token = os.getenv('JIRA_API_TOKEN')
jira = get_jira(uname, token)
if not uname or not token:
    sys.exit(1)

last_tag = get_last_tag()
log = get_glog(jira, last_tag)

issues = get_jira_issues(jira, log)

update_jira_issues(jira, issues)
