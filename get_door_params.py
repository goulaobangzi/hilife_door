# -*- coding: utf-8 -*-
"""
获取 HiLife 开门所需的所有参数
演示如何动态获取 communityId, doorId, userId
"""
import requests
import base64
import json
import urllib3
urllib3.disable_warnings()


def login(phone: str, password: str) -> dict:
    """登录获取 access_token 和 userId"""
    url = 'https://token.91helife.com/oauth/token'
    auth = base64.b64encode(b'esnMobileClient:esnMobile').decode()
    
    resp = requests.post(url, 
        headers={
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'multiple',
            'username': phone,
            'password': password
        },
        verify=False, timeout=15
    )
    return resp.json()


def get_person_id(access_token: str) -> str:
    """
    获取 personId (pID) - 这是开门 API 需要的 userId
    
    通过 accesscontrol API 获取
    """
    # 先尝试从 queryOpenTypes 获取
    url = f'https://www.91helife.com/accesscontrol/AccessControlMobile/queryOpenTypes?access_token={access_token}'
    
    resp = requests.get(url, verify=False, timeout=10)
    # 这个 API 可能不返回 personId，但可以验证 token 有效
    
    return None  # 需要从其他地方获取


def get_card_info(access_token: str, user_id: str) -> list:
    """
    获取卡号信息 - 包含 communityId
    
    这是获取 communityId 的关键 API！
    
    注意: user_id 应该是 personId (pID)，不是登录返回的 openID
    """
    url = f'https://www.91helife.com/erp/front/interface/door/CardNos/three?access_token={access_token}'
    body = {'userId': user_id}
    
    resp = requests.post(url, 
        headers={'Content-Type': 'application/json'},
        json=body, verify=False, timeout=10
    )
    
    result = resp.json()
    print(f"  CardNos API 响应: {json.dumps(result, ensure_ascii=False)[:200]}")
    if result.get('status') == 1:
        return result.get('data', [])
    return []


def get_doors(access_token: str, user_id: str, community_id: str, card_no: str) -> list:
    """
    获取门列表 - 包含 doorId (msDoorId)
    
    这是获取 doorId 的关键 API！
    """
    url = f'https://www.91helife.com/erp/front/interface/es/door/v3/getDoors?access_token={access_token}'
    
    body = {
        'communityID': str(community_id),
        'communityId': str(community_id),
        'type': '1',
        'userId': user_id,
        'cardNo': card_no,
        'phoneNo': card_no,
        'begin': 1,
        'end': 200,
        'lat': '0',
        'lon': '0',
    }
    
    resp = requests.post(url, 
        headers={'Content-Type': 'application/json'},
        json=body, verify=False, timeout=10
    )
    
    result = resp.json()
    if result.get('status') == 1:
        return result.get('data', {}).get('dataList', [])
    return []


def main():
    # 配置 - 使用 .credentials 中的账号信息
    phone = '13641086363'
    password = 'wj521541'
    
    print("=" * 60)
    print("HiLife 开门参数获取工具")
    print("=" * 60)
    
    # 1. 登录
    print("\n【步骤 1】登录...")
    token_data = login(phone, password)
    
    access_token = token_data.get('access_token')
    user_id = token_data.get('openID')  # 这就是 userId！
    
    if not access_token:
        print("登录失败！")
        return
    
    print(f"  ✅ access_token: {access_token[:30]}...")
    print(f"  ✅ userId (openID): {user_id}")
    
    # 2. 获取卡号信息 (包含 communityId)
    print("\n【步骤 2】获取卡号信息...")
    cards = get_card_info(access_token, user_id)
    
    if not cards:
        print("  ❌ 获取卡号信息失败")
        return
    
    print(f"  找到 {len(cards)} 张卡:")
    for card in cards:
        print(f"    - 卡号: {card.get('cardNo')}")
        print(f"      小区: {card.get('communityName')}")
        print(f"      communityId: {card.get('communityId')}")
        print(f"      doorCommunityId: {card.get('doorCommunityId')}")
    
    # 使用第一张卡的信息
    card = cards[0]
    community_id = card.get('communityId')
    door_community_id = card.get('doorCommunityId')
    card_no = card.get('cardNo')
    
    # 3. 获取门列表 (包含 doorId)
    print(f"\n【步骤 3】获取门列表 (communityId: {community_id})...")
    doors = get_doors(access_token, user_id, community_id, card_no)
    
    if not doors:
        print("  ❌ 获取门列表失败")
        return
    
    print(f"  找到 {len(doors)} 个门:")
    for door in doors:
        ms_door_id = door.get('msDoorId')
        door_name = door.get('msDoorName')
        print(f"    - {door_name}")
        print(f"      doorId (msDoorId): {ms_door_id}")
    
    # 4. 输出完整的开门参数
    print("\n" + "=" * 60)
    print("【完整的开门参数】")
    print("=" * 60)
    
    door = doors[0]  # 使用第一个门作为示例
    
    params = {
        'doorName': door.get('msDoorName'),
        'doorCommunityId': str(door_community_id),
        'communityId': str(community_id),
        'doorId': door.get('msDoorId'),
        'cardNo': card_no,
        'userId': user_id,
        'isScan': 2
    }
    
    print(json.dumps(params, ensure_ascii=False, indent=2))
    
    print("\n【参数来源说明】")
    print(f"  userId: 来自登录响应的 openID")
    print(f"  communityId: 来自 CardNos API 的 communityId")
    print(f"  doorCommunityId: 来自 CardNos API 的 doorCommunityId")
    print(f"  doorId: 来自 getDoors API 的 msDoorId")
    print(f"  cardNo: 来自 CardNos API 的 cardNo (通常是手机号)")


if __name__ == '__main__':
    main()
