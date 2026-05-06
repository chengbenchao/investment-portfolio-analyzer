#!/usr/bin/env python3
"""
财务报表分析模块 - 首席金融分析师第二优先级技能
包含：
1. 财务报表核心指标分析
2. 利润质量评估
3. 现金流健康度分析
4. 资产负债健康度评估
5. 综合财务评分系统
"""

from datetime import datetime
import json


# 财务健康评分权重配置
SCORING_WEIGHTS = {
    'profitability': 0.30,  # 盈利能力 30%
    'cash_flow': 0.25,      # 现金流 25%
    'solvency': 0.20,       # 偿债能力 20%
    'efficiency': 0.15,     # 运营效率 15%
    'growth': 0.10          # 成长性 10%
}


# 股票财务数据参考（基于历史数据）
FINANCIAL_DATA = {
    "601088": {
        "name": "中国神华",
        "sector": "煤炭",
        # 盈利能力指标
        "roe": 0.18,        # 净资产收益率
        "roa": 0.12,        # 总资产收益率
        "gross_margin": 0.35,  # 毛利率
        "net_margin": 0.25,    # 净利率
        # 现金流指标
        "operating_cash_flow_ratio": 1.8,  # 经营现金流比率
        "free_cash_flow_yield": 0.12,      # 自由现金流收益率
        "cash_to_debt": 0.85,              # 现金对负债比率
        # 偿债能力指标
        "debt_to_equity": 0.45,            # 资产负债率
        "current_ratio": 2.2,              # 流动比率
        "quick_ratio": 1.8,                # 速动比率
        # 运营效率指标
        "asset_turnover": 0.65,            # 总资产周转率
        "inventory_turnover": 8.5,         # 存货周转率
        # 成长性指标
        "revenue_growth_3y": 0.08,         # 3年营收复合增长率
        "eps_growth_3y": 0.12,             # 3年EPS复合增长率
        "dividend_growth_3y": 0.05,        # 3年股息增长率
    },
    "600900": {
        "name": "长江电力",
        "sector": "电力",
        "roe": 0.15,
        "roa": 0.08,
        "gross_margin": 0.55,
        "net_margin": 0.45,
        "operating_cash_flow_ratio": 2.5,
        "free_cash_flow_yield": 0.08,
        "cash_to_debt": 0.65,
        "debt_to_equity": 0.85,
        "current_ratio": 1.8,
        "quick_ratio": 1.5,
        "asset_turnover": 0.35,
        "inventory_turnover": 12.0,
        "revenue_growth_3y": 0.05,
        "eps_growth_3y": 0.06,
        "dividend_growth_3y": 0.04,
    },
    "601225": {
        "name": "陕西煤业",
        "sector": "煤炭",
        "roe": 0.22,
        "roa": 0.15,
        "gross_margin": 0.40,
        "net_margin": 0.30,
        "operating_cash_flow_ratio": 2.0,
        "free_cash_flow_yield": 0.15,
        "cash_to_debt": 0.90,
        "debt_to_equity": 0.35,
        "current_ratio": 2.5,
        "quick_ratio": 2.0,
        "asset_turnover": 0.70,
        "inventory_turnover": 9.0,
        "revenue_growth_3y": 0.10,
        "eps_growth_3y": 0.15,
        "dividend_growth_3y": 0.06,
    },
    "601857": {
        "name": "中国石油",
        "sector": "石油",
        "roe": 0.09,
        "roa": 0.05,
        "gross_margin": 0.25,
        "net_margin": 0.10,
        "operating_cash_flow_ratio": 1.5,
        "free_cash_flow_yield": 0.08,
        "cash_to_debt": 0.55,
        "debt_to_equity": 0.60,
        "current_ratio": 1.5,
        "quick_ratio": 1.2,
        "asset_turnover": 0.55,
        "inventory_turnover": 10.0,
        "revenue_growth_3y": 0.03,
        "eps_growth_3y": 0.05,
        "dividend_growth_3y": 0.03,
    },
    "601158": {
        "name": "重庆水务",
        "sector": "水务",
        "roe": 0.10,
        "roa": 0.06,
        "gross_margin": 0.45,
        "net_margin": 0.35,
        "operating_cash_flow_ratio": 2.2,
        "free_cash_flow_yield": 0.07,
        "cash_to_debt": 0.75,
        "debt_to_equity": 0.50,
        "current_ratio": 2.0,
        "quick_ratio": 1.8,
        "asset_turnover": 0.40,
        "inventory_turnover": 15.0,
        "revenue_growth_3y": 0.04,
        "eps_growth_3y": 0.05,
        "dividend_growth_3y": 0.03,
    },
    "600028": {
        "name": "中国石化",
        "sector": "石化",
        "roe": 0.08,
        "roa": 0.04,
        "gross_margin": 0.20,
        "net_margin": 0.08,
        "operating_cash_flow_ratio": 1.4,
        "free_cash_flow_yield": 0.07,
        "cash_to_debt": 0.50,
        "debt_to_equity": 0.55,
        "current_ratio": 1.4,
        "quick_ratio": 1.1,
        "asset_turnover": 0.50,
        "inventory_turnover": 11.0,
        "revenue_growth_3y": 0.02,
        "eps_growth_3y": 0.04,
        "dividend_growth_3y": 0.03,
    },
}


