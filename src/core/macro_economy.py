#!/usr/bin/env python3
"""
宏观经济分析模块 - 首席金融分析师第六优先级技能
包含：
1. GDP、CPI、PPI跟踪
2. 利率与货币政策分析
3. 财政政策影响
4. 国际经济环境
5. 宏观环境评分
"""

from datetime import datetime


# 宏观经济数据（模拟，实际应从国家统计局/央行获取）
MACRO_DATA = {
    "gdp": {
        "current_quarter": "2026Q1",
        "growth_yoy": 0.048,  # GDP同比增速 4.8%
        "growth_qoq": 0.012,  # GDP环比增速 1.2%
        "trend": "stable",  # accelerating/stable/decelerating
    },
    "cpi": {
        "current": 0.018,  # CPI同比 1.8%
        "trend": "rising",
        "core_cpi": 0.015,
    },
    "ppi": {
        "current": -0.012,  # PPI同比 -1.2%
        "trend": "recovering",
    },
    "interest_rate": {
        "lpr_1y": 0.0310,  # 1年期LPR 3.10%
        "lpr_5y": 0.0360,  # 5年期LPR 3.60%
        "mlf": 0.0250,     # MLF利率 2.50%
        "trend": "cutting",  # cutting/stable/hiking
    },
    "money_supply": {
        "m2_growth": 0.085,  # M2增速 8.5%
        "social_financing": 0.092,  # 社融增速 9.2%
    },
    "fiscal": {
        "deficit_ratio": 0.035,  # 财政赤字率 3.5%
        "special_bonds": "3.8万亿",
        "policy_stance": "expansionary",  # expansionary/neutral/tight
    },
    "international": {
        "fed_rate": 0.0450,  # 美联储利率 4.50%
        "usd_cny": 7.15,     # 美元兑人民币
        "brent_oil": 75.50,  # 布伦特原油价格
        "global_growth": 0.032,  # 全球增速 3.2%
    },
}


def analyze_growth_environment():
    """分析经济增长环境"""
    gdp = MACRO_DATA['gdp']
    signals = []
    score = 50

    if gdp['growth_yoy'] > 0.05:
        signals.append(f"🟢 GDP增速 {gdp['growth_yoy']*100:.1f}%，经济强劲")
        score += 20
    elif gdp['growth_yoy'] > 0.04:
        signals.append(f"🟡 GDP增速 {gdp['growth_yoy']*100:.1f}%，经济稳健")
        score += 10
    else:
        signals.append(f"🔴 GDP增速 {gdp['growth_yoy']*100:.1f}%，经济承压")
        score -= 10

    if gdp['trend'] == "accelerating":
        signals.append("📈 经济加速")
        score += 10
    elif gdp['trend'] == "decelerating":
        signals.append("📉 经济减速")
        score -= 10

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_inflation_environment():
    """分析通胀环境"""
    cpi = MACRO_DATA['cpi']
    ppi = MACRO_DATA['ppi']
    signals = []
    score = 50

    if 0.01 < cpi['current'] < 0.03:
        signals.append(f"🟢 CPI {cpi['current']*100:.1f}%，温和通胀（理想区间）")
        score += 15
    elif cpi['current'] > 0.03:
        signals.append(f"🔴 CPI {cpi['current']*100:.1f}%，通胀偏高")
        score -= 10
    elif cpi['current'] < 0:
        signals.append(f"🔴 CPI {cpi['current']*100:.1f}%，通缩风险")
        score -= 15
    else:
        signals.append(f"🟡 CPI {cpi['current']*100:.1f}%，低通胀")
        score += 5

    if ppi['current'] < 0:
        signals.append(f"📉 PPI {ppi['current']*100:.1f}%，工业品价格承压")
        score -= 5
    else:
        signals.append(f"📈 PPI {ppi['current']*100:.1f}%，工业品价格回升")
        score += 5

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_monetary_policy():
    """分析货币政策"""
    rate = MACRO_DATA['interest_rate']
    money = MACRO_DATA['money_supply']
    signals = []
    score = 50

    if rate['trend'] == "cutting":
        signals.append(f"🟢 降息周期 (1Y LPR {rate['lpr_1y']*100:.2f}%)")
        score += 15
    elif rate['trend'] == "hiking":
        signals.append(f"🔴 加息周期 (1Y LPR {rate['lpr_1y']*100:.2f}%)")
        score -= 15
    else:
        signals.append(f"🟡 利率稳定 (1Y LPR {rate['lpr_1y']*100:.2f}%)")
        score += 5

    if money['m2_growth'] > 0.08:
        signals.append(f"💰 M2增速 {money['m2_growth']*100:.1f}%，流动性充裕")
        score += 10
    else:
        signals.append(f"  M2增速 {money['m2_growth']*100:.1f}%，流动性一般")

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_fiscal_policy():
    """分析财政政策"""
    fiscal = MACRO_DATA['fiscal']
    signals = []
    score = 50

    if fiscal['policy_stance'] == "expansionary":
        signals.append(f"🟢 积极财政政策 (赤字率 {fiscal['deficit_ratio']*100:.1f}%)")
        score += 15
    elif fiscal['policy_stance'] == "neutral":
        signals.append(f"🟡 稳健财政政策")
        score += 5
    else:
        signals.append(f"🔴 紧缩财政政策")
        score -= 10

    signals.append(f"📊 专项债规模: {fiscal['special_bonds']}")

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_international_environment():
    """分析国际环境"""
    intl = MACRO_DATA['international']
    signals = []
    score = 50

    # 美联储政策影响
    if intl['fed_rate'] > 0.04:
        signals.append(f"🇺 美联储利率 {intl['fed_rate']*100:.2f}%，高利率环境")
        score -= 10
    else:
        signals.append(f"🇺🇸 美联储利率 {intl['fed_rate']*100:.2f}%，利率正常化")
        score += 5

    # 汇率
    if intl['usd_cny'] > 7.2:
        signals.append(f"💱 人民币贬值压力 (USD/CNY {intl['usd_cny']:.2f})")
        score -= 5
    else:
        signals.append(f"💱 人民币汇率稳定 (USD/CNY {intl['usd_cny']:.2f})")
        score += 5

    # 油价
    if intl['brent_oil'] > 80:
        signals.append(f"🛢️ 高油价 ({intl['brent_oil']:.1f}美元)，利好能源股")
        score += 10
    elif intl['brent_oil'] < 60:
        signals.append(f"🛢️ 低油价 ({intl['brent_oil']:.1f}美元)，利空能源股")
        score -= 10
    else:
        signals.append(f"🛢️ 油价中性 ({intl['brent_oil']:.1f}美元)")

    return {'score': max(0, min(100, score)), 'signals': signals}


