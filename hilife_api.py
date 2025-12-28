"""
合生活 App API 接口
=====================================

【登录方法已验证成功】

使用方法:
---------
1. 直接运行此脚本:
   python hilife_api.py
   
2. 在代码中使用:
   from hilife_api import HiLifeAPI
   
   api = HiLifeAPI("手机号", "密码")
   if api.login():
       print("登录成功!")
       print(f"Token: {api.access_token}")

登录 API 详解:
--------------
- 端点: https://token.91helife.com/oauth/token
- 方法: POST
- 认证: Basic Auth (esnMobileClient:esnMobile)
- 关键参数: grant_type=multiple (不是 password!)

作者: Cascade AI
日期: 2024-12
"""
import requests
import base64
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ============================================================
#                        配置常量
# ============================================================

# OAuth 凭证 (从 APK 反编译提取)
OAUTH_CLIENT_ID = "esnMobileClient"
OAUTH_CLIENT_SECRET = "esnMobile"

# API 服务器地址
TOKEN_HOST = "https://token.91helife.com"    # 认证服务器
ERP_HOST = "https://www.91helife.com"        # ERP 服务器
MOBILE_HOST = "https://m.91helife.com"       # Mobile 服务器


# ============================================================
#                        API 客户端
# ============================================================

class HiLifeAPI:
    """合生活 API 客户端"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.open_id = None
        self.custom_id = None
        self.session = requests.Session()
        self.session.verify = False
        
    def login(self) -> bool:
        """
        登录获取 Access Token
        
        关键发现:
        - grant_type 必须是 "multiple" 而不是 "password"
        - 使用 Basic Auth 传递 OAuth 凭证
        """
        url = f"{TOKEN_HOST}/oauth/token"
        
        # Basic Auth
        auth_string = f"{OAUTH_CLIENT_ID}:{OAUTH_CLIENT_SECRET}"
        auth_header = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "okhttp/4.9.3",
        }
        
        # 关键: grant_type 必须是 "multiple"
        data = {
            "grant_type": "multiple",  # 不是 "password"!
            "username": self.username,
            "password": self.password,
        }
        
        print(f"[*] 登录: {self.username}")
        
        try:
            resp = self.session.post(url, data=data, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                result = resp.json()
                if 'access_token' in result:
                    self.access_token = result['access_token']
                    self.refresh_token = result.get('refresh_token')
                    self.open_id = result.get('openID')
                    self.custom_id = result.get('customID')
                    
                    print(f"[+] 登录成功!")
                    print(f"    Access Token: {self.access_token[:30]}...")
                    print(f"    OpenID: {self.open_id}")
                    print(f"    CustomID: {self.custom_id}")
                    return True
            
            print(f"[-] 登录失败: {resp.text}")
            return False
            
        except Exception as e:
            print(f"[-] 登录错误: {e}")
            return False
    
    def get_headers(self) -> dict:
        """获取带认证的请求头"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "okhttp/4.9.3",
            "Content-Type": "application/json",
            "accountIsolationID": str(self.custom_id) if self.custom_id else "10000",
        }
    
    def get_community_list(self) -> dict:
        """获取小区列表"""
        if not self.access_token:
            print("[-] 未登录")
            return None
        
        urls = [
            f"{ERP_HOST}/erp/front/interface/customer/getCommunity?access_token={self.access_token}",
            f"{ERP_HOST}/erp//front/interface/customer/getCommunity?access_token={self.access_token}",
        ]
        
        bodies = [
            {"personId": self.open_id},
            {"openID": self.open_id},
            {"personId": self.open_id, "customID": self.custom_id},
            {"personId": self.open_id, "accountIsolationID": self.custom_id},
            {"personId": self.open_id, "companyId": self.custom_id},
            {"personId": self.open_id, "communityId": self.custom_id},
            {"personId": self.open_id, "companyID": self.custom_id},
            {"personId": self.open_id, "accountIsolationID": "10000"},
            {},
        ]
        
        headers = self.get_headers()
        # 尝试添加一些通用 Header
        headers["Client-Version"] = "1.0.0"
        headers["Device-Type"] = "android"
        headers["accountIsolationID"] = str(self.custom_id) if self.custom_id else "10000"
        
        for url in urls:
            print(f"\n[*] 获取小区列表: {url}")
            
            for body in bodies:
                try:
                    resp = self.session.post(url, headers=headers, json=body, timeout=15)
                    result = resp.json() if resp.text else {}
                    
                    # DEBUG: 打印详细响应以便调试
                    print(f"    [DEBUG] Body: {body}")
                    print(f"    [DEBUG] Resp: {json.dumps(result, ensure_ascii=False)[:200]}")
                    
                    if result.get('status') == 0 or result.get('code') == '0000':
                        print(f"[+] 成功! Body: {body}")
                        print(f"    响应: {json.dumps(result, ensure_ascii=False)[:500]}")
                        return result
                    
                    # 尝试 form-urlencoded
                    headers_form = {
                        "Authorization": f"Bearer {self.access_token}",
                        "User-Agent": "okhttp/4.9.3",
                        "Content-Type": "application/x-www-form-urlencoded",
                    }
                    resp = self.session.post(url, headers=headers_form, data=body, timeout=15)
                    result = resp.json() if resp.text else {}
                    
                    # DEBUG: 打印详细响应以便调试
                    print(f"    [DEBUG] Body: {body}")
                    print(f"    [DEBUG] Resp: {json.dumps(result, ensure_ascii=False)[:200]}")
                    
                    if result.get('status') == 0 or result.get('code') == '0000':
                        print(f"[+] 成功 (form)! Body: {body}")
                        print(f"    响应: {json.dumps(result, ensure_ascii=False)[:500]}")
                        return result
                    
                    # 打印非重复的错误
                    msg = result.get('msg', '')
                    if msg and '请求失败' not in msg:
                        print(f"    Body: {body}, 响应: {msg}")
                        
                except Exception as e:
                    print(f"    错误: {e}")
        
        return None
    
    def get_door_list(self, community_id: str = None) -> dict:
        """获取门列表 - 尝试所有已知的 API 端点"""
        if not self.access_token:
            print("[-] 未登录")
            return None
        
        # 从 APK 反编译发现的所有门禁相关端点
        endpoints = [
            f"{ERP_HOST}/erp/front/interface/es/door/v3/openList",
            f"{ERP_HOST}/erp/front/interface/es/door/v3/getDoors",
            f"{ERP_HOST}/erp/front/interface/door/cardNos",
            f"{ERP_HOST}/erp/front/interface/door/CardNos/three",
            f"{ERP_HOST}/erp/front/interface/door/v3/collectDoors",
            # Mobile 服务器
            f"{MOBILE_HOST}/erp/front/interface/es/door/v3/openList",
            f"{MOBILE_HOST}/erp/front/interface/es/door/v3/getDoors",
            f"{MOBILE_HOST}/erp/front/interface/door/cardNos",
        ]
        
        # 从 APK 反编译发现的所有可能参数组合
        params_list = [
            {"personId": self.open_id},
            {"openID": self.open_id},
            {"openId": self.open_id},
            {"personId": self.open_id, "communityId": community_id or self.custom_id},
            {"personId": self.open_id, "companyId": self.custom_id},
            {"personId": self.open_id, "doorCommunityId": self.custom_id},
            {"userId": self.open_id},
            {"customerId": self.open_id},
            {},
        ]
        
        for url in endpoints:
            print(f"\n[*] 尝试端点: {url}")
            
            for body in params_list:
                # 移除 None 值
                body = {k: v for k, v in body.items() if v is not None}
                
                # 尝试不同的 Token 传递方式
                url_variants = [
                    url,  # 原始 URL
                    f"{url}?access_token={self.access_token}",  # Token 在 URL 参数中
                ]
                
                for test_url in url_variants:
                    # 尝试 JSON 和 form-urlencoded 两种格式
                    for content_type in ['json', 'form']:
                        try:
                            headers = self.get_headers()
                            
                            if content_type == 'json':
                                resp = self.session.post(test_url, headers=headers, json=body, timeout=15)
                            else:
                                headers["Content-Type"] = "application/x-www-form-urlencoded"
                                resp = self.session.post(test_url, headers=headers, data=body, timeout=15)
                            
                            result = resp.json() if resp.text else {}
                            
                            # 检查是否真正成功 (排除“未登录”的情况)
                            if (result.get('status') == 0 or result.get('code') == '0000') and '未登录' not in result.get('msg', ''):
                                print(f"[+] 成功! [{content_type}] URL: {test_url[:80]}...")
                                print(f"    Body: {body}")
                                print(f"    响应: {json.dumps(result, ensure_ascii=False)[:500]}")
                                return result
                            
                        except Exception as e:
                            pass
        
        print("[-] 所有端点都失败了")
        return None
    
    def open_door(self, door_id: str) -> bool:
        """开门"""
        if not self.access_token:
            print("[-] 未登录")
            return False
        
        url = f"{ERP_HOST}/erp/front/interface/door/openDoor/three"
        
        body = {
            "doorId": door_id,
            "personId": self.open_id,
        }
        
        print(f"[*] 开门: {door_id}")
        
        try:
            resp = self.session.post(
                url,
                headers=self.get_headers(),
                json=body,
                timeout=15
            )
            
            result = resp.json() if resp.text else {}
            print(f"    响应: {json.dumps(result, ensure_ascii=False)}")
            
            return result.get('status') == 0 or result.get('code') == '0000'
            
        except Exception as e:
            print(f"[-] 开门错误: {e}")
            return False


