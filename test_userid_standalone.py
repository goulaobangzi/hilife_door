#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
独立测试自动获取 userId 功能
"""
import requests
import base64
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HiLifeApiTest:
    """简化的 HiLife API 测试类"""
    
    def __init__(self, phone: str, password: str):
        self.phone = phone
        self.password = password
        self.access_token = None
        self.user_id = None
        self.session = requests.Session()
        self.session.verify = False
    
    def login(self) -> bool:
        """登录并自动获取 personID"""
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
            open_id = data.get("openID")
            
            if not self.access_token:
                logger.error("未获取到 access_token")
                return False
            
            logger.info(f"获取到 access_token: {self.access_token[:30]}...")
            
            # 2. 使用 access_token 获取 personID
            person_id = self._get_person_id()
            if person_id:
                self.user_id = person_id
                logger.info(f"✅ 自动获取到 personID: {person_id}")
                return True
            else:
                self.user_id = open_id
                logger.warning(f"⚠️ 无法获取 personID，使用 openID: {open_id}")
                return True
                
        except Exception as e:
            logger.error(f"登录错误: {e}")
            return False
    
    def _get_person_id(self) -> str:
        """获取真正的 personID"""
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
                
                # 查找 personID
                if 'data' in result and 'personInfo' in result['data']:
                    person_info = result['data']['personInfo']
                    if 'personID' in person_info:
                        return person_info['personID']
                elif 'data' in result and 'personID' in result['data']:
                    return result['data']['personID']
                elif 'personInfo' in result and 'personID' in result['personInfo']:
                    return result['personInfo']['personID']
                
                logger.debug("未找到 personID")
            
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
            
            if resp.status_code == 200:
                result = resp.json()
                if result.get('status') == 1:
                    return result.get('data', [])
            
        except Exception as e:
            logger.error(f"获取社区列表错误: {e}")
        
        return []

def main():
    print("=" * 60)
    print("HiLife 自动获取 userId 测试")
    print("=" * 60)
    
    # 测试自动获取
    api = HiLifeApiTest("13641086363", "wj521541")
    
    print("\n[步骤 1] 测试登录和自动获取 userId...")
    if api.login():
        print(f"✅ 成功!")
        print(f"   获取到的 userId: {api.user_id}")
        
        # 验证 userId
        if api.user_id == "5498174404738171004":
            print("✅ 这是正确的 personID！")
        elif len(str(api.user_id)) > 30:
            print("⚠️ 这是 openID（临时ID），不是 personID")
        else:
            print(f"❌ 未知的 ID 格式")
        
        # 测试获取社区
        print("\n[步骤 2] 测试获取社区列表...")
        communities = api.get_communities()
        
        if communities:
            print(f"✅ 成功获取 {len(communities)} 个社区:")
            for community in communities:
                print(f"   - {community.get('communityName', '未知')} (ID: {community.get('communityId')})")
        else:
            print("❌ 无法获取社区列表")
            print("   这通常意味着 userId 不正确")
    
    else:
        print("❌ 登录失败")
    
    print("\n" + "=" * 60)
    print("结论：")
    print("1. 如果显示 '正确的 personID'，说明自动获取功能正常")
    print("2. 用户可以在配置时留空 userId")
    print("3. 系统会自动获取并使用正确的 personID")
    print("=" * 60)

if __name__ == '__main__':
    main()
