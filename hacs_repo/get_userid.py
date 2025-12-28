#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HiLife userId 获取工具
无需验证码，直接获取 personID
"""
import requests
import base64
import urllib3
urllib3.disable_warnings()

def get_person_id(phone: str, password: str) -> str:
    """获取 PersonID"""
    print("正在获取 PersonID...")
    
    # 1. 获取 access_token
    print("[1/2] 获取 access_token...")
    token_url = 'https://token.91helife.com/oauth/token'
    auth = base64.b64encode(b'esnMobileClient:esnMobile').decode()
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = {
        'grant_type': 'multiple',
        'username': phone,
        'password': password
    }
    
    try:
        resp = requests.post(token_url, headers=headers, data=data, verify=False, timeout=15)
        if resp.status_code != 200:
            print(f"获取 token 失败: {resp.text}")
            return None
            
        token_data = resp.json()
        access_token = token_data.get('access_token')
        open_id = token_data.get('openID')
        
        if not access_token:
            print("获取 access_token 失败")
            return None
            
        print(f"✓ access_token: {access_token[:30]}...")
        
    except Exception as e:
        print(f"获取 token 错误: {e}")
        return None
    
    # 2. 使用 token 获取 PersonID
    print("[2/2] 获取 PersonID...")
    person_url = f'https://www.91helife.com/admin/portal/getPersonInfo?access_token={access_token}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.91helife.com/',
    }
    
    try:
        resp = requests.get(person_url, headers=headers, verify=False, timeout=10)
        if resp.status_code != 200:
            print(f"获取 PersonID 失败: {resp.text}")
            return None
            
        result = resp.json()
        
        # 从响应中提取 PersonID - 检查多个可能的位置
        person_id = None
        
        # 位置1: data.personInfo.personID
        if 'data' in result and 'personInfo' in result['data']:
            person_info = result['data']['personInfo']
            if 'personID' in person_info:
                person_id = person_info['personID']
        
        # 位置2: data.personID
        elif 'data' in result and 'personID' in result['data']:
            person_id = result['data']['personID']
        
        # 位置3: personInfo.personID
        elif 'personInfo' in result and 'personID' in result['personInfo']:
            person_id = result['personInfo']['personID']
        
        if person_id:
            print(f"✓ PersonID: {person_id}")
            return person_id
        else:
            print("响应中未找到 PersonID")
            # 打印响应结构以便调试
            print("响应结构:")
            if 'data' in result:
                print("- data keys:", list(result['data'].keys()) if isinstance(result['data'], dict) else type(result['data']))
                if 'personInfo' in result['data']:
                    print("- personInfo keys:", list(result['data']['personInfo'].keys()) if isinstance(result['data']['personInfo'], dict) else type(result['data']['personInfo']))
            return None
            
    except Exception as e:
        print(f"获取 PersonID 错误: {e}")
        return None

def main():
    # 使用 .credentials 中的账号
    phone = '13641086363'
    password = 'wj521541'
    
    print("=" * 50)
    print("HiLife PersonID 获取工具")
    print("=" * 50)
    
    person_id = get_person_id(phone, password)
    
    if person_id:
        print("\n" + "=" * 50)
        print(f"✅ 成功获取 PersonID: {person_id}")
        print("=" * 50)
        print("\n这个 PersonID 可以用于 Home Assistant 配置")
    else:
        print("\n❌ 获取失败")
        print("\n请检查：")
        print("1. 账号密码是否正确")
        print("2. 网络连接是否正常")

if __name__ == '__main__':
    main()