def score_metric(value, min_val, max_val):
    """
    指标评分函数
    value: 当前值
    min_val: 最低值
    max_val: 最高值
    返回: 0-100的评分
    """
    if value <= min_val:
        return 0
    elif value >= max_val:
        return 100
    else:
        return ((value - min_val) / (max_val - min_val)) * 100


def analyze_profitability(data):
    """分析盈利能力"""
    roe_score = score_metric(data['roe'], 0.08, 0.20) * 0.35
    roa_score = score_metric(data['roa'], 0.05, 0.15) * 0.25
    net_margin_score = score_metric(data['net_margin'], 0.10, 0.30) * 0.25
    gross_margin_score = score_metric(data['gross_margin'], 0.20, 0.40) * 0.15

    total = roe_score + roa_score + net_margin_score + gross_margin_score
    return {
        'score': total,
        'details': {
            'ROE': {'value': f"{data['roe']*100:.1f}%", 'score': score_metric(data['roe'], 0.08, 0.20)},
            'ROA': {'value': f"{data['roa']*100:.1f}%", 'score': score_metric(data['roa'], 0.05, 0.15)},
            '净利率': {'value': f"{data['net_margin']*100:.1f}%", 'score': score_metric(data['net_margin'], 0.10, 0.30)},
            '毛利率': {'value': f"{data['gross_margin']*100:.1f}%", 'score': score_metric(data['gross_margin'], 0.20, 0.40)},
        }
    }


def analyze_cash_flow(data):
    """分析现金流健康度"""
    ocf_score = score_metric(data['operating_cash_flow_ratio'], 1.0, 2.0) * 0.35
    fcf_score = score_metric(data['free_cash_flow_yield'], 0.05, 0.12) * 0.35
    cash_debt_score = score_metric(data['cash_to_debt'], 0.4, 0.8) * 0.30

    total = ocf_score + fcf_score + cash_debt_score
    return {
        'score': total,
        'details': {
            '经营现金流比率': {'value': f"{data['operating_cash_flow_ratio']:.2f}", 'score': score_metric(data['operating_cash_flow_ratio'], 1.0, 2.0)},
            '自由现金流收益率': {'value': f"{data['free_cash_flow_yield']*100:.1f}%", 'score': score_metric(data['free_cash_flow_yield'], 0.05, 0.12)},
            '现金对负债': {'value': f"{data['cash_to_debt']:.2f}", 'score': score_metric(data['cash_to_debt'], 0.4, 0.8)},
        }
    }


def analyze_solvency(data):
    """分析偿债能力"""
    de_score = score_metric(data['debt_to_equity'], 0.8, 0.2) * 0.35  # 越低越好，所以反转
    current_score = score_metric(data['current_ratio'], 1.0, 2.0) * 0.35
    quick_score = score_metric(data['quick_ratio'], 0.8, 1.5) * 0.30

    total = de_score + current_score + quick_score
    return {
        'score': total,
        'details': {
            '资产负债率': {'value': f"{data['debt_to_equity']*100:.1f}%", 'score': score_metric(data['debt_to_equity'], 0.8, 0.2)},
            '流动比率': {'value': f"{data['current_ratio']:.2f}", 'score': score_metric(data['current_ratio'], 1.0, 2.0)},
            '速动比率': {'value': f"{data['quick_ratio']:.2f}", 'score': score_metric(data['quick_ratio'], 0.8, 1.5)},
        }
    }


def analyze_efficiency(data):
    """分析运营效率"""
    asset_turn_score = score_metric(data['asset_turnover'], 0.3, 0.7) * 0.40
    inventory_score = score_metric(data['inventory_turnover'], 5.0, 12.0) * 0.30
    cash_conv_score = min(100, data['inventory_turnover'] / 12.0 * 100) * 0.30

    total = asset_turn_score + inventory_score + cash_conv_score
    return {
        'score': total,
        'details': {
            '总资产周转率': {'value': f"{data['asset_turnover']:.2f}", 'score': score_metric(data['asset_turnover'], 0.3, 0.7)},
            '存货周转率': {'value': f"{data['inventory_turnover']:.1f}", 'score': score_metric(data['inventory_turnover'], 5.0, 12.0)},
        }
    }


