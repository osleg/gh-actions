import os
import sys

from pprint import pprint

from atlassian import Jira


def get_jira(uname, token):
    return Jira(
        url="https://cycognito.atlassian.net",
        username=uname,
        password=token,
        cloud=True)

def get_last_fixV(jira):
    pass

def get_glog():
    pass

if __name__ == '__main__':
    uname = os.getenv('JIRA_USERNAME')
    token = os.getenv('JIRA_API_TOKEN')

    log =  get_glog()

    if not uname or not token:
        sys.exit(1)

    jira = get_jira(uname, token)


    pprint(i)
