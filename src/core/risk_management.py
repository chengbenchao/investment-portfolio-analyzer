#!/usr/bin/env python3
"""
风险管理模块 - 首席金融分析师第四优先级技能
包含：
1. VaR (Value at Risk) 计算
2. 最大回撤监控
3. 仓位管理建议
4. 止损策略
5. 风险等级评估
"""

from datetime import datetime
import math


# 风险参数配置
RISK_PARAMS = {
    'var_confidence': 0.95,      # VaR置信度 95%
    'max_position_pct': 0.25,    # 单只股票最大仓位 25%
    'stop_loss_pct': 0.10,       # 止损线 10%
    'take_profit_pct': 0.20,     # 止盈线 20%
    'rebalance_threshold': 0.05, # 再平衡阈值 5%
}


# 股票风险数据（基于历史波动率）
RISK_DATA = {
    "601088": {
        "name": "中国神华",
        "current_price": 47.56,
        "volatility_30d": 0.025,  # 30日波动率 2.5%
        "volatility_90d": 0.028,  # 90日波动率 2.8%
        "beta": 0.85,             # 贝塔系数
        "max_drawdown_1y": -0.18, # 1年最大回撤 -18%
        "sharpe_ratio": 1.25,     # 夏普比率
        "correlation_market": 0.75, # 与市场相关性
        "avg_daily_return": 0.001,  # 日均收益率 0.1%
    },
    "600900": {
        "name": "长江电力",
        "current_price": 27.14,
        "volatility_30d": 0.018,
        "volatility_90d": 0.020,
        "beta": 0.65,
        "max_drawdown_1y": -0.12,
        "sharpe_ratio": 1.45,
        "correlation_market": 0.60,
        "avg_daily_return": 0.0008,
    },
    "601225": {
        "name": "陕西煤业",
        "current_price": 25.47,
        "volatility_30d": 0.032,
        "volatility_90d": 0.035,
        "beta": 1.05,
        "max_drawdown_1y": -0.25,
        "sharpe_ratio": 1.15,
        "correlation_market": 0.80,
        "avg_daily_return": 0.0012,
    },
    "601857": {
        "name": "中国石油",
        "current_price": 11.91,
        "volatility_30d": 0.028,
        "volatility_90d": 0.030,
        "beta": 0.90,
        "max_drawdown_1y": -0.22,
        "sharpe_ratio": 0.65,
        "correlation_market": 0.70,
        "avg_daily_return": 0.0005,
    },
    "601158": {
        "name": "重庆水务",
        "current_price": 4.44,
        "volatility_30d": 0.015,
        "volatility_90d": 0.016,
        "beta": 0.55,
        "max_drawdown_1y": -0.15,
        "sharpe_ratio": 1.35,
        "correlation_market": 0.50,
        "avg_daily_return": 0.0006,
    },
    "600028": {
        "name": "中国石化",
        "current_price": 5.37,
        "volatility_30d": 0.026,
        "volatility_90d": 0.028,
        "beta": 0.80,
        "max_drawdown_1y": -0.20,
        "sharpe_ratio": 0.75,
        "correlation_market": 0.65,
        "avg_daily_return": 0.0004,
    },
}


def calculate_var(data, confidence=0.95):
    """计算VaR (Value at Risk)"""
    volatility = data['volatility_30d']
    avg_return = data['avg_daily_return']

    # 正态分布假设下的VaR
    # 95%置信度的Z值是1.645
    z_score = 1.645 if confidence == 0.95 else 2.326

    var_daily = abs(avg_return - z_score * volatility)
    var_weekly = var_daily * math.sqrt(5)
    var_monthly = var_daily * math.sqrt(22)

    return {
        'daily': var_daily,
        'weekly': var_weekly,
        'monthly': var_monthly,
    }


