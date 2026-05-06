#!/usr/bin/env python3
"""
行业研究模块 - 首席金融分析师第五优先级技能
包含：
1. 行业周期判断
2. 竞争格局分析
3. 产业链上下游分析
4. 行业对标估值
5. 行业评分系统
"""

from datetime import datetime


# 行业数据配置
INDUSTRY_DATA = {
    "煤炭": {
        "sector_code": "coal",
        "cycle_stage": "成熟期",  # 导入期/成长期/成熟期/衰退期
        "cycle_position": "中后期",
        "growth_rate": 0.03,  # 行业增长率
        "market_size": "2.5万亿",
        "concentration_top3": 0.45,  # CR3集中度
        "concentration_top5": 0.60,
        "barriers_to_entry": "高",  # 进入壁垒
        "policy_support": "中性",  # 政策支持度
        "tech_disruption_risk": "中",  # 技术颠覆风险
        "upstream": ["采矿设备", "运输物流"],
        "downstream": ["电力", "钢铁", "化工"],
        "key_players": ["中国神华", "陕西煤业", "中煤能源", "兖矿能源", "山西焦煤"],
        "avg_pe": 8.5,
        "avg_pb": 1.2,
        "avg_dividend_yield": 0.065,
        "outlook": "短期稳定，长期受新能源替代压力",
    },
    "电力": {
        "sector_code": "power",
        "cycle_stage": "成熟期",
        "cycle_position": "中期",
        "growth_rate": 0.04,
        "market_size": "3.2万亿",
        "concentration_top3": 0.55,
        "concentration_top5": 0.70,
        "barriers_to_entry": "极高",
        "policy_support": "积极",
        "tech_disruption_risk": "低",
        "upstream": ["煤炭", "天然气", "设备制造"],
        "downstream": ["工业用户", "居民用电", "商业用电"],
        "key_players": ["长江电力", "华能国际", "国电电力", "华电国际", "大唐发电"],
        "avg_pe": 14.0,
        "avg_pb": 1.8,
        "avg_dividend_yield": 0.045,
        "outlook": "稳定增长，清洁能源转型带来机遇",
    },
    "石油石化": {
        "sector_code": "oil_gas",
        "cycle_stage": "成熟期",
        "cycle_position": "中后期",
        "growth_rate": 0.02,
        "market_size": "5.8万亿",
        "concentration_top3": 0.70,
        "concentration_top5": 0.85,
        "barriers_to_entry": "极高",
        "policy_support": "中性",
        "tech_disruption_risk": "中",
        "upstream": ["勘探开采", "油服设备"],
        "downstream": ["化工", "交通燃料", "工业原料"],
        "key_players": ["中国石油", "中国石化", "中国海油", "恒力石化", "荣盛石化"],
        "avg_pe": 9.0,
        "avg_pb": 0.85,
        "avg_dividend_yield": 0.055,
        "outlook": "受油价波动影响大，新能源长期替代",
    },
    "水务环保": {
        "sector_code": "water_env",
        "cycle_stage": "成长期",
        "cycle_position": "中期",
        "growth_rate": 0.06,
        "market_size": "0.8万亿",
        "concentration_top3": 0.25,
        "concentration_top5": 0.40,
        "barriers_to_entry": "中",
        "policy_support": "积极",
        "tech_disruption_risk": "低",
        "upstream": ["水处理设备", "环保材料"],
        "downstream": ["居民用水", "工业用水", "政府"],
        "key_players": ["重庆水务", "首创环保", "北控水务", "碧水源", "兴蓉环境"],
        "avg_pe": 12.0,
        "avg_pb": 1.4,
        "avg_dividend_yield": 0.042,
        "outlook": "政策驱动增长，环保标准提升带来机遇",
    },
}


# 股票所属行业映射
STOCK_INDUSTRY_MAP = {
    "601088": "煤炭",
    "600900": "电力",
    "601225": "煤炭",
    "601857": "石油石化",
    "601158": "水务环保",
    "600028": "石油石化",
}


# 股票在行业中的地位
STOCK_INDUSTRY_POSITION = {
    "601088": {"rank": 1, "market_share": 0.18, "note": "行业龙头，全产业链布局"},
    "600900": {"rank": 1, "market_share": 0.22, "note": "水电龙头，现金流极佳"},
    "601225": {"rank": 2, "market_share": 0.12, "note": "区域龙头，资源禀赋优"},
    "601857": {"rank": 1, "market_share": 0.35, "note": "油气全产业链垄断"},
    "601158": {"rank": 3, "market_share": 0.08, "note": "区域水务龙头"},
    "600028": {"rank": 2, "market_share": 0.30, "note": "炼化龙头，规模优势"},
}


