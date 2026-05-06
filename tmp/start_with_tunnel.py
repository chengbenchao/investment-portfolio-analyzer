#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动A股投资组合和Cloudflare Tunnel
"""

import subprocess
import time
import os

def cleanup():
    """清理旧进程"""
    print("🧹 清理旧进程...")
    subprocess.run(['pkill', '-f', 'cloudflare'], capture_output=True)
    subprocess.run(['pkill', '-f', 'python3.*http.server'], capture_output=True)
    subprocess.run(['pkill', '-f', 'python.*investment'], capture_output=True)
    time.sleep(2)

def start_server():
    """启动Python HTTP服务器"""
    project_path = '/root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio'
    os.chdir(project_path)
    
    print("🚀 启动A股投资组合（8000端口）...")
    subprocess.Popen(['python3', '-m', 'http.server', '8000'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    return True

def main():
    print("=" * 70)
    print("🚀 启动A股投资组合服务")
    print("=" * 70)
    
    # 清理旧进程
    cleanup()
    
    # 启动服务器
    start_server()
    
    # 显示信息
    print()
    print("=" * 70)
    print("📊 服务状态")
    print("=" * 70)
    print()
    print("📍 本地访问: http://localhost:8000")
    print()
    print("🌐 公网访问: 请手动运行以下命令获取地址")
    print()
    print("   cloudflared tunnel --url http://localhost:8000")
    print()
    print("💡 执行后，Tunnel会显示一个类似这样的地址：")
    print("   https://random-name.trycloudflare.com")
    print()
    print("=" * 70)
    print("🎯 提示")
    print("=" * 70)
    print()
    print("🔄 这个会话结束，Tunnel也会停止")
    print("📝 下次需要重新启动Tunnel")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
