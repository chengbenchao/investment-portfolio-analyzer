#!/usr/bin/env python3
"""
技术分析模块 - 首席金融分析师第三优先级技能
包含：
1. K线形态识别
2. 均线系统 (MA/EMA)
3. MACD、RSI等技术指标
4. 支撑压力位分析
5. 技术面综合评分
"""

from datetime import datetime
import math


# 技术分析参数配置
TECHNICAL_PARAMS = {
    'ma_periods': [5, 10, 20, 60],  # 均线周期
    'rsi_period': 14,               # RSI周期
    'macd_fast': 12,                # MACD快线
    'macd_slow': 26,                # MACD慢线
    'macd_signal': 9,               # MACD信号线
    'bollinger_period': 20,         # 布林带周期
    'bollinger_std': 2,             # 布林带标准差倍数
}


# 股票历史价格数据（模拟，实际应从API获取）
PRICE_DATA = {
    "601088": {
        "name": "中国神华",
        "current_price": 47.56,
        "high_52w": 52.80,
        "low_52w": 38.20,
        "ma5": 48.10,
        "ma10": 48.50,
        "ma20": 49.20,
        "ma60": 47.80,
        "rsi": 42,
        "macd": -0.35,
        "macd_signal": -0.20,
        "macd_histogram": -0.15,
        "bollinger_upper": 51.20,
        "bollinger_middle": 48.50,
        "bollinger_lower": 45.80,
        "volume_ratio": 0.85,
        "support_levels": [45.00, 42.50, 40.00],
        "resistance_levels": [50.00, 52.50, 55.00],
        "trend": "down",  # up/down/sideways
    },
    "600900": {
        "name": "长江电力",
        "current_price": 27.14,
        "high_52w": 29.50,
        "low_52w": 23.80,
        "ma5": 27.30,
        "ma10": 27.50,
        "ma20": 27.80,
        "ma60": 27.20,
        "rsi": 45,
        "macd": -0.12,
        "macd_signal": -0.08,
        "macd_histogram": -0.04,
        "bollinger_upper": 28.50,
        "bollinger_middle": 27.50,
        "bollinger_lower": 26.50,
        "volume_ratio": 0.90,
        "support_levels": [26.50, 25.50, 24.50],
        "resistance_levels": [28.00, 29.00, 29.50],
        "trend": "sideways",
    },
    "601225": {
        "name": "陕西煤业",
        "current_price": 25.47,
        "high_52w": 32.50,
        "low_52w": 22.80,
        "ma5": 26.20,
        "ma10": 26.80,
        "ma20": 27.50,
        "ma60": 26.50,
        "rsi": 38,
        "macd": -0.55,
        "macd_signal": -0.35,
        "macd_histogram": -0.20,
        "bollinger_upper": 29.00,
        "bollinger_middle": 27.00,
        "bollinger_lower": 25.00,
        "volume_ratio": 1.15,
        "support_levels": [24.50, 23.00, 22.00],
        "resistance_levels": [27.00, 28.50, 30.00],
        "trend": "down",
    },
    "601857": {
        "name": "中国石油",
        "current_price": 11.91,
        "high_52w": 14.50,
        "low_52w": 9.80,
        "ma5": 12.20,
        "ma10": 12.50,
        "ma20": 12.80,
        "ma60": 12.30,
        "rsi": 35,
        "macd": -0.25,
        "macd_signal": -0.15,
        "macd_histogram": -0.10,
        "bollinger_upper": 13.50,
        "bollinger_middle": 12.50,
        "bollinger_lower": 11.50,
        "volume_ratio": 1.20,
        "support_levels": [11.00, 10.50, 10.00],
        "resistance_levels": [12.50, 13.00, 13.50],
        "trend": "down",
    },
    "601158": {
        "name": "重庆水务",
        "current_price": 4.44,
        "high_52w": 5.20,
        "low_52w": 4.10,
        "ma5": 4.42,
        "ma10": 4.45,
        "ma20": 4.48,
        "ma60": 4.50,
        "rsi": 52,
        "macd": 0.02,
        "macd_signal": 0.01,
        "macd_histogram": 0.01,
        "bollinger_upper": 4.65,
        "bollinger_middle": 4.45,
        "bollinger_lower": 4.25,
        "volume_ratio": 0.95,
        "support_levels": [4.30, 4.20, 4.10],
        "resistance_levels": [4.55, 4.65, 4.80],
        "trend": "sideways",
    },
    "600028": {
        "name": "中国石化",
        "current_price": 5.37,
        "high_52w": 6.50,
        "low_52w": 4.80,
        "ma5": 5.40,
        "ma10": 5.45,
        "ma20": 5.50,
        "ma60": 5.42,
        "rsi": 48,
        "macd": -0.05,
        "macd_signal": -0.03,
        "macd_histogram": -0.02,
        "bollinger_upper": 5.70,
        "bollinger_middle": 5.45,
        "bollinger_lower": 5.20,
        "volume_ratio": 0.88,
        "support_levels": [5.20, 5.10, 5.00],
        "resistance_levels": [5.50, 5.65, 5.80],
        "trend": "sideways",
    },
}


