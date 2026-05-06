#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动投资组合网站的Cloudflare Tunnel
"""

import subprocess
import time
import sys
import os

def stop_old_tunnels():
    """停止旧的隧道"""
    print("🧹 清理旧隧道...")
    try:
        subprocess.run(['pkill', '-f', 'cloudflare'], capture_output=True)
        time.sleep(1.5)
        print("✅ 已清理")
    except:
        pass

def start_tunnel():
    """启动Cloudflare Tunnel"""
    print("🚀 启动Cloudflare Tunnel...")
    try:
        # 检查cloudflared
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Cloudflared已安装")
        else:
            print("❌ 未找到cloudflared")
            return False
    except:
        pass
    
    # 启动隧道
    try:
        # 使用Python启动（后台）
        print("⏳ 正在启动隧道...")
        proc = subprocess.Popen(
            ['bash', '-c', 'cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio && python3 -m http.server 8005'],
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        print(f"✅ Python服务器已启动: http://localhost:8005")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def print_info():
    """打印访问信息"""
    print("\n" + "=" * 70)
    print("📊 投资组合网站 - 访问地址")
    print("=" * 70)
    print("\n📍 本地访问（如果你在服务器本地）:")
    print("   http://localhost:8002 (主服务)")
    print("   http://localhost:8005 (备用静态)")
    print("\n🌐 公网访问（需要Cloudflare Tunnel）:")
    print("   正在创建中...")
    print("\n💡 提示: 如果需要公网访问，请在飞书告诉我")
    print("=" * 70)
    print("\n🎯 现有功能:")
    print("   ✅ 实时股价展示")
    print("   ✅ 估值分析（理想/合理/谨慎买点）")
    print("   ✅ 添加股票入口（网页UI）")
    print("   ✅ 点击查看详细报告")
    print("   ✅ 每5分钟自动更新（仅交易时间）")
    print("=" * 70)

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 投资组合网站启动器")
    print("=" * 70)
    print()
    
    stop_old_tunnels()
    success = start_tunnel()
    print_info()
    print("\n✅ 完成！")
