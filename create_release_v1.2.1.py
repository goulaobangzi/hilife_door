"""
创建 v1.2.1 Release 的说明
"""

print("""
=== 创建 GitHub Release v1.2.1 ===

请按以下步骤操作：

1. 访问 GitHub Release 页面：
   https://github.com/goulaobangzi/hilife_door/releases/new

2. 填写信息：
   - Tag: v1.2.1
   - Target: main
   - Title: Version 1.2.1 - 修复自动获取 userId
   - Description: 复制下面的内容

3. Release 描述内容：

# Version 1.2.1 - 修复自动获取 userId

## 🐛 重要修复
- ✅ **修复了自动获取 userId 功能**
- ✅ 解决了 "No communities found" 的问题
- ✅ 现在用户可以留空 userId，系统会自动检测

## 🔧 技术细节
- 登录时自动调用 `getPersonInfo` API 获取真正的 personID
- 如果无法获取 personID，会回退到使用 openID
- 确保使用正确的 userId 格式（19位数字）

## 📋 使用方法
1. 在 Home Assistant 中配置 HiLife 集成
2. 输入手机号和密码
3. **userId 留空**（系统会自动获取）
4. 保存配置

## ✅ 测试结果
- 自动获取 personID: `5498174404738171004`
- 成功获取社区列表
- 无需手动输入 userId

## 🔄 升级说明
- 如果您已经在使用 v1.2.0，建议升级到此版本
- 如果遇到 "No communities found" 错误，此版本将解决该问题
- 旧版本用户无需重新配置，升级后会自动修复

4. 点击 "Publish release" 发布

完成之后，HACS 就能检测到 v1.2.1 版本了！

注意：确保不要勾选 "This is a pre-release" 或 "Set as a draft"
""")

print("\n标签 v1.2.1 已推送到 GitHub！")
print("现在请访问上面的链接创建 Release。")
