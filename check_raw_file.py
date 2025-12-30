import requests

# 直接访问 GitHub 的原始文件
url = "https://raw.githubusercontent.com/goulaobangzi/hilife_door/main/custom_components/hilife_door/manifest.json"
response = requests.get(url)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    print(f"文件内容:\n{response.text}")
else:
    print(f"获取失败: {response.text}")

# 检查 README
url = "https://raw.githubusercontent.com/goulaobangzi/hilife_door/main/README.md"
response = requests.get(url)
if response.status_code == 200:
    if "get_userid.py" in response.text:
        print("\n✅ README.md 已更新，包含 get_userid.py")
    else:
        print("\n❌ README.md 未更新")