def analyze_growth(data):
    """分析成长性"""
    rev_score = score_metric(data['revenue_growth_3y'], 0.02, 0.10) * 0.40
    eps_score = score_metric(data['eps_growth_3y'], 0.03, 0.12) * 0.40
    div_score = score_metric(data['dividend_growth_3y'], 0.02, 0.06) * 0.20

    total = rev_score + eps_score + div_score
    return {
        'score': total,
        'details': {
            '营收3年CAGR': {'value': f"{data['revenue_growth_3y']*100:.1f}%", 'score': score_metric(data['revenue_growth_3y'], 0.02, 0.10)},
            'EPS 3年CAGR': {'value': f"{data['eps_growth_3y']*100:.1f}%", 'score': score_metric(data['eps_growth_3y'], 0.03, 0.12)},
            '股息3年CAGR': {'value': f"{data['dividend_growth_3y']*100:.1f}%", 'score': score_metric(data['dividend_growth_3y'], 0.02, 0.06)},
        }
    }


def get_health_level(score):
    """根据评分返回健康等级"""
    if score >= 80:
        return "🟢 优秀", "#4ade80"
    elif score >= 60:
        return "🟡 良好", "#facc15"
    elif score >= 40:
        return "🟠 一般", "#fb923c"
    else:
        return "🔴 较差", "#f87171"


def analyze_stock(code):
    """分析单只股票的财务状况"""
    if code not in FINANCIAL_DATA:
        return None

    data = FINANCIAL_DATA[code]

    # 各项分析
    profit_analysis = analyze_profitability(data)
    cash_analysis = analyze_cash_flow(data)
    solvency_analysis = analyze_solvency(data)
    efficiency_analysis = analyze_efficiency(data)
    growth_analysis = analyze_growth(data)

    # 综合评分
    total_score = (
        profit_analysis['score'] * SCORING_WEIGHTS['profitability'] +
        cash_analysis['score'] * SCORING_WEIGHTS['cash_flow'] +
        solvency_analysis['score'] * SCORING_WEIGHTS['solvency'] +
        efficiency_analysis['score'] * SCORING_WEIGHTS['efficiency'] +
        growth_analysis['score'] * SCORING_WEIGHTS['growth']
    )

    health_level, color = get_health_level(total_score)

    return {
        'code': code,
        'name': data['name'],
        'sector': data['sector'],
        'total_score': total_score,
        'health_level': health_level,
        'health_color': color,
        'profitability': profit_analysis,
        'cash_flow': cash_analysis,
        'solvency': solvency_analysis,
        'efficiency': efficiency_analysis,
        'growth': growth_analysis,
    }


def generate_financial_report(codes):
    """生成财务分析报告"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 财务报表分析报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")

    analyses = {}
    for code in codes:
        analysis = analyze_stock(code)
        if analysis:
            analyses[code] = analysis

    for code, analysis in analyses.items():
        report.append(f"📌 {analysis['name']} ({code})")
        report.append("-" * 60)
        report.append(f"🏆 综合财务评分: {analysis['total_score']:.1f}/100 {analysis['health_level']}")
        report.append("")

        # 盈利能力
        report.append(f"💰 盈利能力 ({SCORING_WEIGHTS['profitability']*100:.0f}%): {analysis['profitability']['score']:.1f}/100")
        for metric, details in analysis['profitability']['details'].items():
            report.append(f"   • {metric}: {details['value']} (得分: {details['score']:.1f})")
        report.append("")

        # 现金流
        report.append(f"💵 现金流 ({SCORING_WEIGHTS['cash_flow']*100:.0f}%): {analysis['cash_flow']['score']:.1f}/100")
        for metric, details in analysis['cash_flow']['details'].items():
            report.append(f"   • {metric}: {details['value']} (得分: {details['score']:.1f})")
        report.append("")

        # 偿债能力
        report.append(f"🏦 偿债能力 ({SCORING_WEIGHTS['solvency']*100:.0f}%): {analysis['solvency']['score']:.1f}/100")
        for metric, details in analysis['solvency']['details'].items():
            report.append(f"   • {metric}: {details['value']} (得分: {details['score']:.1f})")
        report.append("")

        # 运营效率
        report.append(f"⚡ 运营效率 ({SCORING_WEIGHTS['efficiency']*100:.0f}%): {analysis['efficiency']['score']:.1f}/100")
        for metric, details in analysis['efficiency']['details'].items():
            report.append(f"   • {metric}: {details['value']} (得分: {details['score']:.1f})")
        report.append("")

        # 成长性
        report.append(f"📈 成长性 ({SCORING_WEIGHTS['growth']*100:.0f}%): {analysis['growth']['score']:.1f}/100")
        for metric, details in analysis['growth']['details'].items():
            report.append(f"   • {metric}: {details['value']} (得分: {details['score']:.1f})")
        report.append("")
        report.append("=" * 70)
        report.append("")

    # 综合对比
    report.append("📋 综合财务评分对比:")
    report.append("-" * 60)
    for code, analysis in sorted(analyses.items(), key=lambda x: x[1]['total_score'], reverse=True):
        report.append(f"  {analysis['name']:<10} {analysis['total_score']:>5.1f}/100  {analysis['health_level']}")
    report.append("")
    report.append("⚠️ 风险提示: 财务数据基于历史情况，仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def main():
    """测试"""
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    report = generate_financial_report(codes)
    print(report)


if __name__ == "__main__":
    main()
