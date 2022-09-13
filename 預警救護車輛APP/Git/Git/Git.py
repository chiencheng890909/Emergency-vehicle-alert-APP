import requests
from github import Github

g = Github()
user = g.get_user('miro20000909')
Accounts = user.get_repo('safe_drving')
print(Accounts)
