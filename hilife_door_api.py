# -*- coding: utf-8 -*-
"""
HiLife 合生活 开门 API
基于 mitmproxy 抓包分析

使用方法:
    python hilife_door_api.py

配置:
    修改 CONFIG 中的手机号和密码
"""
import requests
import base64
import json
import urllib3
urllib3.disable_warnings()

# ============ 配置 ============
# 请替换为你的账号信息
CONFIG = {
    'phone': 'YOUR_PHONE',
    'password': 'YOUR_PASSWORD',
    'user_id': '',  # 可留空，自动获取
    'community_id': 'YOUR_COMMUNITY_ID',  # 从 CardNos API 获取
}

# ============ API 端点 ============
API = {
    'login': 'https://token.91helife.com/oauth/token',
    'open_door': 'https://www.91helife.com/erp/front/interface/door/openDoor/three',
    'get_doors': 'https://www.91helife.com/erp/front/interface/es/door/v3/getDoors',
    'get_cards': 'https://www.91helife.com/erp/front/interface/door/CardNos/three',
}

# ============ 门列表 ============
# 门列表会通过 API 自动获取，这里是示例格式
DOORS = {
    # '门名称': {'msDoorId': 9001xxxx, 'id': xxxx},
}


class HiLifeDoorAPI:
    """HiLife 开门 API 封装"""
    
    def __init__(self, phone: str, password: str):
        self.phone = phone
        self.password = password
        self.access_token = None
        self.user_id = CONFIG.get('user_id')
        self.community_id = CONFIG['community_id']
    
    def login(self) -> bool:
        """登录获取 access_token"""
        auth = base64.b64encode(b'esnMobileClient:esnMobile').decode()
        
        resp = requests.post(
            API['login'],
            headers={
                'Authorization': f'Basic {auth}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'multiple',
                'username': self.phone,
                'password': self.password
            },
            verify=False,
            timeout=15
        )
        
        if resp.status_code == 200:
            data = resp.json()
            self.access_token = data.get('access_token')
            
            # 自动获取 user_id
            if not self.user_id:
                self.user_id = data.get('openID')
                if self.user_id:
                    print(f"已自动获取 User ID: {self.user_id}")
            
            return bool(self.access_token)
        return False
    
    def get_doors(self) -> list:
        """获取门列表"""
        if not self.access_token:
            if not self.login():
                return []
        
        url = f"{API['get_doors']}?access_token={self.access_token}"
        
        body = {
            'lon': '116.410344',
            'lat': '39.916296',
            'end': 200,
            'begin': 1,
            'communityID': self.community_id,
            'communityId': self.community_id,
            'type': '1',
            'userId': self.user_id,
            'cardNo': self.phone,
            'phoneNo': self.phone,
        }
        
        resp = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=UTF-8'
            },
            json=body,
            verify=False,
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 1:
                return data.get('data', {}).get('dataList', [])
        return []
    
    def open_door(self, door_name: str, door_id: int) -> dict:
        """
        开门
        
        Args:
            door_name: 门名称
            door_id: 门 ID (msDoorId 格式，如 90012284)
        
        Returns:
            API 响应
        """
        if not self.access_token:
            if not self.login():
                return {'status': -1, 'msg': '登录失败'}
        
        url = f"{API['open_door']}?access_token={self.access_token}"
        
        body = {
            'doorName': door_name,
            'doorCommunityId': self.community_id,
            'communityId': self.community_id,
            'doorId': door_id,
            'cardNo': self.phone,
            'userId': self.user_id,
            'isScan': 2,
        }
        
        resp = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=UTF-8'
            },
            json=body,
            verify=False,
            timeout=10
        )
        
        if resp.status_code == 200:
            return resp.json()
        return {'status': -1, 'msg': f'HTTP {resp.status_code}'}
    
    def open_door_by_name(self, door_name: str) -> dict:
        """
        通过门名称开门
        
        Args:
            door_name: 门名称 (需要在 DOORS 字典中)
        
        Returns:
            API 响应
        """
        if door_name not in DOORS:
            return {'status': -1, 'msg': f'未知的门: {door_name}'}
        
        door_info = DOORS[door_name]
        return self.open_door(door_name, door_info['msDoorId'])


def main():
    """主函数"""
    api = HiLifeDoorAPI(CONFIG['phone'], CONFIG['password'])
    
    # 登录
    print("登录中...")
    if not api.login():
        print("登录失败")
        return
    print(f"登录成功，access_token: {api.access_token[:20]}...")
    
    # 获取门列表
    print("\n获取门列表...")
    doors = api.get_doors()
    print(f"找到 {len(doors)} 个门:")
    for door in doors[:5]:
        print(f"  - {door.get('msDoorName')} (ID: {door.get('msDoorId')})")
    
    # 开门测试
    print("\n" + "=" * 50)
    door_name = '珠江愉景家园西区26#楼大堂门'
    print(f"开门: {door_name}")
    result = api.open_door_by_name(door_name)
    print(f"结果: {json.dumps(result, ensure_ascii=False)}")
    
    if result.get('status') == 1:
        print("✅ 开门成功！")
    else:
        print(f"❌ 开门失败: {result.get('msg')}")


if __name__ == '__main__':
    main()