def analyze_industry_cycle(industry_data):
    """分析行业周期"""
    stage = industry_data['cycle_stage']
    position = industry_data['cycle_position']
    growth = industry_data['growth_rate']

    signals = []
    score = 50

    if stage == "成长期":
        signals.append("🟢 行业处于成长期")
        score += 20
    elif stage == "成熟期":
        signals.append("🟡 行业处于成熟期")
        score += 10
    elif stage == "衰退期":
        signals.append("🔴 行业处于衰退期")
        score -= 20

    if position == "早期":
        signals.append("📈 周期早期，增长空间大")
        score += 10
    elif position == "中期":
        signals.append("📊 周期中期，稳定发展")
    elif position == "中后期":
        signals.append("📉 周期中后期，增长放缓")
        score -= 10

    if growth > 0.05:
        signals.append(f"🚀 行业增速 {growth*100:.0f}%，高速增长")
        score += 15
    elif growth > 0.03:
        signals.append(f"📈 行业增速 {growth*100:.0f}%，稳健增长")
        score += 5
    else:
        signals.append(f" 行业增速 {growth*100:.0f}%，增长缓慢")
        score -= 10

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_competition(industry_data):
    """分析竞争格局"""
    cr3 = industry_data['concentration_top3']
    cr5 = industry_data['concentration_top5']
    barriers = industry_data['barriers_to_entry']

    signals = []
    score = 50

    if cr3 > 0.6:
        signals.append(f"🔒 高度集中 (CR3={cr3*100:.0f}%)")
        score += 15
    elif cr3 > 0.4:
        signals.append(f"📊 中度集中 (CR3={cr3*100:.0f}%)")
        score += 5
    else:
        signals.append(f"🔓 分散竞争 (CR3={cr3*100:.0f}%)")
        score -= 5

    if barriers == "极高":
        signals.append("🏰 进入壁垒极高（护城河深）")
        score += 15
    elif barriers == "高":
        signals.append("🛡️ 进入壁垒高")
        score += 10
    elif barriers == "中":
        signals.append("🚧 进入壁垒中等")
        score += 5

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_policy_and_risk(industry_data):
    """分析政策与风险"""
    policy = industry_data['policy_support']
    tech_risk = industry_data['tech_disruption_risk']

    signals = []
    score = 50

    if policy == "积极":
        signals.append("🟢 政策支持积极")
        score += 15
    elif policy == "中性":
        signals.append("🟡 政策中性")
    elif policy == "限制":
        signals.append("🔴 政策限制")
        score -= 15

    if tech_risk == "低":
        signals.append("✅ 技术颠覆风险低")
        score += 10
    elif tech_risk == "中":
        signals.append("⚠️ 存在技术颠覆风险")
        score -= 5
    elif tech_risk == "高":
        signals.append("🚨 技术颠覆风险高")
        score -= 15

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_valuation_vs_industry(stock_code, stock_pe, stock_pb, stock_dividend):
    """分析与行业估值的对比"""
    industry_name = STOCK_INDUSTRY_MAP.get(stock_code)
    if not industry_name or industry_name not in INDUSTRY_DATA:
        return None

    industry = INDUSTRY_DATA[industry_name]

    pe_diff = ((stock_pe - industry['avg_pe']) / industry['avg_pe']) * 100
    pb_diff = ((stock_pb - industry['avg_pb']) / industry['avg_pb']) * 100
    div_diff = ((stock_dividend - industry['avg_dividend_yield']) / industry['avg_dividend_yield']) * 100

    signals = []

    if pe_diff < -10:
        signals.append(f"🟢 PE低于行业 {abs(pe_diff):.1f}%")
    elif pe_diff > 10:
        signals.append(f"🔴 PE高于行业 {pe_diff:.1f}%")
    else:
        signals.append(f"🟡 PE与行业持平 (差异 {pe_diff:+.1f}%)")

    if div_diff > 10:
        signals.append(f"🟢 股息率高于行业 {div_diff:.1f}%")
    elif div_diff < -10:
        signals.append(f"🔴 股息率低于行业 {abs(div_diff):.1f}%")
    else:
        signals.append(f"🟡 股息率与行业持平")

    return {
        'industry': industry_name,
        'signals': signals,
        'pe_diff': pe_diff,
        'pb_diff': pb_diff,
        'div_diff': div_diff,
    }