def analyze_risk_level(data):
    """分析风险等级"""
    volatility = data['volatility_30d']
    beta = data['beta']
    max_dd = abs(data['max_drawdown_1y'])
    sharpe = data['sharpe_ratio']

    score = 100

    # 波动率评分
    if volatility > 0.03:
        score -= 20
    elif volatility > 0.025:
        score -= 10

    # 贝塔评分
    if beta > 1.0:
        score -= 15
    elif beta < 0.7:
        score += 10

    # 最大回撤评分
    if max_dd > 0.20:
        score -= 20
    elif max_dd > 0.15:
        score -= 10

    # 夏普比率评分
    if sharpe > 1.2:
        score += 15
    elif sharpe > 1.0:
        score += 10
    elif sharpe < 0.8:
        score -= 10

    score = max(0, min(100, score))

    if score >= 75:
        level = "🟢 低风险"
    elif score >= 50:
        level = "🟡 中风险"
    elif score >= 25:
        level = "🟠 中高风险"
    else:
        level = "🔴 高风险"

    return {'score': score, 'level': level}


def calculate_position_suggestion(data, total_capital, risk_level_score):
    """计算仓位建议"""
    volatility = data['volatility_30d']
    max_position = RISK_PARAMS['max_position_pct']

    # 根据风险等级调整仓位
    if risk_level_score >= 75:
        position_pct = max_position
    elif risk_level_score >= 50:
        position_pct = max_position * 0.8
    elif risk_level_score >= 25:
        position_pct = max_position * 0.6
    else:
        position_pct = max_position * 0.4

    # 根据波动率微调
    if volatility > 0.03:
        position_pct *= 0.8
    elif volatility < 0.02:
        position_pct *= 1.2

    position_pct = min(position_pct, max_position)
    position_amount = total_capital * position_pct

    return {
        'position_pct': position_pct,
        'position_amount': position_amount,
        'max_allowed': total_capital * max_position,
    }


def calculate_stop_loss(data):
    """计算止损止盈位"""
    price = data['current_price']
    volatility = data['volatility_30d']
    max_dd = abs(data['max_drawdown_1y'])

    # 动态止损：基于波动率和历史最大回撤
    stop_loss_pct = min(
        RISK_PARAMS['stop_loss_pct'],
        max_dd * 0.5,
        volatility * 10
    )

    stop_loss_price = price * (1 - stop_loss_pct)

    # 动态止盈
    take_profit_pct = max(
        RISK_PARAMS['take_profit_pct'],
        max_dd * 0.8
    )

    take_profit_price = price * (1 + take_profit_pct)

    return {
        'stop_loss_pct': stop_loss_pct,
        'stop_loss_price': stop_loss_price,
        'take_profit_pct': take_profit_pct,
        'take_profit_price': take_profit_price,
    }


def analyze_diversification(codes_data):
    """分析组合分散度"""
    if len(codes_data) < 2:
        return {'score': 0, 'note': "股票数量不足，无法分析分散度"}

    # 计算平均相关性
    correlations = [d['correlation_market'] for d in codes_data]
    avg_correlation = sum(correlations) / len(correlations)

    # 计算波动率分散度
    volatilities = [d['volatility_30d'] for d in codes_data]
    avg_volatility = sum(volatilities) / len(volatilities)
    vol_std = math.sqrt(sum((v - avg_volatility) ** 2 for v in volatilities) / len(volatilities))

    # 分散度评分
    score = 100

    # 相关性越低越好
    if avg_correlation > 0.7:
        score -= 20
    elif avg_correlation > 0.6:
        score -= 10
    else:
        score += 10

    # 股票数量
    if len(codes_data) >= 6:
        score += 10
    elif len(codes_data) >= 4:
        score += 5

    score = max(0, min(100, score))

    return {
        'score': score,
        'avg_correlation': avg_correlation,
        'stock_count': len(codes_data),
        'note': "分散度良好" if score >= 70 else "分散度一般"
    }


def analyze_stock_risk(code, total_capital=100000):
    """分析单只股票风险"""
    if code not in RISK_DATA:
        return None

    data = RISK_DATA[code]

    var = calculate_var(data)
    risk_level = analyze_risk_level(data)
    position = calculate_position_suggestion(data, total_capital, risk_level['score'])
    stop_loss = calculate_stop_loss(data)

    return {
        'code': code,
        'name': data['name'],
        'current_price': data['current_price'],
        'var': var,
        'risk_level': risk_level,
        'position': position,
        'stop_loss': stop_loss,
        'volatility_30d': data['volatility_30d'],
        'beta': data['beta'],
        'max_drawdown_1y': data['max_drawdown_1y'],
        'sharpe_ratio': data['sharpe_ratio'],
        'correlation_market': data['correlation_market'],
    }


