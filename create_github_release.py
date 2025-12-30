"""
创建 GitHub Release 的脚本
需要 GitHub Personal Access Token
"""

import requests
import json
import base64

# 配置
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # 替换为你的 token
REPO_OWNER = "goulaobangzi"
REPO_NAME = "hilife_door"
TAG_NAME = "v1.2.0"

def create_release():
    """创建 GitHub Release"""
    
    # API URL
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    
    # Headers
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    # Release 数据
    release_data = {
        "tag_name": TAG_NAME,
        "target_commitish": "main",
        "name": f"Version 1.2.0 - 无需验证码获取 userId",
        "body": """## 🎉 新功能
- ✨ 新增无需验证码的 userId 获取脚本 `get_userid.py`
- 🚀 一键运行即可获取正确的 userId
- 📝 简化了获取流程，不再需要 mitmproxy 抓包

## 📋 获取 userId 的方法

### 方法1：脚本自动获取（推荐）
```bash
python get_userid.py
```

### 方法2：Chrome 开发者工具
1. 访问 https://www.91helife.com
2. 按 F12 打开开发者工具
3. 登录后查找 getPersonInfo 请求

### 方法3：ADB 读取（需要 root）
```bash
adb shell "su -c 'grep personId ...'"
```

## 🔧 更新说明
- 此版本简化了 userId 获取流程
- 旧版本用户可以继续使用，无需重新配置
- 如果自动获取失败，请使用脚本手动获取
""",
        "draft": False,
        "prerelease": False
    }
    
    # 创建 Release
    print(f"正在创建 Release {TAG_NAME}...")
    response = requests.post(url, headers=headers, json=release_data)
    
    if response.status_code == 201:
        release = response.json()
        print("✅ Release 创建成功！")
        print(f"   - URL: {release['html_url']}")
        print(f"   - 上传地址: {release['upload_url']}")
        return True
    else:
        print(f"❌ 创建失败: {response.status_code}")
        print(f"   错误信息: {response.text}")
        return False

def get_token_instructions():
    """获取 GitHub Token 的说明"""
    print("\n=== 获取 GitHub Personal Access Token ===")
    print("1. 登录 GitHub")
    print("2. 点击右上角头像 → Settings")
    print("3. 左侧菜单 → Developer settings")
    print("4. Personal access tokens → Tokens (classic)")
    print("5. Generate new token")
    print("6. 勾选 'repo' 权限")
    print("7. 复制生成的 token")
    print("\n将 token 粘贴到脚本中的 GITHUB_TOKEN 变量")

if __name__ == "__main__":
    # 检查是否配置了 token
    if GITHUB_TOKEN == "YOUR_GITHUB_TOKEN":
        print("❌ 请先配置 GitHub Token")
        get_token_instructions()
    else:
        # 尝试创建 Release
        if create_release():
            print("\n✅ 成功！现在 HACS 应该能够检测到更新了。")
            print("请在 HACS 中重新加载或重启 Home Assistant。")
        else:
            print("\n❌ 创建失败，请检查权限和网络连接。")