def analyze_industry(code, stock_pe=None, stock_pb=None, stock_dividend=None):
    """分析单只股票的行业情况"""
    industry_name = STOCK_INDUSTRY_MAP.get(code)
    if not industry_name:
        return None

    industry_data = INDUSTRY_DATA[industry_name]
    position = STOCK_INDUSTRY_POSITION.get(code, {})

    cycle = analyze_industry_cycle(industry_data)
    competition = analyze_competition(industry_data)
    policy_risk = analyze_policy_and_risk(industry_data)

    # 综合行业评分
    total_score = (
        cycle['score'] * 0.30 +
        competition['score'] * 0.30 +
        policy_risk['score'] * 0.25 +
        (position.get('rank', 5) <= 2) * 15  # 行业前两名加分
    )

    # 行业对标分析
    valuation_comparison = None
    if stock_pe and stock_pb and stock_dividend:
        valuation_comparison = analyze_valuation_vs_industry(code, stock_pe, stock_pb, stock_dividend)

    return {
        'code': code,
        'industry': industry_name,
        'total_score': total_score,
        'cycle': cycle,
        'competition': competition,
        'policy_risk': policy_risk,
        'valuation_comparison': valuation_comparison,
        'industry_data': industry_data,
        'position': position,
    }


def generate_industry_report(codes, stock_metrics=None):
    """生成行业研究报告"""
    if stock_metrics is None:
        stock_metrics = {}

    report = []
    report.append("=" * 70)
    report.append("🏭 能源公用事业投资组合 - 行业研究报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")

    for code in codes:
        metrics = stock_metrics.get(code, {})
        analysis = analyze_industry(
            code,
            metrics.get('pe'),
            metrics.get('pb'),
            metrics.get('dividend_yield')
        )
        if not analysis:
            continue

        report.append(f"📌 {analysis['position'].get('note', analysis['industry'])} ({code})")
        report.append(f"🏭 所属行业: {analysis['industry']}")
        report.append(f"🏆 行业评分: {analysis['total_score']:.1f}/100")
        report.append("-" * 60)

        # 行业周期
        report.append("📈 行业周期分析:")
        for signal in analysis['cycle']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        # 竞争格局
        report.append("🏰 竞争格局:")
        for signal in analysis['competition']['signals']:
            report.append(f"   • {signal}")
        report.append(f"   • 行业排名: 第 {analysis['position'].get('rank', '?')} 名")
        report.append(f"   • 市场份额: {analysis['position'].get('market_share', '?')*100:.0f}%")
        report.append("")

        # 政策与风险
        report.append("📋 政策与风险:")
        for signal in analysis['policy_risk']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        # 产业链
        industry_data = analysis['industry_data']
        report.append("🔗 产业链:")
        report.append(f"   • 上游: {', '.join(industry_data['upstream'])}")
        report.append(f"   • 下游: {', '.join(industry_data['downstream'])}")
        report.append("")

        # 行业估值对比
        if analysis['valuation_comparison']:
            report.append("📊 行业估值对比:")
            for signal in analysis['valuation_comparison']['signals']:
                report.append(f"   • {signal}")
            report.append("")

        report.append(f"🔮 行业展望: {industry_data['outlook']}")
        report.append("")
        report.append("=" * 70)
        report.append("")

    # 行业汇总
    report.append("📋 行业汇总:")
    report.append("-" * 60)
    industries_seen = set()
    for code in codes:
        industry = STOCK_INDUSTRY_MAP.get(code)
        if industry and industry not in industries_seen:
            industries_seen.add(industry)
            data = INDUSTRY_DATA[industry]
            report.append(f"  {industry:<10} 增速:{data['growth_rate']*100:>4.0f}%  周期:{data['cycle_stage']}  集中度CR3:{data['concentration_top3']*100:.0f}%")
    report.append("")
    report.append("⚠️ 行业研究仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def main():
    """测试"""
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    stock_metrics = {
        '601088': {'pe': 8.65, 'pb': 1.46, 'dividend_yield': 0.069},
        '600900': {'pe': 16.45, 'pb': 2.36, 'dividend_yield': 0.036},
        '601225': {'pe': 8.50, 'pb': 1.82, 'dividend_yield': 0.070},
        '601857': {'pe': 12.55, 'pb': 1.10, 'dividend_yield': 0.048},
        '601158': {'pe': 8.88, 'pb': 0.99, 'dividend_yield': 0.067},
        '600028': {'pe': 6.31, 'pb': 0.65, 'dividend_yield': 0.095},
    }
    report = generate_industry_report(codes, stock_metrics)
    print(report)


if __name__ == "__main__":
    main()
