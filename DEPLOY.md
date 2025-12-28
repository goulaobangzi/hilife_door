# 部署到 GitHub

## 步骤

1. 在 GitHub 上创建新仓库：`hilife_door`
   - 访问：https://github.com/new
   - 仓库名：`hilife_door`
   - 描述：`HiLife 合生活门禁 - Home Assistant 集成`
   - 设为公开（Public）
   - 不要初始化 README、.gitignore 或 license

2. 添加远程仓库：
```bash
git remote add origin https://github.com/your-username/hilife_door.git
```

3. 推送到 GitHub：
```bash
git branch -M main
git push -u origin main
```

4. 创建 Release：
   - 访问 GitHub 仓库页面
   - 点击 "Releases" → "Create a new release"
   - 标签：`v1.2.0`
   - 标题：`Version 1.2.0`
   - 描述：添加无需验证码的 userId 获取脚本

## 更新 manifest.json

记得将 manifest.json 中的以下内容替换为实际信息：
- `codeowners`: ["@your-github-username"]
- `documentation`: "https://github.com/your-username/hilife_door"
- `issue_tracker`: "https://github.com/your-username/hilife_door/issues"

## HACS 提交

如果需要提交到 HACS：
1. Fork HACS 仓库：https://github.com/hacs/integration
2. 创建 PR 添加你的集成
