#!/usr/bin/env python3
"""
阿里云百炼AI分析模块
使用qwen-plus模型进行股票深度分析
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any


class BailianAIAnalyzer:
    """阿里云百炼AI分析器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化AI分析器
        
        Args:
            api_key: 阿里云百炼API密钥，默认从环境变量读取
        """
        self.api_key = api_key or os.getenv('BAILIAN_API_KEY', '')
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model = "qwen-plus"
        
    def _call_ai_api(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        调用阿里云百炼API
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI生成的文本
        """
        if not self.api_key:
            return "⚠️ 未配置阿里云百炼API密钥，请设置 BAILIAN_API_KEY 环境变量"
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'input': {
                    'messages': [
                        {
                            'role': 'system',
                            'content': '你是一位资深的A股分析师，具备CFA级别的金融分析素养。你擅长从财报数据中洞察企业真实经营状况，善于运用技术分析工具捕捉市场趋势信号，并能站在行业视角进行横向对标与估值比较。你的分析风格客观、严谨、数据驱动，始终以事实为依据，不做主观臆断或投资诱导。你会主动提示分析局限性和风险因素，确保用户获得全面、均衡的研究视角。'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                },
                'parameters': {
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                    'result_format': 'message'
                }
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result['output']['choices'][0]['message']['content']
            else:
                return f"⚠️ API调用失败: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"⚠️ AI分析出错: {str(e)}"
    
    def analyze_stock(self, stock_data: Dict, financial_data: Optional[Dict] = None) -> str:
        """
        分析单只股票
        
        Args:
            stock_data: 股票基本数据
            financial_data: 财务数据（可选）
            
        Returns:
            AI分析报告
        """
        prompt = f"""请对以下股票进行专业分析：

【股票基本信息】
- 股票名称：{stock_data.get('name', '未知')}
- 股票代码：{stock_data.get('code', '未知')}
- 所属行业：{stock_data.get('sector', '未知')}
- 当前价格：{stock_data.get('currentPrice', 'N/A')}元
- PE(TTM)：{stock_data.get('pe', 'N/A')}倍
- PB：{stock_data.get('pb', 'N/A')}倍
- 股息率：{stock_data.get('dividendYield', 'N/A')}%
- 理想买点：{stock_data.get('idealBuy', 'N/A')}元
- 合理买点：{stock_data.get('reasonableBuy', 'N/A')}元
- 谨慎买点：{stock_data.get('cautiousBuy', 'N/A')}元
"""
        
        if financial_data:
            prompt += f"""
【财务数据】
- ROE：{financial_data.get('roe', 'N/A')}%
- 毛利率：{financial_data.get('grossMargin', 'N/A')}%
- 净利润：{financial_data.get('netProfit', 'N/A')}亿元
- 资产负债率：{financial_data.get('debtRatio', 'N/A')}%
- 经营现金流：{financial_data.get('operatingCashFlow', 'N/A')}亿元
"""
        
        prompt += """
请从以下维度进行分析：
1. 公司概况与行业地位
2. 估值分析（PE/PB/股息率）
3. 财务健康状况评估
4. 投资风险提示
5. 综合投资建议（仅供参考，不构成投资决策）

请使用Markdown格式输出，语言要专业、客观、严谨。
"""
        
        return self._call_ai_api(prompt, temperature=0.6, max_tokens=2500)
    
    def generate_market_report(self, market_data: List[Dict], date: Optional[str] = None) -> str:
        """
        生成市场分析报告
        
        Args:
            market_data: 市场数据（多只股票）
            date: 报告日期
            
        Returns:
            市场分析报告
        """
        date_str = date or datetime.now().strftime('%Y年%m月%d日')
        
        stock_summary = '\n'.join([
            f"- {s.get('name', 'N/A')}({s.get('code', 'N/A')}): {s.get('currentPrice', 'N/A')}元, PE:{s.get('pe', 'N/A')}倍"
            for s in market_data[:10]
        ])
        
        prompt = f"""请生成一份{date_str}的A股市场分析日报。

【市场概况】
{len(market_data)}只股票数据汇总
部分股票示例：
{stock_summary}

请从以下方面分析：
1. 市场整体概况
2. 板块轮动分析
3. 热点题材解读
4. 资金流向判断
5. 后市展望与风险提示

请使用Markdown格式，语言专业、客观。
"""
        
        return self._call_ai_api(prompt, temperature=0.7, max_tokens=3000)
    
    def analyze_news(self, news_title: str, news_content: str, related_stocks: Optional[List[str]] = None) -> str:
        """
        分析新闻对市场的影响
        
        Args:
            news_title: 新闻标题
            news_content: 新闻内容
            related_stocks: 相关股票列表
            
        Returns:
            新闻影响分析
        """
        stocks_info = ', '.join(related_stocks) if related_stocks else '暂无'
        
        prompt = f"""请分析以下新闻对A股市场的影响：

【新闻标题】
{news_title}

【新闻内容】
{news_content}

【相关股票】
{stocks_info}

请从以下维度分析：
1. 新闻核心要点提炼
2. 对相关板块的影响分析
3. 对整体市场的影响判断
4. 投资机会与风险提示

请使用Markdown格式，客观、专业分析。
"""
        
        return self._call_ai_api(prompt, temperature=0.6, max_tokens=2000)
    
    def compare_stocks(self, stocks_data: List[Dict]) -> str:
        """
        多股票对比分析
        
        Args:
            stocks_data: 多只股票数据
            
        Returns:
            对比分析报告
        """
        stocks_info = '\n'.join([
            f"【{i+1}. {s.get('name', 'N/A')}({s.get('code', 'N/A')})】\n"
            f"   价格: {s.get('currentPrice', 'N/A')}元 | PE: {s.get('pe', 'N/A')}倍 | "
            f"PB: {s.get('pb', 'N/A')}倍 | 股息率: {s.get('dividendYield', 'N/A')}%\n"
            f"   行业: {s.get('sector', 'N/A')}"
            for i, s in enumerate(stocks_data)
        ])
        
        prompt = f"""请对以下股票进行对比分析：

{stocks_info}

请从以下维度对比：
1. 估值水平对比（PE/PB/股息率）
2. 行业地位对比
3. 投资价值对比
4. 风险收益特征对比
5. 配置建议（仅供参考）

请使用Markdown格式，包含对比表格和详细分析。
"""
        
        return self._call_ai_api(prompt, temperature=0.6, max_tokens=3000)


def get_ai_analyzer() -> BailianAIAnalyzer:
    """
    获取AI分析器实例
    
    Returns:
        BailianAIAnalyzer实例
    """
    return BailianAIAnalyzer()


if __name__ == '__main__':
    # 测试代码
    analyzer = get_ai_analyzer()
    
    # 测试股票分析
    test_stock = {
        'name': '贵州茅台',
        'code': '600519',
        'sector': '白酒',
        'currentPrice': 1800.00,
        'pe': 35.5,
        'pb': 12.8,
        'dividendYield': 1.8,
        'idealBuy': 1200.00,
        'reasonableBuy': 1500.00,
        'cautiousBuy': 1700.00
    }
    
    print("=" * 80)
    print("AI分析测试")
    print("=" * 80)
    result = analyzer.analyze_stock(test_stock)
    print(result)
    print("=" * 80)
