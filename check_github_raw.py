import requests
import json
import base64

# 检查 GitHub 上的 manifest.json
url = "https://api.github.com/repos/goulaobangzi/hilife_door/contents/custom_components/hilife_door/manifest.json"
response = requests.get(url)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    content = response.json()
    print(f"文件 SHA: {content['sha']}")
    decoded = base64.b64decode(content['content']).decode('utf-8')
    print(f"文件内容:\n{decoded}")
else:
    print(f"响应内容: {response.text}")

# 检查最新的提交
url = "https://api.github.com/repos/goulaobangzi/hilife_door/commits/main"
response = requests.get(url)
print(f"\n最新提交:")
if response.status_code == 200:
    commit = response.json()
    print(f"SHA: {commit['sha']}")
    print(f"消息: {commit['commit']['message']}")
    print(f"作者: {commit['commit']['author']['name']}")
