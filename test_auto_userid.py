#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试自动获取 userId 功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

from hilife_door.api import HiLifeApi

def test_auto_userid():
    """测试自动获取 userId"""
    print("=" * 60)
    print("测试自动获取 userId 功能")
    print("=" * 60)
    
    # 创建 API 实例，不传入 userId
    api = HiLifeApi("13641086363", "wj521541", user_id=None)
    
    print("\n[1] 尝试登录并自动获取 userId...")
    if api.login():
        print(f"✅ 登录成功!")
        print(f"   自动获取的 userId: {api.user_id}")
        
        # 验证是否是正确的 personID
        if api.user_id == "5498174404738171004":
            print("✅ 自动获取到正确的 personID!")
        elif api.user_id and len(api.user_id) > 30:
            print("⚠️ 获取到的是 openID（临时ID），不是 personID")
        else:
            print(f"❌ 获取的 userId 格式异常: {api.user_id}")
        
        # 测试获取社区列表
        print("\n[2] 测试获取社区列表...")
        communities = api.get_communities()
        if communities:
            print(f"✅ 成功获取 {len(communities)} 个社区:")
            for community in communities:
                print(f"   - {community.get('name')} (ID: {community.get('id')})")
        else:
            print("❌ 无法获取社区列表")
            
    else:
        print("❌ 登录失败")
        return False
    
    return True

def test_with_manual_userid():
    """测试手动传入 userId"""
    print("\n" + "=" * 60)
    print("测试手动传入正确的 userId")
    print("=" * 60)
    
    # 使用正确的 personID
    api = HiLifeApi("13641086363", "wj521541", user_id="5498174404738171004")
    
    print("\n[1] 使用正确的 personID 登录...")
    if api.login():
        print(f"✅ 登录成功!")
        print(f"   使用的 userId: {api.user_id}")
        
        # 测试获取社区列表
        print("\n[2] 测试获取社区列表...")
        communities = api.get_communities()
        if communities:
            print(f"✅ 成功获取 {len(communities)} 个社区:")
            for community in communities:
                print(f"   - {community.get('name')} (ID: {community.get('id')})")
        else:
            print("❌ 无法获取社区列表")
    else:
        print("❌ 登录失败")

if __name__ == '__main__':
    # 测试自动获取
    success = test_auto_userid()
    
    # 测试手动传入
    test_with_manual_userid()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 自动获取 userId 功能正常!")
        print("用户可以在配置时留空 userId，系统会自动获取。")
    else:
        print("❌ 自动获取功能有问题，需要进一步调试。")
    print("=" * 60)
