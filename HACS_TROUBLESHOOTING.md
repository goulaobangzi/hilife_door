# HACS 故障排除指南

## 问题描述
HACS 显示："The version v1.2.0 for this integration can not be used with HACS."

## 可能的原因和解决方案

### 1. HACS 缓存问题
**解决方案**：
- 在 Home Assistant 中重启 HACS
- 进入 HACS → 集成 → 右上角三个点 → "重新加载"
- 等待几分钟让 HACS 刷新

### 2. 仓库添加错误
**检查步骤**：
1. 在 HACS 中，进入"集成"
2. 找到"HiLife 合生活门禁"
3. 确认仓库 URL 是：`https://github.com/goulaobangzi/hilife_door`
4. 确认类型是："Integration"

### 3. 版本格式问题
**当前状态**：
- ✅ 版本格式正确：1.2.0
- ✅ Release 存在且非草稿

### 4. 手动安装方法
如果 HACS 仍然无法使用，可以手动安装：

```bash
# 下载 v1.2.0
wget https://github.com/goulaobangzi/hilife_door/archive/refs/tags/v1.2.0.zip

# 解压到 Home Assistant
unzip v1.2.0.zip
cp -r hilife_door-1.2.0/custom_components/hilife_door /config/custom_components/

# 重启 Home Assistant
```

### 5. 验证安装
安装后，在 Home Assistant 中检查：
1. 设置 → 设备与服务
2. 查看是否有"HiLife 合生活门禁"
3. 如果有错误，检查日志

### 6. 联系支持
如果问题仍然存在：
1. 在 GitHub 上创建 Issue
2. 提供错误日志
3. 说明 Home Assistant 版本

## 临时解决方案

在 HACS 修复之前，用户可以：

1. **使用旧版本**：继续使用 v1.0.0
2. **手动安装**：下载最新版本手动安装
3. **使用脚本**：直接运行 `get_userid.py` 获取 userId

## 检查清单

- [x] manifest.json 包含所有必需字段
- [x] hacs.json 存在且格式正确
- [x] GitHub Release v1.2.0 已创建
- [x] 版本格式符合语义化版本规范
- [x] 文件结构符合 HACS 要求

## 下一步

1. 等待 HACS 自动刷新（可能需要 1-2 小时）
2. 如果仍有问题，考虑重新提交到 HACS 官方仓库
3. 为用户提供手动安装指导
