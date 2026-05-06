#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查服务状态
"""

import subprocess
import os

def check_port(port):
    """检查端口是否在运行"""
    try:
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    print("=" * 70)
    print("📊 服务状态检查")
    print("=" * 70)
    
    ports = [8000, 8001, 8002]
    
    print()
    for port in ports:
        status = "✅ 在运行" if check_port(port) else "❌ 未运行"
        project = "A股投资组合" if port == 8000 else "Vibe-Trading" if port == 8001 else "其他"
        print(f"{port:5d} - {project}: {status}")
    
    print()
    print("=" * 70)
    print("🌐 获取Cloudflare Tunnel地址的方法")
    print("=" * 70)
    print()
    print("📝 方法1：手动启动（推荐）")
    print("   cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio")
    print("   cloudflared tunnel --url http://localhost:8000")
    print()
    print("💡 执行后，Tunnel会显示一个类似这样的地址：")
    print("   https://random-name.trycloudflare.com")
    print()
    print("=" * 70)
    print("📍 本地访问地址")
    print("=" * 70)
    print()
    print("   A股投资组合: http://localhost:8000")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
