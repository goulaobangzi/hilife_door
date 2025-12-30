import json
import requests
from pathlib import Path

# HACS 要求检查
print("=== HACS 兼容性检查 ===\n")

# 1. 检查 manifest.json
manifest_path = Path("custom_components/hilife_door/manifest.json")
if manifest_path.exists():
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    print("✅ manifest.json 存在")
    print(f"   - domain: {manifest.get('domain')}")
    print(f"   - name: {manifest.get('name')}")
    print(f"   - version: {manifest.get('version')}")
    print(f"   - config_flow: {manifest.get('config_flow')}")
    print(f"   - iot_class: {manifest.get('iot_class')}")
    
    # 检查必需字段
    required_fields = ['domain', 'name', 'version', 'config_flow', 'iot_class']
    missing = [field for field in required_fields if not manifest.get(field)]
    if missing:
        print(f"\n❌ 缺少必需字段: {missing}")
    else:
        print("\n✅ 所有必需字段都存在")
else:
    print("❌ manifest.json 不存在")

# 2. 检查 hacs.json
hacs_path = Path("custom_components/hilife_door/hacs.json")
if hacs_path.exists():
    with open(hacs_path, 'r', encoding='utf-8') as f:
        hacs = json.load(f)
    
    print("\n✅ hacs.json 存在")
    print(f"   - name: {hacs.get('name')}")
    print(f"   - render_readme: {hacs.get('render_readme')}")
    print(f"   - homeassistant: {hacs.get('homeassistant')}")
else:
    print("\n❌ hacs.json 不存在")

# 3. 检查文件结构
print("\n=== 文件结构检查 ===")
required_files = [
    "custom_components/hilife_door/__init__.py",
    "custom_components/hilife_door/manifest.json",
    "custom_components/hilife_door/config_flow.py",
    "custom_components/hilife_door/strings.json",
]

for file_path in required_files:
    if Path(file_path).exists():
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path}")

# 4. 检查 GitHub Release
print("\n=== GitHub Release 检查 ===")
try:
    response = requests.get("https://api.github.com/repos/goulaobangzi/hilife_door/releases/tags/v1.2.0")
    if response.status_code == 200:
        print("✅ v1.2.0 Release 存在")
        release = response.json()
        print(f"   - 标题: {release['name']}")
        print(f"   - 是否为预发布: {release['prerelease']}")
        print(f"   - 是否为草稿: {release['draft']}")
    else:
        print("❌ v1.2.0 Release 不存在")
        print("   解决方案：在 GitHub 上创建正式的 Release")
except:
    print("❌ 无法检查 GitHub Release")

# 5. 版本格式检查
print("\n=== 版本格式检查 ===")
version = manifest.get('version', '')
if version and len(version.split('.')) >= 2:
    print(f"✅ 版本格式正确: {version}")
else:
    print(f"❌ 版本格式错误: {version}")
    print("   应使用语义化版本，如：1.2.0")

print("\n=== 建议 ===")
print("1. 确保 GitHub 上存在 v1.2.0 的正式 Release")
print("2. Release 不能是草稿（draft）或预发布（prerelease）")
print("3. 仓库应该是公开的（Public）")
print("4. 在 HACS 中使用正确的仓库 URL：https://github.com/goulaobangzi/hilife_door")
