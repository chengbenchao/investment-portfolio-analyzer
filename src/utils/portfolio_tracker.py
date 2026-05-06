#!/usr/bin/env python3
"""
投资组合跟踪工具
用于记录交易、分红，查看持仓和收益
"""

import json
import csv
import os
from datetime import datetime

PORTFOLIO_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PORTFOLIO_DIR, 'portfolio_config.json')
TRANSACTIONS_FILE = os.path.join(PORTFOLIO_DIR, 'transactions.csv')
DIVIDENDS_FILE = os.path.join(PORTFOLIO_DIR, 'dividends.csv')
HOLDINGS_FILE = os.path.join(PORTFOLIO_DIR, 'holdings.csv')


def load_config():
    """加载投资组合配置"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_transaction(stock_code, stock_name, action, price, quantity, notes=""):
    """添加交易记录"""
    amount = round(price * quantity, 2)
    date = datetime.now().strftime('%Y-%m-%d')
    
    with open(TRANSACTIONS_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, stock_code, stock_name, action, price, quantity, amount, notes])
    
    print(f"✅ 已记录交易: {action} {stock_name} {quantity}股 @ {price}元, 总额 {amount}元")


def add_dividend(stock_code, stock_name, dividend_per_share, quantity, tax=0, notes=""):
    """添加分红记录"""
    total_amount = round(dividend_per_share * quantity, 2)
    net_amount = round(total_amount - tax, 2)
    date = datetime.now().strftime('%Y-%m-%d')
    
    with open(DIVIDENDS_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, stock_code, stock_name, dividend_per_share, quantity, total_amount, tax, net_amount, notes])
    
    print(f"✅ 已记录分红: {stock_name} 每股 {dividend_per_share}元, 总计 {total_amount}元 (税后 {net_amount}元)")


def show_portfolio():
    """显示投资组合概览"""
    config = load_config()
    
    print("\n" + "="*60)
    print("📊 投资组合概览")
    print("="*60)
    print(f"组合名称: {config['portfolio_name']}")
    print(f"目标总投资: {config['total_investment']:,}元")
    print()
    
    print("🎯 6只精选股票:")
    print("-"*80)
    print(f"{'股票名称':<10} {'代码':<8} {'目标金额':>10} {'理想买点':>8} {'合理买点':>8} {'预期股息率':>10}")
    print("-"*80)
    
    for stock in config['stocks']:
        print(f"{stock['name']:<10} {stock['code']:<8} {stock['target_amount']:>10,} {stock['ideal_buy_price']:>8} {stock['reasonable_buy_price']:>8} {stock['expected_dividend_yield']:>10}")
    
    print()
    print("📅 建仓计划:")
    for phase in config['purchase_plan']:
        print(f"  {phase['phase']}: {phase['timing']} - {phase['amount']:,}元 ({phase['percentage']*100:.0f}%)")
    
    print("\n" + "="*60)


def show_transactions():
    """显示交易记录"""
    print("\n" + "="*60)
    print("📝 交易记录")
    print("="*60)
    
    if os.path.getsize(TRANSACTIONS_FILE) <= 62:  # 只有标题行
        print("暂无交易记录")
        return
    
    with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"{'日期':<12} {'股票':<10} {'操作':<6} {'价格':>8} {'数量':>8} {'金额':>12} {'备注':<15}")
        print("-"*80)
        
        for row in reader:
            print(f"{row['date']:<12} {row['stock_name']:<10} {row['action']:<6} {float(row['price']):>8.2f} {int(row['quantity']):>8} {float(row['amount']):>12.2f} {row['notes']:<15}")


def show_dividends():
    """显示分红记录"""
    print("\n" + "="*60)
    print("💰 分红记录")
    print("="*60)
    
    if os.path.getsize(DIVIDENDS_FILE) <= 89:  # 只有标题行
        print("暂无分红记录")
        return
    
    with open(DIVIDENDS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"{'日期':<12} {'股票':<10} {'每股分红':>10} {'数量':>8} {'总分红':>12} {'税额':>8} {'税后':>12}")
        print("-"*80)
        
        for row in reader:
            print(f"{row['date']:<12} {row['stock_name']:<10} {float(row['dividend_per_share']):>10.2f} {int(row['quantity']):>8} {float(row['total_amount']):>12.2f} {float(row['tax']):>8.2f} {float(row['net_amount']):>12.2f}")


def check_price_alert(current_prices=None):
    """检查价格提醒"""
    config = load_config()
    
    print("\n" + "="*60)
    print("🔔 价格提醒检查")
    print("="*60)
    
    if current_prices:
        print("(使用提供的当前价格)")
    else:
        print("(请输入当前价格进行检查)")
        return
    
    print("\n价格检查结果:")
    print("-"*60)
    
    for stock in config['stocks']:
        current = current_prices.get(stock['code'])
        if current:
            if current <= stock['ideal_buy_price']:
                print(f"🟢 {stock['name']} ({stock['code']}): {current}元 - 理想买点！建议买入")
            elif current <= stock['reasonable_buy_price']:
                print(f"🟡 {stock['name']} ({stock['code']}): {current}元 - 合理买点，可以买入")
            elif current <= stock['cautious_buy_price']:
                print(f"🟠 {stock['name']} ({stock['code']}): {current}元 - 谨慎买点，少量配置")
            else:
                print(f"🔴 {stock['name']} ({stock['code']}): {current}元 - 价格偏高，建议观望")


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) == 1 or sys.argv[1] in ['help', '-h', '--help']:
        print("""
📊 投资组合跟踪工具

使用方法:
  python portfolio_tracker.py              - 显示组合概览
  python portfolio_tracker.py portfolio    - 显示组合概览
  python portfolio_tracker.py transactions - 显示交易记录
  python portfolio_tracker.py dividends    - 显示分红记录
  
交互使用:
  python portfolio_tracker.py

示例:
  # 添加买入记录
  # (需要修改脚本使用add_transaction函数)
        """)
        show_portfolio()
        return
    
    command = sys.argv[1]
    
    if command in ['portfolio', 'show']:
        show_portfolio()
    elif command in ['transactions', 'tx']:
        show_transactions()
    elif command in ['dividends', 'div']:
        show_dividends()
    else:
        print(f"未知命令: {command}")
        print("使用 'help' 查看帮助")


if __name__ == '__main__':
    main()
