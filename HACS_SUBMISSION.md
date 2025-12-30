# 提交到 HACS 官方仓库指南

## 当前状态
- 集成已在个人仓库发布：https://github.com/goulaobangzi/hilife_door
- 用户可以通过"自定义存储库"添加

## 选项1：继续使用自定义存储库（推荐）

**优点**：
- 完全控制发布流程
- 立即可用，无需等待审核
- 可以快速发布更新

**用户使用步骤**：
1. HACS → 集成 → 三个点 → 自定义存储库
2. 添加：`https://github.com/goulaobangzi/hilife_door`
3. 类别选择：Integration
4. 点击添加并安装

## 选项2：提交到 HACS 官方仓库

**优点**：
- 在 HACS 默认商店中显示
- 更容易发现

**缺点**：
- 需要审核（可能需要几天到几周）
- 发布流程受 HACS 团队控制

**提交步骤**：

1. Fork HACS integration 仓库：
   ```bash
   git clone https://github.com/hacs/integration.git
   cd integration
   ```

2. 创建新分支：
   ```bash
   git checkout -b add-hilife-door
   ```

3. 添加集成：
   ```bash
   mkdir -p integrations/hilife_door
   # 复制所有文件到 integrations/hilife_door/
   cp -r /path/to/hilife_door/* integrations/hilife_door/
   ```

4. 提交更改：
   ```bash
   git add .
   git commit -m "Add HiLife Door integration"
   ```

5. 推送并创建 PR：
   ```bash
   git push origin add-hilife-door
   # 在 GitHub 上创建 Pull Request
   ```

6. 填写 PR 模板：
   - 集成名称：HiLife 合生活门禁
   - 描述：控制 HiLife（合生活）App 中的智能门禁
   - 链接：https://github.com/goulaobangzi/hilife_door

## 建议

**当前建议使用选项1（自定义存储库）**，原因：
1. 用户可以立即使用
2. 已经有完整的 Release
3. 可以快速响应问题和更新

如果集成变得流行（超过 100 个用户），可以考虑提交到官方仓库。

## 用户通知

在 README 中添加说明：

```markdown
## 安装

### HACS 安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 点击 HACS → 集成 → 右上角三个点 → 自定义存储库
3. 添加此仓库 URL：`https://github.com/goulaobangzi/hilife_door`
4. 类别选择 "Integration"
5. 点击添加
6. 在 HACS 中搜索 "HiLife" 并安装
7. 重启 Home Assistant
```

## 注意事项

- 确保仓库是公开的
- 确保所有 Release 都是正式版本（非草稿）
- 保持 manifest.json 更新
