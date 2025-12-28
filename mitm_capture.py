# -*- coding: utf-8 -*-
"""
HiLife 抓包参数提取工具
将抓包分析的逻辑封装为类，用于自动探测和提取开门所需的参数
"""
import requests
import base64
import json
import urllib3
urllib3.disable_warnings()

class HiLifeParamSniffer:
    """
    用于探测和提取 HiLife 开门参数的工具类
    """
    def __init__(self, phone: str, password: str):
        self.phone = phone
        self.password = password
        self.access_token = None
        self.user_id = None  # openID
        self.session = requests.Session()
        self.session.verify = False
        
    def login(self) -> bool:
        """登录获取 access_token 和 userId"""
        url = 'https://token.91helife.com/oauth/token'
        auth = base64.b64encode(b'esnMobileClient:esnMobile').decode()
        
        try:
            resp = self.session.post(url, 
                headers={
                    'Authorization': f'Basic {auth}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={
                    'grant_type': 'multiple',
                    'username': self.phone,
                    'password': self.password
                },
                timeout=15
            )
            
            data = resp.json()
            self.access_token = data.get('access_token')
            self.user_id = data.get('openID')
            
            if self.access_token and self.user_id:
                return True
            return False
            
        except Exception as e:
            print(f"登录异常: {e}")
            return False

    def get_card_info(self) -> list:
        """
        获取卡号信息 - 包含 communityId
        这是获取 communityId 的关键 API
        """
        if not self.access_token:
            return []
            
        url = f'https://www.91helife.com/erp/front/interface/door/CardNos/three?access_token={self.access_token}'
        body = {'userId': self.user_id}
        
        try:
            resp = self.session.post(url, 
                headers={'Content-Type': 'application/json'},
                json=body, 
                timeout=10
            )
            
            result = resp.json()
            if result.get('status') == 1:
                return result.get('data', [])
            return []
            
        except Exception as e:
            print(f"获取卡号信息异常: {e}")
            return []

    def get_doors(self, community_id: str, card_no: str) -> list:
        """
        获取门列表 - 包含 doorId (msDoorId)
        这是获取 doorId 的关键 API
        """
        if not self.access_token:
            return []
            
        url = f'https://www.91helife.com/erp/front/interface/es/door/v3/getDoors?access_token={self.access_token}'
        
        body = {
            'communityID': str(community_id),
            'communityId': str(community_id),
            'type': '1',
            'userId': self.user_id,
            'cardNo': card_no,
            'phoneNo': card_no,
            'begin': 1,
            'end': 200,
            'lat': '0',
            'lon': '0',
        }
        
        try:
            resp = self.session.post(url, 
                headers={'Content-Type': 'application/json'},
                json=body, 
                timeout=10
            )
            
            result = resp.json()
            if result.get('status') == 1:
                return result.get('data', {}).get('dataList', [])
            return []
            
        except Exception as e:
            print(f"获取门列表异常: {e}")
            return []

    def sniff_all_params(self) -> list:
        """
        执行完整的探测流程，返回所有可用的开门参数配置
        """
        results = []
        
        print("正在登录...")
        if not self.login():
            print("登录失败")
            return results
            
        print(f"登录成功! UserId: {self.user_id}")
        
        print("正在获取卡信息...")
        cards = self.get_card_info()
        if not cards:
            print("未找到卡信息")
            return results
            
        for card in cards:
            community_id = card.get('communityId')
            door_community_id = card.get('doorCommunityId')
            card_no = card.get('cardNo')
            community_name = card.get('communityName')
            
            print(f"分析小区: {community_name} (ID: {community_id})")
            
            doors = self.get_doors(community_id, card_no)
            if not doors:
                print(f"  在小区 {community_name} 未找到门禁设备")
                continue
                
            for door in doors:
                ms_door_id = door.get('msDoorId')
                door_name = door.get('msDoorName')
                
                # 构造完整的开门参数
                param = {
                    'doorName': door_name,
                    'communityName': community_name,
                    'doorCommunityId': str(door_community_id),
                    'communityId': str(community_id),
                    'doorId': ms_door_id,
                    'cardNo': card_no,
                    'userId': self.user_id,
                    'isScan': 2
                }
                results.append(param)
                print(f"  => 发现门禁: {door_name}")
                
        return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python mitm_capture.py <phone> <password>")
        sys.exit(1)
        
    phone = sys.argv[1]
    password = sys.argv[2]
    
    sniffer = HiLifeParamSniffer(phone, password)
    params = sniffer.sniff_all_params()
    
    if params:
        print("\n" + "="*60)
        print(f"成功提取 {len(params)} 个门禁参数配置")
        print("="*60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
    else:
        print("\n未能提取到任何门禁参数")
