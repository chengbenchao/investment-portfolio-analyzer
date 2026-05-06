#!/usr/bin/env python3
"""
增强版股票分析报告生成器
生成专业、美观的Markdown/HTML格式报告
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from .ai_analyzer import get_ai_analyzer


class EnhancedReportGenerator:
    """增强版报告生成器"""
    
    def __init__(self, reports_dir: Optional[str] = None):
        """
        初始化报告生成器
        
        Args:
            reports_dir: 报告保存目录
        """
        self.reports_dir = Path(reports_dir) if reports_dir else Path(__file__).parent.parent.parent / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.ai_analyzer = get_ai_analyzer()
    
    def generate_stock_report(self, stock_data: Dict, financial_data: Optional[Dict] = None, 
                             include_ai_analysis: bool = True) -> str:
        """
        生成单只股票的详细分析报告
        
        Args:
            stock_data: 股票基本数据
            financial_data: 财务数据
            include_ai_analysis: 是否包含AI分析
            
        Returns:
            Markdown格式的报告
        """
        stock_name = stock_data.get('name', '未知股票')
        stock_code = stock_data.get('code', 'N/A')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = []
        
        # 报告标题
        report.append(f"# 📊 {stock_name}({stock_code}) 深度分析报告")
        report.append("")
        report.append(f"> **生成时间**：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report.append(f"> **分析工具**：A股投资分析助手 + 阿里云百炼qwen-plus")
        report.append("")
        
        # 免责声明
        report.append("---")
        report.append("## ⚠️ 免责声明")
        report.append("")
        report.append("本报告仅供学习和研究使用，**不构成任何投资建议**。")
        report.append("- 股市有风险，投资需谨慎")
        report.append("- 所有分析数据仅供参考")
        report.append("- 使用者应自行承担投资风险")
        report.append("")
        
        # 基本信息卡片
        report.append("---")
        report.append("## 📋 基本信息")
        report.append("")
        
        current_price = stock_data.get('currentPrice', 'N/A')
        pe = stock_data.get('pe', 'N/A')
        pb = stock_data.get('pb', 'N/A')
        dividend_yield = stock_data.get('dividendYield', 'N/A')
        
        # 判断投资建议
        ideal_buy = stock_data.get('idealBuy', 0)
        reasonable_buy = stock_data.get('reasonableBuy', 0)
        cautious_buy = stock_data.get('cautiousBuy', 0)
        
        try:
            price_float = float(current_price) if current_price != 'N/A' else 999999
            if price_float <= ideal_buy:
                suggestion = "🟢 **理想买点** - 强烈关注"
            elif price_float <= reasonable_buy:
                suggestion = "🟡 **合理买点** - 适度关注"
            elif price_float <= cautious_buy:
                suggestion = "🟠 **谨慎买点** - 轻仓试探"
            else:
                suggestion = "🔴 **观望** - 等待更好时机"
        except:
            suggestion = "⚠️ 数据不足"
        
        report.append("| 指标 | 数值 |")
        report.append("|------|------|")
        report.append(f"| 股票名称 | {stock_name} |")
        report.append(f"| 股票代码 | {stock_code} |")
        report.append(f"| 所属行业 | {stock_data.get('sector', 'N/A')} |")
        report.append(f"| 当前价格 | {current_price} 元 |")
        report.append(f"| PE(TTM) | {pe} 倍 |")
        report.append(f"| PB | {pb} 倍 |")
        report.append(f"| 股息率 | {dividend_yield}% |")
        report.append(f"| **投资建议** | **{suggestion}** |")
        report.append("")
        
        # 估值区间
        report.append("---")
        report.append("## 💰 估值区间分析")
        report.append("")
        report.append(f"- 🟢 **理想买点**：{ideal_buy} 元 (行业均值 × 50%)")
        report.append(f"- 🟡 **合理买点**：{reasonable_buy} 元 (行业均值 × 70%)")
        report.append(f"- 🟠 **谨慎买点**：{cautious_buy} 元 (行业均值 × 85%)")
        report.append("")
        
        # 财务分析（如果有）
        if financial_data:
            report.append("---")
            report.append("## 📈 财务健康状况")
            report.append("")
            report.append("| 财务指标 | 数值 | 评价 |")
            report.append("|----------|------|------|")
            report.append(f"| ROE | {financial_data.get('roe', 'N/A')}% | - |")
            report.append(f"| 毛利率 | {financial_data.get('grossMargin', 'N/A')}% | - |")
            report.append(f"| 净利润 | {financial_data.get('netProfit', 'N/A')}亿元 | - |")
            report.append(f"| 资产负债率 | {financial_data.get('debtRatio', 'N/A')}% | - |")
            report.append(f"| 经营现金流 | {financial_data.get('operatingCashFlow', 'N/A')}亿元 | - |")
            report.append("")
        
        # AI深度分析
        if include_ai_analysis:
            report.append("---")
            report.append("## 🤖 AI深度分析")
            report.append("")
            report.append("*以下分析由阿里云百炼 qwen-plus 模型生成：*")
            report.append("")
            
            ai_analysis = self.ai_analyzer.analyze_stock(stock_data, financial_data)
            report.append(ai_analysis)
            report.append("")
        
        # 风险提示
        report.append("---")
        report.append("## ⚠️ 风险提示")
        report.append("")
        report.append("### 市场风险")
        report.append("- 宏观经济波动风险")
        report.append("- 政策调整风险")
        report.append("- 市场情绪波动风险")
        report.append("")
        report.append("### 公司风险")
        report.append("- 行业竞争加剧风险")
        report.append("- 业绩不及预期风险")
        report.append("- 经营管理风险")
        report.append("")
        
        # 总结
        report.append("---")
        report.append("## 📝 总结")
        report.append("")
        report.append(f"**{stock_name}({stock_code})** 当前价格 {current_price} 元，")
        report.append(f"PE {pe} 倍，PB {pb} 倍，股息率 {dividend_yield}%。")
        report.append("")
        report.append("---")
        report.append("")
        report.append("*本报告由A股投资分析助手自动生成，数据仅供参考，不构成投资建议。*")
        
        # 保存报告
        report_content = '\n'.join(report)
        filename = f"{stock_code}_{stock_name}_analysis_{timestamp}.md"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 报告已保存到: {filepath}")
        
        return report_content
    
    def generate_market_daily_report(self, stocks_data: List[Dict], 
                                    include_ai_analysis: bool = True) -> str:
        """
        生成市场日报
        
        Args:
            stocks_data: 股票数据列表
            include_ai_analysis: 是否包含AI分析
            
        Returns:
            Markdown格式的市场日报
        """
        date_str = datetime.now().strftime('%Y年%m月%d日')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = []
        
        # 报告标题
        report.append(f"# 📈 A股市场日报 - {date_str}")
        report.append("")
        report.append(f"> **生成时间**：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report.append(f"> **统计范围**：{len(stocks_data)} 只股票")
        report.append("")
        
        # 免责声明
        report.append("---")
        report.append("## ⚠️ 免责声明")
        report.append("")
        report.append("本报告仅供学习和研究使用，**不构成任何投资建议**。")
        report.append("")
        
        # 市场概览
        report.append("---")
        report.append("## 📊 市场概览")
        report.append("")
        
        # 计算统计数据
        try:
            pe_values = [float(s.get('pe', 0)) for s in stocks_data if s.get('pe') and str(s.get('pe')).replace('.', '', 1).isdigit()]
            pb_values = [float(s.get('pb', 0)) for s in stocks_data if s.get('pb') and str(s.get('pb')).replace('.', '', 1).isdigit()]
            dy_values = [float(s.get('dividendYield', 0)) for s in stocks_data if s.get('dividendYield') and str(s.get('dividendYield')).replace('.', '', 1).isdigit()]
            
            avg_pe = sum(pe_values) / len(pe_values) if pe_values else 0
            avg_pb = sum(pb_values) / len(pb_values) if pb_values else 0
            avg_dy = sum(dy_values) / len(dy_values) if dy_values else 0
            
            report.append("| 统计指标 | 数值 |")
            report.append("|----------|------|")
            report.append(f"| 股票数量 | {len(stocks_data)} 只 |")
            report.append(f"| 平均PE(TTM) | {avg_pe:.2f} 倍 |")
            report.append(f"| 平均PB | {avg_pb:.2f} 倍 |")
            report.append(f"| 平均股息率 | {avg_dy:.2f}% |")
            report.append("")
        except Exception as e:
            report.append(f"*统计计算出错: {e}*")
            report.append("")
        
        # 股票列表
        report.append("---")
        report.append("## 📋 股票详情")
        report.append("")
        report.append("| 股票名称 | 代码 | 行业 | 价格 | PE | PB | 股息率 | 建议 |")
        report.append("|---------|------|------|------|----|----|--------|------|")
        
        for stock in stocks_data:
            name = stock.get('name', 'N/A')
            code = stock.get('code', 'N/A')
            sector = stock.get('sector', 'N/A')
            price = stock.get('currentPrice', 'N/A')
            pe = stock.get('pe', 'N/A')
            pb = stock.get('pb', 'N/A')
            dy = stock.get('dividendYield', 'N/A')
            
            # 简化版建议
            try:
                price_float = float(price) if price != 'N/A' else 999999
                ideal = float(stock.get('idealBuy', 0)) if stock.get('idealBuy') else 0
                reasonable = float(stock.get('reasonableBuy', 0)) if stock.get('reasonableBuy') else 0
                
                if price_float <= ideal:
                    suggestion = "🟢 理想"
                elif price_float <= reasonable:
                    suggestion = "🟡 合理"
                else:
                    suggestion = "🔴 观望"
            except:
                suggestion = "⚠️"
            
            report.append(f"| {name} | {code} | {sector} | {price} | {pe} | {pb} | {dy}% | {suggestion} |")
        
        report.append("")
        
        # AI市场分析
        if include_ai_analysis:
            report.append("---")
            report.append("## 🤖 AI市场分析")
            report.append("")
            report.append("*以下分析由阿里云百炼 qwen-plus 模型生成：*")
            report.append("")
            
            ai_analysis = self.ai_analyzer.generate_market_report(stocks_data)
            report.append(ai_analysis)
            report.append("")
        
        # 保存报告
        report_content = '\n'.join(report)
        filename = f"market_daily_{timestamp}.md"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 市场日报已保存到: {filepath}")
        
        return report_content
    
    def generate_comparison_report(self, stocks_data: List[Dict]) -> str:
        """
        生成多股票对比分析报告
        
        Args:
            stocks_data: 多只股票数据
            
        Returns:
            Markdown格式的对比报告
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = []
        
        # 报告标题
        stock_names = '、'.join([s.get('name', 'N/A') for s in stocks_data])
        report.append(f"# 📊 股票对比分析报告：{stock_names}")
        report.append("")
        report.append(f"> **生成时间**：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report.append("")
        
        # 免责声明
        report.append("---")
        report.append("## ⚠️ 免责声明")
        report.append("")
        report.append("本报告仅供学习和研究使用，**不构成任何投资建议**。")
        report.append("")
        
        # 对比表格
        report.append("---")
        report.append("## 📋 核心指标对比")
        report.append("")
        
        # 构建表头
        headers = ["指标"] + [s.get('name', f'股票{i+1}') for i, s in enumerate(stocks_data)]
        report.append("| " + " | ".join(headers) + " |")
        report.append("| " + " | ".join(["------"] * len(headers)) + " |")
        
        # 数据行
        metrics = [
            ("股票代码", "code"),
            ("所属行业", "sector"),
            ("当前价格", "currentPrice", "元"),
            ("PE(TTM)", "pe", "倍"),
            ("PB", "pb", "倍"),
            ("股息率", "dividendYield", "%"),
            ("理想买点", "idealBuy", "元"),
            ("合理买点", "reasonableBuy", "元"),
        ]
        
        for metric_name, metric_key, *suffix in metrics:
            suffix = suffix[0] if suffix else ""
            row = [metric_name]
            for stock in stocks_data:
                value = stock.get(metric_key, 'N/A')
                row.append(f"{value}{suffix}" if value != 'N/A' else 'N/A')
            report.append("| " + " | ".join(row) + " |")
        
        report.append("")
        
        # AI对比分析
        report.append("---")
        report.append("## 🤖 AI深度对比分析")
        report.append("")
        report.append("*以下分析由阿里云百炼 qwen-plus 模型生成：*")
        report.append("")
        
        ai_analysis = self.ai_analyzer.compare_stocks(stocks_data)
        report.append(ai_analysis)
        report.append("")
        
        # 保存报告
        report_content = '\n'.join(report)
        filename = f"comparison_{timestamp}.md"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 对比报告已保存到: {filepath}")
        
        return report_content


def get_report_generator() -> EnhancedReportGenerator:
    """
    获取报告生成器实例
    
    Returns:
        EnhancedReportGenerator实例
    """
    return EnhancedReportGenerator()


if __name__ == '__main__':
    # 测试代码
    generator = get_report_generator()
    
    # 测试单股票报告
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
    print("生成单股票报告测试")
    print("=" * 80)
    generator.generate_stock_report(test_stock, include_ai_analysis=False)
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