# ============================================================
#                        简单登录函数
# ============================================================

def login(username: str, password: str) -> dict:
    """
    简单的登录函数
    
    参数:
        username: 手机号
        password: 密码
    
    返回:
        成功: {"access_token": "...", "openID": "...", ...}
        失败: None
    
    示例:
        result = login("13800138000", "password123")
        if result:
            print(f"Token: {result['access_token']}")
    """
    url = f"{TOKEN_HOST}/oauth/token"
    
    # Basic Auth 认证头
    auth_string = f"{OAUTH_CLIENT_ID}:{OAUTH_CLIENT_SECRET}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "okhttp/4.9.3",
    }
    
    # 请求参数 - 关键: grant_type 必须是 "multiple"
    data = {
        "grant_type": "multiple",  # 重要: 不是 "password"!
        "username": username,
        "password": password,
    }
    
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=15, verify=False)
        
        if resp.status_code == 200:
            result = resp.json()
            if 'access_token' in result:
                return result
        
        print(f"登录失败: {resp.text}")
        return None
        
    except Exception as e:
        print(f"登录错误: {e}")
        return None


# ============================================================
#                        主程序
# ============================================================

if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    合生活 App 登录工具                        ║
╠══════════════════════════════════════════════════════════════╣
║  使用方法:                                                    ║
║    python hilife_api.py                     # 使用默认账号    ║
║    python hilife_api.py 手机号 密码          # 指定账号       ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # 获取用户名和密码
    if len(sys.argv) >= 3:
        USERNAME = sys.argv[1]
        PASSWORD = sys.argv[2]
    else:
        # 请通过命令行参数传入账号信息
        print("用法: python hilife_api.py <手机号> <密码>")
        print("示例: python hilife_api.py 13800138000 mypassword")
        sys.exit(1)
    
    print(f"[*] 账号: {USERNAME}")
    print(f"[*] 密码: {'*' * len(PASSWORD)}")
    print()
    
    # 方法1: 使用简单函数
    print("=" * 60)
    print("方法1: 使用 login() 函数")
    print("=" * 60)
    
    result = login(USERNAME, PASSWORD)
    if result:
        print(f"\n✅ 登录成功!")
        print(f"   Access Token: {result['access_token']}")
        print(f"   Refresh Token: {result.get('refresh_token', 'N/A')}")
        print(f"   OpenID: {result.get('openID', 'N/A')}")
        print(f"   CustomID: {result.get('customID', 'N/A')}")
        print(f"   过期时间: {result.get('expires_in', 'N/A')} 秒")
    else:
        print("\n❌ 登录失败")
    
    print()
    
    # 方法2: 使用 API 类
    print("=" * 60)
    print("方法2: 使用 HiLifeAPI 类")
    print("=" * 60)
    
    api = HiLifeAPI(USERNAME, PASSWORD)
    if api.login():
        print(f"\n✅ 登录成功!")
        print(f"   可以通过 api.access_token 获取 Token")
        print(f"   可以通过 api.open_id 获取 OpenID")
        
        # 测试获取小区列表
        print("\n" + "=" * 40)
        print("测试: 获取小区列表")
        print("=" * 40)
        communities = api.get_community_list()
        
        # 测试获取门禁列表
        print("\n" + "=" * 40)
        print("测试: 获取门禁列表")
        print("=" * 40)
        # 尝试用获取到的第一个小区ID (如果有)
        cid = None
        if communities and 'data' in communities and communities['data']:
             # 这种结构取决于实际API返回，先简单尝试不传参和传参
             pass
             
        doors = api.get_door_list()
        
        if doors:
            print(f"\n✅ 发现门禁设备!")
            # 简单解析一下门禁信息
            data = doors.get('data', [])
            if isinstance(data, list):
                print(f"   共找到 {len(data)} 个门禁:")
                for door in data:
                    d_id = door.get('doorId') or door.get('id')
                    d_name = door.get('doorName') or door.get('name')
                    print(f"   - [{d_id}] {d_name}")
            else:
                print(f"   数据: {data}")
        else:
            print("\n❌ 未找到门禁设备，请检查 get_door_list 中的接口地址或参数")
    
    # 显示完整的登录请求示例
    print()
    print("=" * 60)
    print("完整的 HTTP 请求示例")
    print("=" * 60)
    print(f"""
POST https://token.91helife.com/oauth/token
Headers:
  Authorization: Basic ZXNuTW9iaWxlQ2xpZW50OmVzbk1vYmlsZQ==
  Content-Type: application/x-www-form-urlencoded
  User-Agent: okhttp/4.9.3

Body:
  grant_type=multiple&username={USERNAME}&password={PASSWORD}

cURL 命令:
  curl -X POST "https://token.91helife.com/oauth/token" \\
    -H "Authorization: Basic ZXNuTW9iaWxlQ2xpZW50OmVzbk1vYmlsZQ==" \\
    -H "Content-Type: application/x-www-form-urlencoded" \\
    -d "grant_type=multiple&username={USERNAME}&password={PASSWORD}"
""")
