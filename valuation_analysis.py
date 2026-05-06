#!/usr/bin/env python3
"""
估值分析模块 - 首席金融分析师第一优先级技能
包含：
1. PE/PB/股息率分析
2. 历史估值百分位计算
3. 理想买点计算
4. 投资建议生成
"""

import json
import os
from datetime import datetime

# 股票配置（包含历史估值参考）
STOCKS_CONFIG = {
    "601088": {
        "name": "中国神华",
        "sector": "煤炭",
        "reference": {
            "pe_avg": 8,  # 历史平均PE
            "pe_low": 6,  # 历史低位PE
            "pb_avg": 1.0,  # 历史平均PB
            "dividend_yield_avg": 6,  # 平均股息率%
            "eps": 5.5,  # 预期EPS
            "bps": 32.5,  # 每股净资产
        }
    },
    "600900": {
        "name": "长江电力",
        "sector": "电力",
        "reference": {
            "pe_avg": 16,
            "pe_low": 12,
            "pb_avg": 2.3,
            "dividend_yield_avg": 4.5,
            "eps": 1.65,
            "bps": 11.5,
        }
    },
    "601225": {
        "name": "陕西煤业",
        "sector": "煤炭",
        "reference": {
            "pe_avg": 7,
            "pe_low": 5,
            "pb_avg": 1.3,
            "dividend_yield_avg": 6.5,
            "eps": 3.0,
            "bps": 14.0,
        }
    },
    "601857": {
        "name": "中国石油",
        "sector": "石油",
        "reference": {
            "pe_avg": 12,
            "pe_low": 8,
            "pb_avg": 0.8,
            "dividend_yield_avg": 4.8,
            "eps": 0.95,
            "bps": 10.8,
        }
    },
    "601158": {
        "name": "重庆水务",
        "sector": "水务",
        "reference": {
            "pe_avg": 14,
            "pe_low": 10,
            "pb_avg": 1.6,
            "dividend_yield_avg": 4.2,
            "eps": 0.5,
            "bps": 4.5,
        }
    },
    "600028": {
        "name": "中国石化",
        "sector": "石化",
        "reference": {
            "pe_avg": 10,
            "pe_low": 7,
            "pb_avg": 0.9,
            "dividend_yield_avg": 5.2,
            "eps": 0.85,
            "bps": 8.2,
        }
    },
}


class StockValuation:
    """单只股票估值分析"""

    def __init__(self, code, current_price):
        self.code = code
        self.current_price = current_price
        self.config = STOCKS_CONFIG.get(code, {})
        self.name = self.config.get("name", code)
        self.reference = self.config.get("reference", {})

    def calculate_metrics(self):
        """计算估值指标"""
        ref = self.reference
        price = self.current_price

        metrics = {
            "pe": price / ref["eps"] if ref["eps"] else None,
            "pb": price / ref["bps"] if ref["bps"] else None,
            "dividend_yield": (ref["eps"] * 0.6 / price * 100) if ref["eps"] else None,
            # 假设分红率60%
        }

        return metrics

    def calculate_buy_points(self):
        """计算买点"""
        ref = self.reference
        metrics = self.calculate_metrics()

        # 方法1: 基于历史低位PE
        ideal_by_pe = ref["pe_low"] * ref["eps"]

        # 方法2: 基于目标股息率5%
        ideal_by_dividend = (ref["eps"] * 0.6 / 0.05) if ref["eps"] else None

        # 方法3: 基于历史低位PB
        ideal_by_pb = ref["pb_avg"] * 0.7 * ref["bps"]

        # 综合判断（取保守值）
        candidates = [ideal_by_pe]
        if ideal_by_dividend:
            candidates.append(ideal_by_dividend)
        candidates.append(ideal_by_pb)

        ideal_point = min(candidates)  # 最保守的买点
        reasonable_point = ideal_point * 1.15  # 理想买点上浮15%
        cautious_point = ideal_point * 1.3  # 理想买点上浮30%

        return {
            "ideal": round(ideal_point, 2),
            "reasonable": round(reasonable_point, 2),
            "cautious": round(cautious_point, 2),
            "detail": {
                "by_pe": round(ideal_by_pe, 2),
                "by_dividend": round(ideal_by_dividend, 2) if ideal_by_dividend else None,
                "by_pb": round(ideal_by_pb, 2),
            }
        }

    def generate_advice(self):
        """生成投资建议"""
        metrics = self.calculate_metrics()
        buy_points = self.calculate_buy_points()

        current_price = self.current_price
        ideal = buy_points["ideal"]
        reasonable = buy_points["reasonable"]
        cautious = buy_points["cautious"]

        if current_price <= ideal:
            signal = "🟢 理想买点"
            rating = "强烈推荐买入"
        elif current_price <= reasonable:
            signal = "🟡 合理买点"
            rating = "推荐买入"
        elif current_price <= cautious:
            signal = "🟠 谨慎买点"
            rating = "少量建仓"
        else:
            signal = "🔴 建议观望"
            rating = "等待更好机会"

        return {
            "name": self.name,
            "current_price": current_price,
            "ideal": ideal,
            "reasonable": reasonable,
            "cautious": cautious,
            "signal": signal,
            "rating": rating,
            "metrics": metrics,
            "buy_points_detail": buy_points["detail"],
        }


