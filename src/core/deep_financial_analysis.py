#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度财务分析模块 - 金融工程师版
分析现金流、利润质量、同业对比等
"""

import requests
import json
import os
from datetime import datetime

class DeepFinancialAnalysis:
    """深度财务分析引擎"""
    
    def __init__(self):
        self.stocks = {
            '601088': {'name': '中国神华', 'sector': '煤炭'},
            '600900': {'name': '长江电力', 'sector': '电力'},
            '601225': {'name': '陕西煤业', 'sector': '煤炭'},
            '601857': {'name': '中国石油', 'sector': '石油'},
            '601158': {'name': '重庆水务', 'sector': '水务'},
            '600028': {'name': '中国石化', 'sector': '石油'},
            '600036': {'name': '招商银行', 'sector': '银行'},
        }
    
    def get_financial_data(self, code):
        """获取财务数据（模拟东方财富API）"""
        # 实际应该调用真实API
        # 这里使用预设数据
        financial_data = {
            '601088': {
                'revenue': 3400, 'net_profit': 600, 'operating_cashflow': 800,
                'roe': 0.178, 'roa': 0.12, 'gross_margin': 0.35,
                'debt_ratio': 0.45, 'current_ratio': 2.2,
                'dividend_payout': 0.65, 'eps': 2.37,
                'revenue_growth': 0.08, 'profit_growth': 0.12,
                'cashflow_quality': 1.33,  # 经营现金流/净利润
            },
            '600900': {
                'revenue': 600, 'net_profit': 270, 'operating_cashflow': 350,
                'roe': 0.082, 'roa': 0.03, 'gross_margin': 0.55,
                'debt_ratio': 0.85, 'current_ratio': 1.8,
                'dividend_payout': 0.70, 'eps': 0.55,
                'revenue_growth': 0.05, 'profit_growth': 0.06,
                'cashflow_quality': 1.30,
            },
            '600036': {
                'revenue': 3300, 'net_profit': 1400, 'operating_cashflow': 1500,
                'roe': 0.175, 'roa': 0.012, 'gross_margin': 0.65,
                'debt_ratio': 0.92, 'current_ratio': 1.1,
                'dividend_payout': 0.33, 'eps': 5.98,
                'revenue_growth': 0.02, 'profit_growth': 0.05,
                'cashflow_quality': 1.07,
            },
        }
        return financial_data.get(code, {})
    
    def analyze_cashflow_quality(self, code):
        """分析现金流质量"""
        data = self.get_financial_data(code)
        if not data:
            return {'error': '无数据'}
        
        cashflow_quality = data.get('cashflow_quality', 0)
        net_profit = data.get('net_profit', 0)
        operating_cashflow = data.get('operating_cashflow', 0)
        
        # 评分标准
        if cashflow_quality >= 1.2:
            quality = '优秀', '经营现金流远超净利润，利润质量极高'
        elif cashflow_quality >= 1.0:
            quality = '良好', '经营现金流与净利润匹配，利润质量可靠'
        elif cashflow_quality >= 0.8:
            quality = '一般', '经营现金流略低于净利润，需关注'
        else:
            quality = '较差', '经营现金流严重不足，利润可能存在水分'
        
        return {
            'code': code,
            'name': self.stocks.get(code, {}).get('name', ''),
            'cashflow_quality_ratio': cashflow_quality,
            'operating_cashflow': operating_cashflow,
            'net_profit': net_profit,
            'quality_rating': quality[0],
            'quality_comment': quality[1],
            'score': min(100, cashflow_quality * 75),
        }
    
    def analyze_profit_quality(self, code):
        """分析利润质量（按行业调整标准）"""
        data = self.get_financial_data(code)
        if not data:
            return {'error': '无数据'}
        
        sector = self.stocks.get(code, {}).get('sector', '')
        roe = data.get('roe', 0)
        roa = data.get('roa', 0)
        gross_margin = data.get('gross_margin', 0)
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        
        # 银行/金融行业特殊处理
        if sector == '银行':
            # 银行ROE 17%是优秀，ROA 1.2%是正常的
            roe_score = min(100, roe / 0.20 * 100)  # 20% ROE为满分
            roa_score = min(100, roa / 0.015 * 100)  # 1.5% ROA为满分
            growth_score = min(100, (revenue_growth + profit_growth) / 0.10 * 100)
            score = (roe_score * 0.4 + roa_score * 0.3 + growth_score * 0.3)
        else:
            # 非金融行业标准
            score = (roe * 300 + roa * 500 + gross_margin * 100 + 
                    revenue_growth * 200 + profit_growth * 200) / 5
        
        if score >= 80:
            rating = '优秀'
        elif score >= 60:
            rating = '良好'
        elif score >= 40:
            rating = '一般'
        else:
            rating = '较差'
        
        return {
            'code': code,
            'name': self.stocks.get(code, {}).get('name', ''),
            'roe': roe,
            'roa': roa,
            'gross_margin': gross_margin,
            'revenue_growth': revenue_growth,
            'profit_growth': profit_growth,
            'quality_rating': rating,
            'score': min(100, max(0, score)),
        }
    
    def analyze_debt_risk(self, code):
        """分析债务风险（按行业调整标准）"""
        data = self.get_financial_data(code)
        if not data:
            return {'error': '无数据'}
        
        sector = self.stocks.get(code, {}).get('sector', '')
        debt_ratio = data.get('debt_ratio', 0)
        current_ratio = data.get('current_ratio', 0)
        
        # 银行/金融行业特殊处理
        if sector == '银行':
            # 银行天生高负债，92%是正常的
            if debt_ratio <= 0.93:
                risk = '低', '银行资产负债率在合理范围内，资本充足'
                score = 75
            elif debt_ratio <= 0.95:
                risk = '中', '银行资产负债率略高，需关注资本充足率'
                score = 60
            else:
                risk = '较高', '银行资产负债率偏高'
                score = 40
        else:
            # 非金融行业标准
            if debt_ratio <= 0.4 and current_ratio >= 2.0:
                risk = '低', '资产负债率低，流动比率健康，偿债能力强'
                score = max(0, 100 - debt_ratio * 100)
            elif debt_ratio <= 0.6 and current_ratio >= 1.5:
                risk = '中', '资产负债率可控，流动比率尚可'
                score = max(0, 100 - debt_ratio * 100)
            elif debt_ratio <= 0.8 and current_ratio >= 1.0:
                risk = '较高', '资产负债率偏高，需关注偿债能力'
                score = max(0, 100 - debt_ratio * 100)
            else:
                risk = '高', '资产负债率过高，存在偿债风险'
                score = max(0, 100 - debt_ratio * 100)
        
        return {
            'code': code,
            'name': self.stocks.get(code, {}).get('name', ''),
            'debt_ratio': debt_ratio,
            'current_ratio': current_ratio,
            'risk_rating': risk[0],
            'risk_comment': risk[1],
            'score': score,
        }
    
    def compare_peers(self, code):
        """同业对比分析"""
        sector = self.stocks.get(code, {}).get('sector', '')
        
        # 同板块股票
        peers = [c for c, info in self.stocks.items() 
                if info.get('sector') == sector and c != code]
        
        if not peers:
            return {'error': '无同业数据'}
        
        comparison = {
            'code': code,
            'name': self.stocks.get(code, {}).get('name', ''),
            'sector': sector,
            'peers': []
        }
        
        for peer_code in peers:
            peer_data = self.get_financial_data(peer_code)
            comparison['peers'].append({
                'code': peer_code,
                'name': self.stocks.get(peer_code, {}).get('name', ''),
                'roe': peer_data.get('roe', 0),
                'debt_ratio': peer_data.get('debt_ratio', 0),
                'gross_margin': peer_data.get('gross_margin', 0),
            })
        
        return comparison
    
    def generate_full_report(self, code):
        """生成完整财务分析报告"""
        cashflow = self.analyze_cashflow_quality(code)
        profit = self.analyze_profit_quality(code)
        debt = self.analyze_debt_risk(code)
        peers = self.compare_peers(code)
        
        report = f"""
{'='*70}
📊 深度财务分析报告 - {self.stocks.get(code, {}).get('name', '')} ({code})
{'='*70}
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
💰 一、现金流质量分析
{'='*70}
经营现金流/净利润：{cashflow.get('cashflow_quality_ratio', 0):.2f}
经营现金流：{cashflow.get('operating_cashflow', 0):.0f} 亿元
净利润：{cashflow.get('net_profit', 0):.0f} 亿元
质量评级：{cashflow.get('quality_rating', 'N/A')}
评价：{cashflow.get('quality_comment', 'N/A')}
现金流得分：{cashflow.get('score', 0):.1f}/100