def generate_risk_report(codes, total_capital=100000):
    """生成风险管理报告"""
    report = []
    report.append("=" * 70)
    report.append("⚠️ 能源公用事业投资组合 - 风险管理报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"💰 总投资金额: {total_capital:,} 元")
    report.append("=" * 70)
    report.append("")

    all_analyses = []
    for code in codes:
        analysis = analyze_stock_risk(code, total_capital)
        if analysis:
            all_analyses.append(analysis)

    for analysis in all_analyses:
        report.append(f"📌 {analysis['name']} ({analysis['code']})")
        report.append(f"💵 当前价格: {analysis['current_price']:.2f} 元")
        report.append(f"🏆 风险等级: {analysis['risk_level']['level']} (评分: {analysis['risk_level']['score']}/100)")
        report.append("-" * 60)

        # VaR分析
        report.append("📊 VaR (风险价值) 分析:")
        report.append(f"   • 日VaR (95%): {analysis['var']['daily']*100:.2f}% (约 {analysis['var']['daily']*analysis['position']['position_amount']:.0f} 元)")
        report.append(f"   • 周VaR (95%): {analysis['var']['weekly']*100:.2f}%")
        report.append(f"   • 月VaR (95%): {analysis['var']['monthly']*100:.2f}%")
        report.append("")

        # 风险指标
        report.append("📈 风险指标:")
        report.append(f"   • 30日波动率: {analysis['volatility_30d']*100:.1f}%")
        report.append(f"   • 贝塔系数: {analysis['beta']:.2f}")
        report.append(f"   • 1年最大回撤: {analysis['max_drawdown_1y']*100:.1f}%")
        report.append(f"   • 夏普比率: {analysis['sharpe_ratio']:.2f}")
        report.append(f"   • 市场相关性: {analysis['correlation_market']:.2f}")
        report.append("")

        # 仓位建议
        report.append("💼 仓位建议:")
        report.append(f"   • 建议仓位: {analysis['position']['position_pct']*100:.1f}% (约 {analysis['position']['position_amount']:.0f} 元)")
        report.append(f"   • 最大允许: {analysis['position']['max_allowed']:.0f} 元")
        report.append("")

        # 止损止盈
        report.append("🛑 止损止盈位:")
        report.append(f"   • 止损位: {analysis['stop_loss']['stop_loss_price']:.2f} 元 (-{analysis['stop_loss']['stop_loss_pct']*100:.1f}%)")
        report.append(f"   • 止盈位: {analysis['stop_loss']['take_profit_price']:.2f} 元 (+{analysis['stop_loss']['take_profit_pct']*100:.1f}%)")
        report.append("")
        report.append("=" * 70)
        report.append("")

    # 组合分散度分析
    report.append("📋 组合分散度分析:")
    report.append("-" * 60)
    diversification = analyze_diversification(all_analyses)
    report.append(f"  分散度评分: {diversification['score']}/100")
    report.append(f"  平均相关性: {diversification['avg_correlation']:.2f}")
    report.append(f"  股票数量: {diversification['stock_count']} 只")
    report.append(f"  评价: {diversification['note']}")
    report.append("")

    # 风险汇总
    report.append("📊 风险汇总:")
    report.append("-" * 60)
    for a in sorted(all_analyses, key=lambda x: x['risk_level']['score']):
        report.append(f"  {a['name']:<10} 风险评分:{a['risk_level']['score']:>3}/100  {a['risk_level']['level']}")
    report.append("")

    report.append("⚠️ 风险提示:")
    report.append("  1. VaR基于历史数据，不能预测极端市场事件")
    report.append("  2. 止损位应根据个人风险承受能力调整")
    report.append("  3. 以上分析仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def main():
    """测试"""
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    report = generate_risk_report(codes)
    print(report)


if __name__ == "__main__":
    main()
