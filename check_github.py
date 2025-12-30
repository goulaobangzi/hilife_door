import requests
import json

# 检查 GitHub 上的 manifest.json
url = "https://api.github.com/repos/goulaobangzi/hilife_door/contents/custom_components/hilife_door/manifest.json"
response = requests.get(url)
if response.status_code == 200:
    content = response.json()
    import base64
    decoded = base64.b64decode(content['content']).decode('utf-8')
    manifest = json.loads(decoded)
    print(f"GitHub 上的版本: {manifest['version']}")
else:
    print(f"获取失败: {response.status_code}")

# 检查最新 release
url = "https://api.github.com/repos/goulaobangzi/hilife_door/releases/latest"
response = requests.get(url)
if response.status_code == 200:
    release = response.json()
    print(f"最新 Release: {release['tag_name']}")
else:
    print(f"获取 Release 失败: {response.status_code}")
