import requests
import json
from datetime import datetime

print("=== HACS 更新问题诊断 ===\n")

# 1. 检查仓库的基本信息
repo = "goulaobangzi/hilife_door"
api_base = f"https://api.github.com/repos/{repo}"

# 获取仓库信息
response = requests.get(api_base)
if response.status_code == 200:
    repo_info = response.json()
    print(f"✅ 仓库信息:")
    print(f"   - 名称: {repo_info['name']}")
    print(f"   - 是否私有: {repo_info['private']}")
    print(f"   - 是否为 Fork: {repo_info['fork']}")
    print(f"   - 默认分支: {repo_info['default_branch']}")
    print(f"   - 创建时间: {repo_info['created_at']}")
    print(f"   - 更新时间: {repo_info['updated_at']}")
    
    if repo_info['private']:
        print("\n❌ 错误：仓库是私有的！HACS 只能使用公开仓库。")
    else:
        print("\n✅ 仓库是公开的")
else:
    print(f"❌ 无法获取仓库信息: {response.status_code}")

# 2. 检查所有 Releases
print("\n=== 所有 Releases ===")
response = requests.get(f"{api_base}/releases")
if response.status_code == 200:
    releases = response.json()
    print(f"找到 {len(releases)} 个 Release:")
    
    for release in releases:
        print(f"\n📦 {release['tag_name']}")
        print(f"   - 名称: {release['name']}")
        print(f"   - 发布时间: {release['published_at']}")
        print(f"   - 是否为最新: {release['prerelease']}")
        print(f"   - 是否为草稿: {release['draft']}")
        print(f"   - 目标分支: {release['target_commitish']}")
        
        # 检查 assets
        if release['assets']:
            print(f"   - 附件: {len(release['assets'])} 个")
else:
    print("❌ 无法获取 Releases")

# 3. 检查最新提交
print("\n=== 最新提交 ===")
response = requests.get(f"{api_base}/commits/main")
if response.status_code == 200:
    commit = response.json()
    print(f"✅ 最新提交:")
    print(f"   - SHA: {commit['sha'][:7]}")
    print(f"   - 消息: {commit['commit']['message']}")
    print(f"   - 时间: {commit['commit']['committer']['date']}")
    
    # 检查提交是否在 Release 之后
    if releases:
        latest_release = releases[0]
        release_date = datetime.fromisoformat(latest_release['published_at'].replace('Z', '+00:00'))
        commit_date = datetime.fromisoformat(commit['commit']['committer']['date'].replace('Z', '+00:00'))
        
        if commit_date > release_date:
            print(f"\n⚠️ 警告：有新的提交在 Release 之后！")
            print(f"   - Release 时间: {release_date}")
            print(f"   - 提交时间: {commit_date}")
            print("   建议：创建新的 Release 包含最新更改")

# 4. 检查 manifest.json 在最新 Release 中的内容
print("\n=== Release 中的 manifest.json ===")
if releases:
    latest_release = releases[0]
    response = requests.get(f"{api_base}/contents/custom_components/hilife_door/manifest.json?ref={latest_release['tag_name']}")
    
    if response.status_code == 200:
        import base64
        content = response.json()
        decoded = base64.b64decode(content['content']).decode('utf-8')
        manifest = json.loads(decoded)
        
        print(f"✅ Release {latest_release['tag_name']} 中的 manifest.json:")
        print(f"   - 版本: {manifest['version']}")
        
        if manifest['version'] != latest_release['tag_name']:
            print(f"\n❌ 错误：manifest.json 版本 ({manifest['version']}) 与 Release 标签 ({latest_release['tag_name']}) 不匹配！")
            print("   这是 HACS 无法更新的常见原因。")
    else:
        print("❌ 无法获取 manifest.json")

# 5. HACS 特定检查
print("\n=== HACS 特定要求 ===")
print("1. 仓库必须包含 hacs.json 文件")
print("2. manifest.json 必须在 custom_components/域名/ 目录下")
print("3. Release 标签必须与 manifest.json 中的版本一致")
print("4. Release 不能是草稿或预发布版本")

print("\n=== 建议的修复步骤 ===")
print("1. 确保 manifest.json 版本与 Release 标签一致")
print("2. 创建新的 Release（如果版本不匹配）")
print("3. 在 HACS 中删除并重新添加仓库")
print("4. 重启 Home Assistant")
