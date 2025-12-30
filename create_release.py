import requests
import json

# GitHub API 配置
token = "YOUR_GITHUB_TOKEN"  # 需要你的 GitHub Personal Access Token
repo = "goulaobangzi/hilife_door"

# 创建 Release 的 API
url = f"https://api.github.com/repos/{repo}/releases"

# Release 数据
release_data = {
    "tag_name": "v1.2.0",
    "target_commitish": "main",
    "name": "Version 1.2.0 - 无需验证码获取 userId",
    "body": """## 🎉 新功能
- ✨ 新增无需验证码的 userId 获取脚本 `get_userid.py`
- 🚀 一键运行即可获取正确的 userId
- 📝 简化了获取流程，不再需要 mitmproxy 抓包

## 📋 获取 userId 的方法
1. **脚本自动获取（推荐）**
   ```bash
   python get_userid.py
   ```
   
2. **Chrome 开发者工具**
   - 访问 https://www.91helife.com
   - F12 打开开发者工具
   - 登录后查找 getPersonInfo 请求
   
3. **ADB 读取（需要 root）**
   ```bash
   adb shell "su -c 'grep personId ...'"
   ```

## 🔧 安装更新
- HACS 用户：在 HACS 中检查更新
- 手动安装：下载最新版本替换文件

## ⚠️ 注意
- 此版本简化了 userId 获取流程
- 旧版本的用户可以继续使用，无需重新配置
""",
    "draft": False,
    "prerelease": False
}

# 发送请求
headers = {
    "Authorization": f"token {token}",
    "Content-Type": "application/json"
}

print("请按以下步骤创建 Release：")
print("1. 访问：https://github.com/goulaobangzi/hilife_door/releases/new")
print("2. 标签：v1.2.0")
print("3. 标题：Version 1.2.0 - 无需验证码获取 userId")
print("4. 复制上面的 body 内容到描述框")
print("5. 点击 \"Publish release\"")