def analyze_trend(data):
    """分析趋势"""
    price = data['current_price']
    ma5 = data['ma5']
    ma10 = data['ma10']
    ma20 = data['ma20']
    ma60 = data['ma60']

    signals = []
    score = 50  # 中性分

    # 均线排列分析
    if price > ma5 > ma10 > ma20:
        signals.append("🟢 多头排列")
        score += 20
    elif price < ma5 < ma10 < ma20:
        signals.append("🔴 空头排列")
        score -= 20
    else:
        signals.append("🟡 均线缠绕")

    # 与60日均线关系
    if price > ma60:
        signals.append("🟢 站上长期均线")
        score += 10
    else:
        signals.append("🔴 跌破长期均线")
        score -= 10

    # 趋势方向
    if data['trend'] == 'up':
        signals.append("📈 上升趋势")
        score += 15
    elif data['trend'] == 'down':
        signals.append("📉 下降趋势")
        score -= 15
    else:
        signals.append("↔️ 横盘震荡")

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_momentum(data):
    """分析动量指标"""
    rsi = data['rsi']
    macd = data['macd']
    macd_signal = data['macd_signal']
    macd_hist = data['macd_histogram']

    signals = []
    score = 50

    # RSI分析
    if rsi > 70:
        signals.append(f"🔴 RSI超买 ({rsi})")
        score -= 15
    elif rsi < 30:
        signals.append(f"🟢 RSI超卖 ({rsi})")
        score += 15
    else:
        signals.append(f"🟡 RSI中性 ({rsi})")

    # MACD分析
    if macd > macd_signal:
        signals.append("🟢 MACD金叉")
        score += 15
    elif macd < macd_signal:
        signals.append("🔴 MACD死叉")
        score -= 15

    # MACD柱状图
    if macd_hist > 0 and macd_hist > 0.1:
        signals.append("📈 MACD红柱放大")
        score += 10
    elif macd_hist < 0 and macd_hist < -0.1:
        signals.append("📉 MACD绿柱放大")
        score -= 10

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_support_resistance(data):
    """分析支撑压力位"""
    price = data['current_price']
    supports = data['support_levels']
    resistances = data['resistance_levels']

    signals = []

    # 距离最近支撑位
    nearest_support = max([s for s in supports if s < price], default=supports[0])
    support_distance = ((price - nearest_support) / price) * 100

    # 距离最近压力位
    nearest_resistance = min([r for r in resistances if r > price], default=resistances[0])
    resistance_distance = ((nearest_resistance - price) / price) * 100

    signals.append(f"📍 最近支撑: {nearest_support:.2f} (距当前 {support_distance:.1f}%)")
    signals.append(f"📍 最近压力: {nearest_resistance:.2f} (距当前 {resistance_distance:.1f}%)")

    # 52周位置
    high_52w = data['high_52w']
    low_52w = data['low_52w']
    position_52w = ((price - low_52w) / (high_52w - low_52w)) * 100

    if position_52w > 80:
        signals.append("🔴 接近52周高位")
    elif position_52w < 20:
        signals.append("🟢 接近52周低位")
    else:
        signals.append(f"🟡 52周位置 {position_52w:.0f}%")

    return {
        'signals': signals,
        'nearest_support': nearest_support,
        'nearest_resistance': nearest_resistance,
        'position_52w': position_52w,
    }