def generate_sector_impact():
    """生成对各板块的影响分析"""
    intl = MACRO_DATA['international']
    rate = MACRO_DATA['interest_rate']

    impacts = {
        "煤炭": {
            "impact": "中性偏多" if intl['brent_oil'] > 70 else "中性偏空",
            "reason": f"油价{intl['brent_oil']:.1f}美元对煤炭有{'支撑' if intl['brent_oil'] > 70 else '压制'}作用",
            "score": 65 if intl['brent_oil'] > 70 else 45,
        },
        "电力": {
            "impact": "利好" if rate['trend'] == "cutting" else "中性",
            "reason": "降息降低融资成本，利好重资产的电力行业",
            "score": 70 if rate['trend'] == "cutting" else 55,
        },
        "石油石化": {
            "impact": "利好" if intl['brent_oil'] > 70 else "利空",
            "reason": f"油价{intl['brent_oil']:.1f}美元{'利好' if intl['brent_oil'] > 70 else '利空'}石油石化盈利",
            "score": 75 if intl['brent_oil'] > 70 else 35,
        },
        "水务环保": {
            "impact": "利好" if MACRO_DATA['fiscal']['policy_stance'] == "expansionary" else "中性",
            "reason": "积极财政政策利好环保基建投资",
            "score": 70 if MACRO_DATA['fiscal']['policy_stance'] == "expansionary" else 55,
        },
    }

    return impacts


def generate_macro_report():
    """生成宏观经济分析报告"""
    report = []
    report.append("=" * 70)
    report.append("🌐 宏观经济环境分析报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")

    growth = analyze_growth_environment()
    inflation = analyze_inflation_environment()
    monetary = analyze_monetary_policy()
    fiscal = analyze_fiscal_policy()
    international = analyze_international_environment()

    # 综合宏观评分
    total_score = (
        growth['score'] * 0.25 +
        inflation['score'] * 0.20 +
        monetary['score'] * 0.25 +
        fiscal['score'] * 0.15 +
        international['score'] * 0.15
    )

    if total_score >= 70:
        macro_outlook = "🟢 宏观环境友好"
    elif total_score >= 50:
        macro_outlook = "🟡 宏观环境中性"
    else:
        macro_outlook = "🔴 宏观环境承压"

    report.append(f"🏆 综合宏观评分: {total_score:.1f}/100 {macro_outlook}")
    report.append("")

    # 经济增长
    report.append("📈 经济增长环境:")
    for signal in growth['signals']:
        report.append(f"   • {signal}")
    report.append("")

    # 通胀
    report.append("💹 通胀环境:")
    for signal in inflation['signals']:
        report.append(f"   • {signal}")
    report.append("")

    # 货币政策
    report.append("💰 货币政策:")
    for signal in monetary['signals']:
        report.append(f"   • {signal}")
    report.append("")

    # 财政政策
    report.append("🏛️ 财政政策:")
    for signal in fiscal['signals']:
        report.append(f"   • {signal}")
    report.append("")

    # 国际环境
    report.append("🌍 国际环境:")
    for signal in international['signals']:
        report.append(f"   • {signal}")
    report.append("")

    # 板块影响
    report.append("📊 对各板块影响:")
    report.append("-" * 60)
    sector_impacts = generate_sector_impact()
    for sector, impact in sector_impacts.items():
        report.append(f"  {sector:<10} {impact['impact']:<8} (评分: {impact['score']}/100)")
        report.append(f"           {impact['reason']}")
    report.append("")

    report.append("⚠️ 宏观分析仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report), total_score


def main():
    """测试"""
    report, score = generate_macro_report()
    print(report)


if __name__ == "__main__":
    main()
