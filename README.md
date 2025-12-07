# HiLife 合生活门禁 - Home Assistant 集成

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

这是一个 Home Assistant 自定义集成，用于控制 HiLife（合生活）App 中的智能门禁。

## 功能

- ✅ 支持多小区（配置时选择）
- ✅ 自动获取门列表
- ✅ 每个门作为独立的 Lock 实体
- ✅ 支持开门操作
- ✅ 中文界面

## 安装

### HACS 安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 点击 HACS → 集成 → 右上角三个点 → 自定义存储库
3. 添加此仓库 URL：`https://github.com/goulaobangzi/hilife_door`
4. 类别选择 "Integration"
5. 点击添加
6. 在 HACS 中搜索 "HiLife" 并安装
7. 重启 Home Assistant

### 手动安装

1. 下载此仓库的 `custom_components/hilife_door` 文件夹
2. 将其复制到 Home Assistant 的 `custom_components` 目录
3. 重启 Home Assistant

## 配置

### 获取 userId

首次配置需要提供 `userId`（也叫 `personId`），这是 HiLife App 为每个用户生成的唯一标识。

**获取方法：**

#### 方法1: mitmproxy 抓包（推荐）

```bash
# 1. 安装 mitmproxy
pip install mitmproxy

# 2. 启动代理
mitmdump -p 8888

# 3. 手机设置代理（电脑IP:8888）
# 4. 安装 mitmproxy 证书到手机

# 5. 在 App 中点击门禁

# 6. 从输出中找到 personId=xxxxxx 或 userId=xxxxxx
```

#### 方法2: ADB 读取（需要 root）

```bash
adb shell "su -c 'grep personId /data/data/cn.net.cyberway.hosponlife.main/shared_prefs/*.xml'"
```

### 添加集成

1. 在 Home Assistant 中，进入 **设置** → **设备与服务** → **添加集成**
2. 搜索 "HiLife" 或 "合生活"
3. 输入：
   - 手机号
   - 密码
   - userId（从上一步获取）
4. 如果绑定了多个小区，选择要添加的小区
5. 完成！

## 截图

### 配置界面

![配置界面](docs/config.png)

### 设备列表

![设备列表](docs/devices.png)

## 使用

配置完成后，每个门会作为一个 Lock 实体出现在 Home Assistant 中。

### 开门

- 在 Home Assistant 界面点击门的"解锁"按钮
- 或者使用服务调用：

```yaml
service: lock.unlock
target:
  entity_id: lock.珠江愉景家园西区26_楼大堂门
```

### 自动化示例

```yaml
automation:
  - alias: "到家自动开门"
    trigger:
      - platform: zone
        entity_id: person.me
        zone: zone.home
        event: enter
    action:
      - service: lock.unlock
        target:
          entity_id: lock.珠江愉景家园西区26_楼大堂门
```

## 注意事项

1. **userId 是固定的** - 配置一次后永久有效
2. **token 自动刷新** - 无需手动操作
3. **门禁状态** - 由于 API 限制，门始终显示为"已锁定"状态

## 故障排除

### 无法连接

- 检查手机号和密码是否正确
- 检查 userId 是否正确
- 检查网络连接

### 未找到小区

- 确认 userId 是否正确
- 确认账号已绑定小区

### 开门失败

- 检查日志中的错误信息
- 确认门禁设备在线

## 支持

如有问题，请在 [Issues](https://github.com/goulaobangzi/hilife_door/issues) 中提交。

## 许可证

MIT License

## 致谢

感谢所有贡献者！