{'='*70}
📈 二、利润质量分析
{'='*70}
ROE（净资产收益率）：{profit.get('roe', 0)*100:.1f}%
ROA（总资产收益率）：{profit.get('roa', 0)*100:.1f}%
毛利率：{profit.get('gross_margin', 0)*100:.1f}%
营收增长率：{profit.get('revenue_growth', 0)*100:.1f}%
利润增长率：{profit.get('profit_growth', 0)*100:.1f}%
质量评级：{profit.get('quality_rating', 'N/A')}
利润得分：{profit.get('score', 0):.1f}/100

{'='*70}
⚠️ 三、债务风险分析
{'='*70}
资产负债率：{debt.get('debt_ratio', 0)*100:.1f}%
流动比率：{debt.get('current_ratio', 0):.2f}
风险评级：{debt.get('risk_rating', 'N/A')}
评价：{debt.get('risk_comment', 'N/A')}
债务得分：{debt.get('score', 0):.1f}/100

{'='*70}
🔄 四、同业对比
{'='*70}
"""
        if 'peers' in peers:
            for peer in peers['peers']:
                report += f"""
{peer['name']} ({peer['code']}):
  ROE: {peer['roe']*100:.1f}% | 负债率：{peer['debt_ratio']*100:.1f}% | 毛利率：{peer['gross_margin']*100:.1f}%
"""
        
        # 综合评分
        total_score = (cashflow.get('score', 0) + profit.get('score', 0) + debt.get('score', 0)) / 3
        
        report += f"""
{'='*70}
🏆 五、综合评分
{'='*70}
现金流质量：{cashflow.get('score', 0):.1f}/100
利润质量：{profit.get('score', 0):.1f}/100
债务风险：{debt.get('score', 0):.1f}/100
─────────────────────────────────────────────────
综合得分：{total_score:.1f}/100

{'='*70}
💡 投资建议
{'='*70}
"""
        if total_score >= 80:
            report += "✅ 财务健康，可重点关注\n"
        elif total_score >= 60:
            report += "🟡 财务状况良好，可适度配置\n"
        elif total_score >= 40:
            report += "⚠️ 财务存在隐忧，需谨慎\n"
        else:
            report += "🔴 财务风险较高，建议回避\n"
        
        report += f"\n{'='*70}\n"
        
        return report


def main():
    """测试函数"""
    analyzer = DeepFinancialAnalysis()
    
    # 分析招商银行
    report = analyzer.generate_full_report('600036')
    print(report)
    
    # 保存报告
    save_path = os.path.join(os.path.dirname(__file__), 'deep_financial_report.txt')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📝 报告已保存至：{save_path}")


if __name__ == "__main__":
    main()
