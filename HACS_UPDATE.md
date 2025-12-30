# HACS 更新说明

## 当前状态
- 主仓库已更新到 v1.2.0
- README.md 已更新，包含新的 userId 获取方法
- manifest.json 版本已更新

## HACS 更新步骤

由于 HACS 的集成仓库需要通过 PR 提交，请按以下步骤操作：

### 方法1：通过 HACS 官方仓库提交 PR

1. 访问 HACS integration 仓库：
   https://github.com/hacs/integration

2. Fork 该仓库到你的账号

3. 克隆你的 Fork：
   ```bash
   git clone https://github.com/你的用户名/integration.git
   cd integration
   ```

4. 创建新分支：
   ```bash
   git checkout -b add-hilife-door-v120
   ```

5. 创建集成目录：
   ```bash
   mkdir -p integrations/hilife_door
   ```

6. 复制文件到新目录：
   - 将 `custom_components/hilife_door/` 中的所有文件复制到 `integrations/hilife_door/`
   - 注意：manifest.json 需要放在 `integrations/hilife_door/` 目录下

7. 提交更改：
   ```bash
   git add .
   git commit -m "Add HiLife Door integration v1.2.0"
   ```

8. 推送到你的 Fork：
   ```bash
   git push origin add-hilife-door-v120
   ```

9. 在 GitHub 上创建 Pull Request

### 方法2：等待 HACS 自动同步

HACS 会定期检查已添加的仓库是否有更新。如果你的仓库已经在 HACS 中，HACS 会在下次检查时自动获取更新。

### 验证更新

用户可以通过以下方式验证是否更新：
1. 在 Home Assistant 中访问 HACS
2. 点击"集成"
3. 找到"HiLife 合生活门禁"
4. 查看版本是否为 1.2.0
5. 如果有更新提示，点击更新

## 注意事项

- 确保 manifest.json 中的版本号为 1.2.0
- 确保新的 get_userid.py 脚本已包含在仓库中
- README.md 已更新包含新的获取方法
