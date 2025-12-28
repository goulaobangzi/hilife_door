# HiLife 合生活门禁 - Home Assistant 集成

这是一个 Home Assistant 自定义集成，用于控制 HiLife（合生活）App 中的智能门禁。

## 项目结构

```
gateunlocker/
├── README.md                    # 项目说明
├── custom_components/           # Home Assistant 集成
│   └── hilife_door/
│       ├── __init__.py          # 集成入口
│       ├── api.py               # API 客户端
│       ├── config_flow.py       # 配置流程
│       ├── const.py             # 常量定义
│       ├── lock.py              # Lock 实体
│       ├── manifest.json        # 插件清单
│       ├── strings.json         # 默认字符串
│       └── translations/        # 多语言支持
├── hacs_repo/                   # HACS 仓库（已上传到 GitHub）
├── hilife_api.py                # 独立 API 测试脚本
├── hilife_door_api.py           # 开门 API 封装
└── get_door_params.py           # 参数获取脚本
```

## GitHub 仓库

**https://github.com/goulaobangzi/hilife_door**

## 功能

- ✅ 支持多小区（配置时选择）
- ✅ 自动获取门列表
- ✅ 每个门作为独立的 Lock 实体
- ✅ 支持开门操作
- ✅ 中文和英文界面

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

1. 将 `custom_components/hilife_door` 文件夹复制到 Home Assistant 的 `custom_components` 目录
2. 重启 Home Assistant

## 配置

### 获取 userId (可选)

集成现已支持自动获取 `userId`，配置时留空即可。

如果自动获取失败，您可以通过以下方式获取 userId：

#### 方法1：脚本自动获取（最简单）

使用项目中的脚本，一键获取 userId：

```bash
python get_userid.py
```

脚本会自动：
1. 登录获取 access_token
2. 调用接口获取 personID
3. 输出正确的 userId

无需验证码，无需抓包。

#### 方法2：Chrome 开发者工具

1. 打开 Chrome 浏览器，访问：https://www.91helife.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Network`（网络）标签
4. 登录账号
5. 查找 `getPersonInfo` 请求
6. 在响应中找到 `personInfo.personID`

#### 方法3：ADB 读取（需要 root）

```bash
adb shell "su -c 'grep personId /data/data/cn.net.cyberway.hosponlife.main/shared_prefs/*.xml'"
```

### 添加集成

1. 在 Home Assistant 中，进入 **设置** → **设备与服务** → **添加集成**
2. 搜索 "HiLife" 或 "合生活"
3. 输入：
   - 手机号
   - 密码
   - userId（可选，留空自动获取）
4. 如果绑定了多个小区，选择要添加的小区
5. 完成！

## API 说明

### 登录 API

```
POST https://token.91helife.com/oauth/token
Authorization: Basic ZXNuTW9iaWxlQ2xpZW50OmVzbk1vYmlsZQ==
Content-Type: application/x-www-form-urlencoded

grant_type=multiple&username=手机号&password=密码
```

### 获取门列表 API

```
POST https://www.91helife.com/erp/front/interface/es/door/v3/getDoors
```

### 开门 API

```
POST https://www.91helife.com/erp/front/interface/door/openDoor/three
```

## 许可证

MIT License
