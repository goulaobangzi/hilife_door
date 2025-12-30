import requests
import json
import base64

# GitHub API 配置
token = "YOUR_GITHUB_TOKEN"  # 需要你的 GitHub token
repo = "goulaobangzi/hilife_door"
path = "custom_components/hilife_door/manifest.json"

# 读取新的 manifest.json
with open('custom_components/hilife_door/manifest.json', 'r') as f:
    new_content = f.read()

# 准备 API 请求
url = f"https://api.github.com/repos/{repo}/contents/{path}"
headers = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json"
}

# 先获取当前文件信息
response = requests.get(url, headers=headers)
if response.status_code == 200:
    current_file = response.json()
    sha = current_file['sha']
    
    # 更新文件
    data = {
        "message": "更新版本到 v1.2.0",
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": sha
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print("文件更新成功！")
    else:
        print(f"更新失败: {response.text}")
else:
    print(f"获取文件失败: {response.text}")
