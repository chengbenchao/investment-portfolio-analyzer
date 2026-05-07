
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查理·芒格投资分析模块

功能：
- 四维度评分（商业模式、管理层、财务质量、估值）
- 心理偏差自检
- 芒格式建议生成
- 决策检查清单

作者：A股分析师
版本：1.0
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class MungerAnalyzer:
    """芒格投资分析器"""
    
    # 预设股票评分（基于行业常识）
    STOCK_SCORES = {
        '600519': {
            'business': 9, 'management': 8, 'finance': 9, 'valuation': 6,
            'overall': 8.2, 'advice': '等待',
            'suggestion': '这是一家优秀的公司，但当前价格不够诱人。耐心等待，市场会给你机会的。记住，好公司也要有好价格。'
        },
        '000858': {
            'business': 8, 'management': 7, 'finance': 8, 'valuation': 7,
            'overall': 7.5, 'advice': '观望',
            'suggestion': '作为白酒行业的重要玩家，公司质地不错。但白酒行业整体估值偏高，且面临消费习惯变化的挑战。建议观望为主。'
        },
        '601888': {
            'business': 7, 'management': 7, 'finance': 7, 'valuation': 7,
            'overall': 7.0, 'advice': '观望',
            'suggestion': '免税行业的长期逻辑仍在，但需要跟踪疫情后消费复苏的强度。当前估值不算便宜，建议等待更明确的信号。'
        },
        '600029': {
            'business': 6, 'management': 7, 'finance': 6, 'valuation': 7,
            'overall': 6.5, 'advice': '观望',
            'suggestion': '航空业是典型的周期性行业。虽然短期有复苏预期，但长期来看，这不是一个容易赚大钱的行业。谨慎参与。'
        },
        '600900': {
            'business': 9, 'management': 8, 'finance': 9, 'valuation': 8,
            'overall': 8.5, 'advice': '持有',
            'suggestion': '这是一个可以"睡得着觉"的投资。商业模式简单易懂，现金流稳定。作为组合的压舱石，继续持有。'
        },
        '600036': {
            'business': 8, 'management': 8, 'finance': 9, 'valuation': 9,
            'overall': 8.5, 'advice': '持有',
            'suggestion': '招商银行是银行业的优质标的，商业模式清晰，管理层优秀。估值合理，建议持有。'
        },
        '601088': {
            'business': 7, 'management': 7, 'finance': 8, 'valuation': 8,
            'overall': 7.5, 'advice': '观望',
            'suggestion': '中国神华是煤炭行业的龙头，现金流稳定。但行业面临长期挑战，建议观望等待更好时机。'
        }
    }
    
    # 决策检查清单
    CHECKLIST = [
        '商业模式分析完成',
        '竞争优势分析完成',
        '管理层评估完成',
        '估值分析完成',
        '已冷静思考至少24小时',
        '已考虑过反面证据',
        '已检查是否存在心理偏差'
    ]
    
    # 心理偏差列表
    BIASES = [
        '确认偏差 - 只看支持自己观点的信息',
        '过度自信 - 是不是觉得自己知道得比市场多',
        '避免怀疑 - 是不是想快速做点什么来缓解焦虑',
        '羊群效应 - 是不是在跟着别人买卖',
        '损失厌恶 - 对损失的恐惧远超对收益的渴望',
        '过度乐观 - 高估成功概率'
    ]
    
    def __init__(self):
        self.last_decision_time = None
    
    def get_score(self, code: str) -> Dict[str, Any]:
        """获取股票芒格评分"""
        if code in self.STOCK_SCORES:
            return self.STOCK_SCORES[code]
        
        # 默认评分
        return {
            'business': 7, 'management': 7, 'finance': 7, 'valuation': 7,
            'overall': 7.0, 'advice': '观望',
            'suggestion': '建议完成四维度分析后再做决策。记住，投资要耐心，不要急于行动。'
        }
    
    def analyze_portfolio(self, stocks: List[Dict]) -> Dict[str, Any]:
        """分析投资组合整体状态"""
        total_score = 0.0
        score_count = 0
        
        for stock in stocks:
            code = stock.get('code', '')
            score = self.get_score(code)
            total_score += score['overall']
            score_count += 1
        
        avg_score = round(total_score / score_count if score_count > 0 else 0, 1)
        
        # 分析市场情绪
        avg_change = sum(s.get('changePercent', 0) for s in stocks) / len(stocks) if stocks else 0
        
        if avg_change > 1:
            market_mood = '偏乐观'
            mood_emoji = '😊'
        elif avg_change < -1:
            market_mood = '偏谨慎'
            mood_emoji = '😟'
        else:
            market_mood = '中性'
            mood_emoji = '😐'
        
        # 检查是否有大幅下跌
        big_drop = any(s.get('changePercent', 0) < -3 for s in stocks)
        
        return {
            'average_score': avg_score,
            'market_mood': market_mood,
            'mood_emoji': mood_emoji,
            'big_drop': big_drop,
            'average_change': round(avg_change, 2),
            'cooling_down': self._check_cooling_down()
        }
    
    def _check_cooling_down(self) -> bool:
        """检查是否过了冷静期"""
        if not self.last_decision_time:
            return True
        
        hours_passed = (datetime.now() - self.last_decision_time).total_seconds() / 3600
        return hours_passed >= 24
    
    def record_decision(self):
        """记录决策时间"""
        self.last_decision_time = datetime.now()
    
    def get_checklist(self) -> List[Dict[str, Any]]:
        """获取决策检查清单"""
        return [{'item': item, 'checked': False} for item in self.CHECKLIST]
    
    def get_biases(self) -> List[str]:
        """获取心理偏差列表"""
        return self.BIASES
    
    def get_munger_advice(self, stock: Dict) -> Dict[str, Any]:
        """获取芒格式投资建议"""
        code = stock.get('code', '')
        score = self.get_score(code)
        name = stock.get('name', '该股票')
        
        # 根据评分给出建议图标
        if score['advice'] == '持有':
            advice_icon = '🟢'
        elif score['advice'] == '等待':
            advice_icon = '🟡'
        else:
            advice_icon = '🔴'
        
        return {
            **score,
            'advice_icon': advice_icon,
            'advice_text': f"{advice_icon} {score['advice']}",
            'stock_name': name,
            'detailed_suggestion': score['suggestion'],
            'progress_bars': {
                'business': self._get_progress_bar(score['business']),
                'management': self._get_progress_bar(score['management']),
                'finance': self._get_progress_bar(score['finance']),
                'valuation': self._get_progress_bar(score['valuation'])
            }
        }
    
    def _get_progress_bar(self, value: int, max_value: int = 10) -> str:
        """生成进度条"""
        filled = min(value, max_value)
        return '█' * filled + '░' * (max_value - filled)
    
    def generate_report_summary(self, stocks: List[Dict]) -> Dict[str, Any]:
        """生成芒格报告摘要"""
        portfolio_analysis = self.analyze_portfolio(stocks)
        
        # 生成配置建议
        high_quality_stocks = [s for s in stocks if self.get_score(s.get('code'))['overall'] >= 8]
        suggestions = [
            '耐心等待 - 好公司常有，但好价格不常有',
            f'关注{len(high_quality_stocks)}只高质量标的的买入机会',
            '定期检视 - 每月回顾一次组合，检查投资逻辑'
        ]
        
        return {
            'munger_decision_status': {
                'cooling_down': portfolio_analysis['cooling_down'],
                'checklist_progress': '0/7',
                'market_mood': portfolio_analysis['market_mood'],
                'mood_emoji': portfolio_analysis['mood_emoji'],
                'big_drop': portfolio_analysis['big_drop']
            },
            'munger_suggestions': suggestions,
            'average_score': portfolio_analysis['average_score']
        }


# 全局实例
munger_analyzer = MungerAnalyzer()
