#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试获取大门列表的问题
"""
import requests
import base64
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HiLifeDoorDebug:
    """调试门禁 API"""
    
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
    
    def get_communities(self) -> list:
        """获取社区列表"""
        if not self.access_token or not self.user_id:
            if not self.login():
                return []
        
        try:
            url = f'https://www.91helife.com/erp/front/interface/door/CardNos/three?access_token={self.access_token}'
            
            resp = self.session.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={'userId': self.user_id},
                timeout=10
            )
            
            logger.debug(f"社区列表响应状态: {resp.status_code}")
            logger.debug(f"社区列表响应: {resp.text}")
            
            if resp.status_code == 200:
                result = resp.json()
                if result.get('status') == 1:
                    return result.get('data', [])
            
        except Exception as e:
            logger.error(f"获取社区列表错误: {e}")
        
        return []
    
    def get_doors(self, community_id: str = None) -> list:
        """获取门禁列表"""
        if not self.access_token or not self.user_id:
            if not self.login():
                return []
        
        # 如果没有提供 community_id，先获取社区列表
        if not community_id:
            communities = self.get_communities()
            if communities:
                community_id = communities[0].get('communityId')
                logger.info(f"使用第一个社区 ID: {community_id}")
            else:
                logger.error("没有找到社区")
                return []
        
        try:
            # 尝试多个可能的 API 端点
            endpoints = [
                f'https://www.91helife.com/erp/front/interface/door/selectList?access_token={self.access_token}',
                f'https://www.91helife.com/erp/front/interface/door/selectAllList?access_token={self.access_token}',
                f'https://www.91helife.com/erp/front/interface/door/doorList?access_token={self.access_token}',
            ]
            
            for endpoint in endpoints:
                logger.info(f"尝试端点: {endpoint}")
                
                # 尝试不同的请求格式
                for data in [
                    {'communityId': community_id, 'userId': self.user_id},
                    {'communityId': community_id},
                    {'userId': self.user_id},
                    {},
                ]:
                    resp = self.session.post(
                        endpoint,
                        headers={'Content-Type': 'application/json'},
                        json=data,
                        timeout=10
                    )
                    
                    logger.debug(f"请求数据: {data}")
                    logger.debug(f"响应状态: {resp.status_code}")
                    logger.debug(f"响应内容: {resp.text[:500]}")
                    
                    if resp.status_code == 200:
                        result = resp.json()
                        # 检查不同的响应格式
                        doors = None
                        if result.get('status') == 1:
                            doors = result.get('data', [])
                        elif 'data' in result:
                            doors = result['data']
                        elif isinstance(result, list):
                            doors = result
                        
                        if doors:
                            logger.info(f"成功获取 {len(doors)} 个门")
                            return doors
            
            logger.error("所有端点都无法获取门列表")
            
        except Exception as e:
            logger.error(f"获取门列表错误: {e}")
        
        return []

def main():
    print("=" * 60)
    print("HiLife 门禁列表调试")
    print("=" * 60)
    
    api = HiLifeDoorDebug("13641086363", "wj521541")
    
    print("\n[步骤 1] 登录...")
    if api.login():
        print(f"✅ 登录成功")
        print(f"   userId: {api.user_id}")
        
        print("\n[步骤 2] 获取社区列表...")
        communities = api.get_communities()
        if communities:
            print(f"✅ 找到 {len(communities)} 个社区:")
            for community in communities:
                print(f"   - {community.get('communityName')} (ID: {community.get('communityId')})")
        else:
            print("❌ 没有找到社区")
            return
        
        print("\n[步骤 3] 获取门禁列表...")
        doors = api.get_doors()
        if doors:
            print(f"✅ 找到 {len(doors)} 个门:")
            for door in doors:
                door_name = door.get('doorName') or door.get('name') or door.get('doorNameStr') or '未知'
                door_id = door.get('doorId') or door.get('id') or door.get('doorID') or '未知'
                print(f"   - {door_name} (ID: {door_id})")
        else:
            print("❌ 没有找到门禁")
            print("\n可能的原因:")
            print("1. API 端点已更改")
            print("2. 需要特定的参数")
            print("3. 账号权限不足")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
