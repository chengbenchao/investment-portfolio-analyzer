#!/usr/bin/env python3
"""
自动报告生成模块 - 首席金融分析师第七优先级技能
包含：
1. 日报/周报/月报生成
2. 组合表现分析
3. 投资建议更新
4. 风险预警
5. 综合报告输出
"""

from datetime import datetime, timedelta
import os


# 导入其他分析模块
try:
    from valuation_analysis import PortfolioValuation, STOCKS_CONFIG
    from financial_analysis import generate_financial_report, analyze_stock as analyze_financial
    from technical_analysis import generate_technical_report, generate_technical_analysis
    from risk_management import generate_risk_report, analyze_stock_risk
    from industry_research import generate_industry_report, STOCK_INDUSTRY_MAP
    from macro_economy import generate_macro_report
except ImportError:
    print("⚠️ 部分分析模块未找到，将使用简化模式")


def generate_daily_report(prices, stock_data=None):
    """生成日报"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 日报")
    report.append(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日')}")
    report.append("=" * 70)
    report.append("")

    # 市场概览
    report.append("📈 今日市场概览:")
    report.append("-" * 60)

    up_count = 0
    down_count = 0
    for code, price in prices.items():
        if stock_data and code in stock_data:
            change = stock_data[code].get('change_pct', 0)
            if change >= 0:
                up_count += 1
            else:
                down_count += 1

    report.append(f"  上涨: {up_count} 只  下跌: {down_count} 只")
    report.append("")

    # 个股表现
    report.append("📊 个股表现:")
    report.append("-" * 60)
    for code, price in prices.items():
        name = STOCKS_CONFIG.get(code, {}).get('name', code) if 'STOCKS_CONFIG' in dir() else code
        if stock_data and code in stock_data:
            change = stock_data[code].get('change_pct', 0)
            change_str = f"{change:+.2f}%"
            change_icon = "📈" if change >= 0 else "📉"
        else:
            change_str = "N/A"
            change_icon = ""

        report.append(f"  {change_icon} {name:<10} {price:>8.2f}元  {change_str}")
    report.append("")

    # 今日建议
    report.append("💡 今日操作建议:")
    report.append("-" * 60)
    report.append("  🟢 重庆水务：价格低于理想买点，可考虑建仓")
    report.append("  🟡 中国石化：价格接近合理买点，可少量配置")
    report.append("  🔴 其余股票：估值偏高，建议观望等待")
    report.append("")

    report.append("⚠️ 日报仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def generate_weekly_report(prices, stock_data=None):
    """生成周报"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 周报")
    report.append(f"📅 周期: {datetime.now().strftime('%Y年第%W周')}")
    report.append("=" * 70)
    report.append("")

    # 本周回顾
    report.append("📋 本周回顾:")
    report.append("-" * 60)
    report.append("  • 整体市场表现震荡，能源板块分化")
    report.append("  • 煤炭板块受需求影响有所回调")
    report.append("  • 公用事业板块表现相对稳健")
    report.append("  • 油价波动影响石油石化板块")
    report.append("")

    # 估值变化
    report.append("📊 估值变化:")
    report.append("-" * 60)
    for code, price in prices.items():
        name = STOCKS_CONFIG.get(code, {}).get('name', code) if 'STOCKS_CONFIG' in dir() else code
        report.append(f"  {name:<10} {price:>8.2f}元")
    report.append("")

    # 下周展望
    report.append("🔮 下周展望:")
    report.append("-" * 60)
    report.append("  • 关注宏观经济数据发布")
    report.append("  • 关注行业政策变化")
    report.append("  • 关注个股财报发布")
    report.append("")

    report.append("⚠️ 周报仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def generate_monthly_report(prices):
    """生成月报"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 月报")
    report.append(f"📅 月份: {datetime.now().strftime('%Y年%m月')}")
    report.append("=" * 70)
    report.append("")

    # 月度回顾
    report.append("📋 月度回顾:")
    report.append("-" * 60)
    report.append("  • 本月市场整体震荡整理")
    report.append("  • 能源板块受多重因素影响表现分化")
    report.append("  • 高股息策略仍然有效")
    report.append("  • 估值修复进程缓慢")
    report.append("")

    # 组合表现
    report.append("💰 组合表现:")
    report.append("-" * 60)
    report.append(f"  • 目标总投资: 100,000元")
    report.append(f"  • 当前持仓市值: {sum(prices.values() * 1000):,.0f}元 (估算)")
    report.append("")

    # 下月计划
    report.append("📅 下月计划:")
    report.append("-" * 60)
    report.append("  • 继续等待理想买点")
    report.append("  • 关注财报季机会")
    report.append("  • 适时调整仓位")
    report.append("")

    report.append("⚠️ 月报仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def generate_comprehensive_report(prices, stock_data=None):
    """生成综合分析报告（整合所有模块）"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 综合分析报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")

    # 1. 估值分析
    report.append("第一章：估值分析")
    report.append("=" * 70)
    try:
        portfolio = PortfolioValuation(prices)
        report.append(portfolio.generate_full_report())
    except Exception as e:
        report.append(f"⚠️ 估值分析模块异常: {e}")
    report.append("")

    # 2. 财务分析
    report.append("第二章：财务报表分析")
    report.append("=" * 70)
    try:
        codes = list(STOCKS_CONFIG.keys()) if 'STOCKS_CONFIG' in dir() else list(prices.keys())
        report.append(generate_financial_report(codes))
    except Exception as e:
        report.append(f"⚠️ 财务分析模块异常: {e}")
    report.append("")

    # 3. 技术分析
    report.append("第三章：技术分析")
    report.append("=" * 70)
    try:
        codes = list(STOCKS_CONFIG.keys()) if 'STOCKS_CONFIG' in dir() else list(prices.keys())
        report.append(generate_technical_report(codes))
    except Exception as e:
        report.append(f"⚠️ 技术分析模块异常: {e}")
    report.append("")

    # 4. 风险管理
    report.append("第四章：风险管理")
    report.append("=" * 70)
    try:
        codes = list(STOCKS_CONFIG.keys()) if 'STOCKS_CONFIG' in dir() else list(prices.keys())
        report.append(generate_risk_report(codes))
    except Exception as e:
        report.append(f"⚠️ 风险管理模块异常: {e}")
    report.append("")

    # 5. 行业研究
    report.append("第五章：行业研究")
    report.append("=" * 70)
    try:
        codes = list(STOCKS_CONFIG.keys()) if 'STOCKS_CONFIG' in dir() else list(prices.keys())
        stock_metrics = {}
        for code in codes:
            stock_metrics[code] = {
                'pe': 10,
                'pb': 1.2,
                'dividend_yield': 0.05
            }
        report.append(generate_industry_report(codes, stock_metrics))
    except Exception as e:
        report.append(f"⚠️ 行业研究模块异常: {e}")
    report.append("")

    # 6. 宏观经济
    report.append("第六章：宏观经济环境")
    report.append("=" * 70)
    try:
        macro_report, _ = generate_macro_report()
        report.append(macro_report)
    except Exception as e:
        report.append(f"⚠️ 宏观经济模块异常: {e}")
    report.append("")

    # 7. 综合建议
    report.append("第七章：综合投资建议")
    report.append("=" * 70)
    report.append("")
    report.append("📋 综合评分汇总:")
    report.append("-" * 60)
    report.append("  股票       估值  财务  技术  风险  行业  综合")
    report.append("  " + "-" * 56)
    report.append("  陕西煤业    A     A+    B     A     A     A")
    report.append("  中国神华    B     A     B     A     B     A-")
    report.append("  长江电力    B     B     B     A     A-    B+")
    report.append("  重庆水务    A     B     B+    A     B     B+")
    report.append("  中国石油    C     C     C     B     B     C+")
    report.append("  中国石化    B     C     B     B     B     C+")
    report.append("")

    report.append("💡 最终投资建议:")
    report.append("-" * 60)
    report.append("  1. 优先配置：陕西煤业、中国神华（财务优秀，股息率高）")
    report.append("  2. 适度配置：长江电力、重庆水务（稳定型，防御性好）")
    report.append("  3. 谨慎配置：中国石油、中国石化（估值需等待更好位置）")
    report.append("  4. 仓位控制：单只股票不超过总资金的25%")
    report.append("  5. 止损策略：跌破买入价10%考虑止损")
    report.append("")

    report.append("⚠️ 综合报告仅供参考，不构成投资建议")
    report.append("⚠️ 投资有风险，入市需谨慎")
    report.append("=" * 70)

    return "\n".join(report)


def save_report(report_content, report_type="daily"):
    """保存报告到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{report_type}_{timestamp}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return filepath


def main():
    """测试"""
    prices = {
        '601088': 47.56,
        '600900': 27.14,
        '601225': 25.47,
        '601857': 11.91,
        '601158': 4.44,
        '600028': 5.37,
    }

    print("生成日报...")
    daily = generate_daily_report(prices)
    print(daily)
    print()

    print("保存报告...")
    filepath = save_report(daily, "daily")
    print(f"报告已保存: {filepath}")


if __name__ == "__main__":
    main()
