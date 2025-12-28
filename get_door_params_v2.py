# -*- coding: utf-8 -*-
"""
获取 HiLife 开门所需的所有参数
演示如何使用 mitm_capture 模块动态获取 communityId, doorId, userId
"""
import json
import sys
from mitm_capture import HiLifeParamSniffer

def main():
    # 配置 - 请替换为你的账号信息
    # 或者通过命令行参数传递: python get_door_params.py <phone> <password>
    phone = 'YOUR_PHONE'
    password = 'YOUR_PASSWORD'
    
    if len(sys.argv) >= 3:
        phone = sys.argv[1]
        password = sys.argv[2]
    
    print("=" * 60)
    print("HiLife 开门参数获取工具")
    print("=" * 60)
    
    if phone == 'YOUR_PHONE':
        print("请编辑脚本填入账号密码，或者使用命令行参数：")
        print("python get_door_params.py <手机号> <密码>")
        return

    # 使用封装好的嗅探器
    sniffer = HiLifeParamSniffer(phone, password)
    
    # 执行探测
    params = sniffer.sniff_all_params()
    
    if not params:
        print("\n❌ 未能获取到开门参数")
        return
    
    # 输出结果
    print("\n" + "=" * 60)
    print("【完整的开门参数】")
    print("=" * 60)
    
    # 打印第一个门的参数作为示例
    if len(params) > 0:
        print(json.dumps(params[0], ensure_ascii=False, indent=2))
        
    if len(params) > 1:
        print(f"\n... 共发现 {len(params)} 个门禁配置")

    print("\n【参数来源说明】")
    print(f"  userId: 来自登录响应的 openID")
    print(f"  communityId: 来自 CardNos API 的 communityId")
    print(f"  doorCommunityId: 来自 CardNos API 的 doorCommunityId")
    print(f"  doorId: 来自 getDoors API 的 msDoorId")
    print(f"  cardNo: 来自 CardNos API 的 cardNo (通常是手机号)")


if __name__ == '__main__':
    main()
