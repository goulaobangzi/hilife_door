#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用正确的 API 测试获取门禁列表
"""
import requests
import base64
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HiLifeDoorCorrect:
    """使用正确的 API 地址"""
    
    def __init__(self, phone: str, password: str):
        self.phone = phone
        self.password = password
        self.access_token = None
        self.user_id = None
        self.session = requests.Session()
        self.session.verify = False
    
    def login(self) -> bool:
        """登录并获取 token"""
        try:
            # 1. 获取 access_token
            auth = base64.b64encode(b'esnMobileClient:esnMobile').decode()
            
            resp = self.session.post(
                'https://token.91helife.com/oauth/token',
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "multiple",
                    "username": self.phone,
                    "password": self.password
                },
                timeout=15
            )
            
            if resp.status_code != 200:
                logger.error(f"获取 token 失败: {resp.text}")
                return False
            
            data = resp.json()
            self.access_token = data.get("access_token")
            
            # 2. 获取 personID
            person_id = self._get_person_id()
            if person_id:
                self.user_id = person_id
                logger.info(f"获取到 personID: {person_id}")
            else:
                logger.error("无法获取 personID")
                return False
                
            return True
                
        except Exception as e:
            logger.error(f"登录错误: {e}")
            return False
    
    def _get_person_id(self) -> str:
        """获取 personID"""
        try:
            url = f'https://www.91helife.com/admin/portal/getPersonInfo?access_token={self.access_token}'
            
            resp = self.session.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.91helife.com/',
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                result = resp.json()
                if 'data' in result and 'personInfo' in result['data']:
                    person_info = result['data']['personInfo']
                    if 'personID' in person_info:
                        return person_info['personID']
            
        except Exception as e:
            logger.error(f"获取 personID 错误: {e}")
        
        return None
    
    def get_doors(self, community_id: str = None) -> list:
        """使用正确的 API 获取门禁列表"""
        if not self.access_token or not self.user_id:
            if not self.login():
                return []
        
        # 如果没有提供 community_id，先获取社区列表
        if not community_id:
            communities = self._get_communities()
            if communities:
                community_id = communities[0].get('communityId')
                logger.info(f"自动使用第一个社区 ID: {community_id}")
            else:
                logger.error("没有找到社区")
                return []
        
        # 正确的 API 端点
        url = "https://www.91helife.com/erp/front/interface/es/door/v3/getDoors"
        
        # 准备请求数据 - 使用完整的参数
        data = {
            "communityID": str(community_id),
            "communityId": str(community_id),
            "type": "1",
            "userId": self.user_id,
            "cardNo": self.phone,
            "phoneNo": self.phone,
            "begin": 1,
            "end": 200
        }
        
        try:
            logger.info(f"请求 URL: {url}")
            logger.info(f"请求数据: {data}")
            
            resp = self.session.post(
                url,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                json=data,
                timeout=10
            )
            
            logger.debug(f"响应状态: {resp.status_code}")
            logger.debug(f"响应内容: {resp.text}")
            
            if resp.status_code == 200:
                result = resp.json()
                
                # 检查响应格式
                if result.get('status') == 1 or result.get('code') == '200' or result.get('code') == '0101':
                    # 尝试多种数据位置
                    doors = None
                    
                    # 位置1: data.dataList
                    if 'data' in result and 'dataList' in result['data']:
                        doors = result['data']['dataList']
                    # 位置2: data
                    elif 'data' in result:
                        doors = result['data']
                    # 位置3: 直接是列表
                    elif isinstance(result, list):
                        doors = result
                    
                    if doors and isinstance(doors, list):
                        return doors
                
                logger.error(f"未找到门列表数据: {result}")
            else:
                logger.error(f"请求失败: {resp.status_code} - {resp.text}")
            
        except Exception as e:
            logger.error(f"获取门列表错误: {e}")
        
        return []
    
    def _get_communities(self) -> list:
        """获取社区列表"""
        try:
            url = f'https://www.91helife.com/erp/front/interface/door/CardNos/three?access_token={self.access_token}'
            
            resp = self.session.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={'userId': self.user_id},
                timeout=10
            )
            
            if resp.status_code == 200:
                result = resp.json()
                if result.get('status') == 1:
                    return result.get('data', [])
            
        except Exception as e:
            logger.error(f"获取社区列表错误: {e}")
        
        return []

def main():
    print("=" * 60)
    print("使用正确的 API 测试门禁列表")
    print("=" * 60)
    
    api = HiLifeDoorCorrect("13641086363", "wj521541")
    
    print("\n[步骤 1] 登录...")
    if api.login():
        print(f"✅ 登录成功")
        print(f"   userId: {api.user_id}")
        
        print("\n[步骤 2] 获取门禁列表...")
        doors = api.get_doors()
        
        if doors:
            print(f"✅ 成功获取 {len(doors)} 个门:")
            for i, door in enumerate(doors, 1):
                door_name = door.get('doorName') or door.get('name') or door.get('doorNameStr') or f'门禁 {i}'
                door_id = door.get('doorId') or door.get('id') or door.get('doorID') or f'ID_{i}'
                print(f"   {i}. {door_name}")
                print(f"      ID: {door_id}")
                print(f"      详细信息: {json.dumps(door, ensure_ascii=False, indent=6)}")
        else:
            print("❌ 没有找到门禁")
            print("\n可能的原因:")
            print("1. API 参数格式不正确")
            print("2. 需要先选择社区")
            print("3. 账号没有门禁权限")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
