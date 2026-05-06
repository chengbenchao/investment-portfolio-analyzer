#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试交易时间判断
"""

from datetime import datetime, time as dt_time

def is_trading_time():
    """
    判断当前是否为A股交易时间
    """
    now = datetime.now()
    current_time = now.time()
    
    # 检查是否为周末
    if now.weekday() >= 5:  # 0=周一, 5=周六, 6=周日
        return False
    
    # 上午时段：9:30 - 11:30
    morning_start = dt_time(9, 30, 0)
    morning_end = dt_time(11, 30, 0)
    
    # 下午时段：13:00 - 15:00
    afternoon_start = dt_time(13, 0, 0)
    afternoon_end = dt_time(15, 0, 0)
    
    if morning_start <= current_time <= morning_end:
        return True
    if afternoon_start <= current_time <= afternoon_end:
        return True
    
    return False

def get_trading_time_info():
    """
    获取交易时间信息
    """
    now = datetime.now()
    current_time = now.time()
    
    info = {
        'now': now.strftime('%Y-%m-%d %H:%M:%S'),
        'is_trading': is_trading_time(),
        'weekday': now.strftime('%A'),
        'next_trading': ''
    }
    
    if now.weekday() >= 5:
        info['next_trading'] = '下周一'
    elif current_time < dt_time(9, 30, 0):
        info['next_trading'] = '今天 9:30'
    elif current_time < dt_time(13, 0, 0):
        info['next_trading'] = '今天 13:00'
    elif current_time < dt_time(15, 0, 0):
        info['next_trading'] = '现在（交易中）'
    else:
        info['next_trading'] = '明天 9:30'
    
    return info

# 测试
if __name__ == '__main__':
    info = get_trading_time_info()
    
    print("=" * 70)
    print("🕐 A股交易时间测试")
    print("=" * 70)
    print(f"\n📅 当前时间: {info['now']}")
    print(f"📆 星期: {info['weekday']}")
    
    if info['is_trading']:
        print(f"\n✅ 当前是交易时间！")
    else:
        print(f"\n⏸️ 当前是非交易时间")
        print(f"🕐 下次交易: {info['next_trading']}")
    
    print(f"\n💡 A股交易时间:")
    print(f"   - 9:30 - 11:30 (上午)")
    print(f"   - 13:00 - 15:00 (下午)")
    print(f"   - 周末休市")
    print("\n" + "=" * 70)
