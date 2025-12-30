# Version 1.2.0 - 无需验证码获取 userId

## 🎉 新功能
- ✨ 新增无需验证码的 userId 获取脚本 `get_userid.py`
- 🚀 一键运行即可获取正确的 userId
- 📝 简化了获取流程，不再需要 mitmproxy 抓包

## 📋 获取 userId 的方法

### 方法1：脚本自动获取（推荐）
```bash
python get_userid.py
```
脚本会自动：
1. 登录获取 access_token
2. 调用接口获取 personID
3. 输出正确的 userId

### 方法2：Chrome 开发者工具
1. 访问 https://www.91helife.com
2. 按 F12 打开开发者工具
3. 切换到 Network（网络）标签
4. 登录账号
5. 查找 `getPersonInfo` 请求
6. 在响应中找到 `personInfo.personID`

### 方法3：ADB 读取（需要 root）
```bash
adb shell "su -c 'grep personId /data/data/cn.net.cyberway.hosponlife.main/shared_prefs/*.xml'"
```

## 🔧 安装更新

### HACS 用户
1. 在 Home Assistant 中进入 HACS
2. 点击"集成"
3. 找到"HiLife 合生活门禁"
4. 点击更新按钮
5. 重启 Home Assistant

### 手动安装用户
1. 下载最新版本：https://github.com/goulaobangzi/hilife_door/archive/refs/tags/v1.2.0.zip
2. 解压后复制 `custom_components/hilife_door` 到 Home Assistant
3. 重启 Home Assistant

## ⚠️ 注意事项
- 此版本简化了 userId 获取流程
- 旧版本的用户可以继续使用，无需重新配置
- 如果自动获取 userId 失败，请使用脚本手动获取

## 🐛 Bug 修复
- 优化了 userId 获取逻辑
- 改进了错误提示信息

## 📝 文档更新
- 更新了 README.md，添加了详细的获取方法说明
- 添加了 get_userid.py 脚本使用说明

---

## 下载
- [v1.2.0.zip](https://github.com/goulaobangzi/hilife_door/archive/refs/tags/v1.2.0.zip)
- [源代码](https://github.com/goulaobangzi/hilife_door/tree/v1.2.0)