def analyze_volume(data):
    """分析成交量"""
    volume_ratio = data['volume_ratio']

    signals = []
    score = 50

    if volume_ratio > 1.5:
        signals.append("📊 放量 (>1.5x)")
        score += 10
    elif volume_ratio < 0.7:
        signals.append("📊 缩量 (<0.7x)")
        score -= 5
    else:
        signals.append(f"📊 正常成交量 ({volume_ratio:.2f}x)")

    return {'score': max(0, min(100, score)), 'signals': signals}


def analyze_bollinger(data):
    """分析布林带"""
    price = data['current_price']
    upper = data['bollinger_upper']
    middle = data['bollinger_middle']
    lower = data['bollinger_lower']

    signals = []

    if price > upper:
        signals.append("🔴 突破布林带上轨（超买）")
    elif price < lower:
        signals.append("🟢 跌破布林带下轨（超卖）")
    elif price > middle:
        signals.append("🟡 在布林带中轨上方")
    else:
        signals.append("🟡 在布林带中轨下方")

    # 布林带宽度
    width = ((upper - lower) / middle) * 100
    if width > 15:
        signals.append("📊 布林带扩张（波动加大）")
    elif width < 5:
        signals.append("📊 布林带收缩（波动减小）")

    return {'signals': signals}


def generate_technical_analysis(code):
    """生成单只股票的技术分析"""
    if code not in PRICE_DATA:
        return None

    data = PRICE_DATA[code]

    trend = analyze_trend(data)
    momentum = analyze_momentum(data)
    sr = analyze_support_resistance(data)
    volume = analyze_volume(data)
    bollinger = analyze_bollinger(data)

    # 综合技术评分
    total_score = (
        trend['score'] * 0.30 +
        momentum['score'] * 0.25 +
        volume['score'] * 0.15 +
        (100 - abs(sr['position_52w'] - 50) * 2) * 0.15 +
        50 * 0.15  # 布林带中性
    )

    if total_score >= 70:
        level = "🟢 技术面强势"
    elif total_score >= 50:
        level = "🟡 技术面中性"
    else:
        level = "🔴 技术面弱势"

    return {
        'code': code,
        'name': data['name'],
        'current_price': data['current_price'],
        'total_score': total_score,
        'level': level,
        'trend': trend,
        'momentum': momentum,
        'support_resistance': sr,
        'volume': volume,
        'bollinger': bollinger,
    }


def generate_technical_report(codes):
    """生成技术分析报告"""
    report = []
    report.append("=" * 70)
    report.append("📊 能源公用事业投资组合 - 技术分析报告")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")

    for code in codes:
        analysis = generate_technical_analysis(code)
        if not analysis:
            continue

        report.append(f"📌 {analysis['name']} ({code})")
        report.append(f"💵 当前价格: {analysis['current_price']:.2f} 元")
        report.append(f"🏆 技术面评分: {analysis['total_score']:.1f}/100 {analysis['level']}")
        report.append("-" * 60)

        report.append("📈 趋势分析:")
        for signal in analysis['trend']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        report.append("⚡ 动量指标:")
        for signal in analysis['momentum']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        report.append("📍 支撑压力位:")
        for signal in analysis['support_resistance']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        report.append("📊 成交量分析:")
        for signal in analysis['volume']['signals']:
            report.append(f"   • {signal}")
        report.append("")

        report.append("📉 布林带分析:")
        for signal in analysis['bollinger']['signals']:
            report.append(f"   • {signal}")
        report.append("")
        report.append("=" * 70)
        report.append("")

    # 综合对比
    report.append("📋 技术面评分对比:")
    report.append("-" * 60)
    analyses = [generate_technical_analysis(c) for c in codes if generate_technical_analysis(c)]
    for a in sorted(analyses, key=lambda x: x['total_score'], reverse=True):
        report.append(f"  {a['name']:<10} {a['total_score']:>5.1f}/100  {a['level']}")
    report.append("")
    report.append("⚠️ 技术分析仅供参考，不构成投资建议")
    report.append("=" * 70)

    return "\n".join(report)


def main():
    """测试"""
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    report = generate_technical_report(codes)
    print(report)


if __name__ == "__main__":
    main()