class PortfolioValuation:
    """投资组合估值分析"""

    def __init__(self, prices_dict):
        self.prices = prices_dict
        self.analyses = {}

        for code, price in prices_dict.items():
            if code in STOCKS_CONFIG:
                self.analyses[code] = StockValuation(code, price)

    def generate_full_report(self):
        """生成完整分析报告"""
        report = []
        report.append("=" * 70)
        report.append("📊 能源公用事业投资组合 - 估值分析报告")
        report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        report.append("")

        # 每只股票分析
        for code, analysis in self.analyses.items():
            advice = analysis.generate_advice()

            report.append(f"📌 {advice['name']} ({code})")
            report.append("-" * 60)
            report.append(f"💵 当前价格: {advice['current_price']} 元")
            report.append("")
            report.append(f"🎯 买点建议:")
            report.append(f"   🟢 理想买点: ≤ {advice['ideal']} 元")
            report.append(f"   🟡 合理买点: ≤ {advice['reasonable']} 元")
            report.append(f"   🟠 谨慎买点: ≤ {advice['cautious']} 元")
            report.append("")
            report.append(f"📈 估值指标:")
            m = advice["metrics"]
            if m["pe"]:
                report.append(f"   PE: {m['pe']:.2f}x (历史平均: {STOCKS_CONFIG[code]['reference']['pe_avg']}x)")
            if m["pb"]:
                report.append(f"   PB: {m['pb']:.2f}x (历史平均: {STOCKS_CONFIG[code]['reference']['pb_avg']}x)")
            if m["dividend_yield"]:
                report.append(f"   预期股息率: {m['dividend_yield']:.2f}% (目标: 5%+)")
            report.append("")
            report.append(f"💡 投资建议: {advice['signal']} - {advice['rating']}")
            report.append("")
            report.append(f"📊 买点计算依据:")
            detail = advice["buy_points_detail"]
            report.append(f"   基于历史低位PE: {detail['by_pe']} 元")
            if detail['by_dividend']:
                report.append(f"   基于目标股息率5%: {detail['by_dividend']} 元")
            report.append(f"   基于历史低位PB: {detail['by_pb']} 元")
            report.append("")

        # 总结
        report.append("=" * 70)
        report.append("📋 总体建议:")
        report.append("   - 优先考虑 🟢 理想买点的股票")
        report.append("   - 其次考虑 🟡 合理买点的股票")
        report.append("   - 🟠 谨慎买点少量参与")
        report.append("   - 🔴 耐心等待更好机会")
        report.append("")
        report.append("⚠️ 风险提示: 以上分析仅供参考，不构成投资建议")
        report.append("=" * 70)

        return "\n".join(report)

    def save_report(self, filepath):
        """保存报告到文件"""
        report = self.generate_full_report()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        return filepath


def main():
    """测试"""
    # 测试数据（当前真实价格）
    prices = {
        "601088": 47.42,
        "600900": 27.11,
        "601225": 25.39,
        "601857": 11.93,
        "601158": 4.44,
        "600028": 5.35,
    }

    portfolio = PortfolioValuation(prices)
    report = portfolio.generate_full_report()
    print(report)

    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"valuation_report_{timestamp}.txt"
    portfolio.save_report(save_path)
    print(f"\n📝 报告已保存到: {save_path}")


if __name__ == "__main__":
    main()
