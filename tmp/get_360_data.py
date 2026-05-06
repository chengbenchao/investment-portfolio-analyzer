
#!/usr/bin/env python3
"""
获取360（601360）的详细数据
"""

import requests
import json
from datetime import datetime


def get_stock_detail(code):
    """获取股票详细信息"""
    secid = f"1.{code}" if code.startswith('6') else f"0.{code}"
    
    # 基本信息
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&amp;fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f60,f107,f116,f117,f127,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f259,f260,f261,f262,f263,f264,f265,f266,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f277,f278,f279,f280,f281,f282,f283,f284,f285,f286,f287,f288,f289,f290,f291,f292,f293,f294,f295,f296,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,f346,f347,f348,f349,f350,f351,f352,f353,f354,f355,f356,f357,f358,f359,f360,f361,f362,f363,f364,f365,f366,f367,f368,f369,f370,f371,f372,f373,f374,f375,f376,f377,f378,f379,f380,f381,f382,f383,f384,f385,f386,f387,f388,f389,f390,f391,f392,f393,f394,f395,f396,f397,f398,f399,f400,f401,f402,f403,f404,f405,f406,f407,f408,f409,f410,f411,f412,f413,f414,f415,f416,f417,f418,f419,f420,f421,f422,f423,f424,f425,f426,f427,f428,f429,f430,f431,f432,f433,f434,f435,f436,f437,f438,f439,f440,f441,f442,f443,f444,f445,f446,f447,f448,f449,f450,f451,f452,f453,f454,f455,f456,f457,f458,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f469,f470,f471,f472,f473,f474,f475,f476,f477,f478,f479,f480,f481,f482,f483,f484,f485,f486,f487,f488,f489,f490,f491,f492,f493,f494,f495,f496,f497,f498,f499,f500"
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://quote.eastmoney.com'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                return data['data']
    except Exception as e:
        print(f"获取 {code} 详细数据失败: {e}")
    
    return None


def main():
    code = '601360'
    print(f"🚀 正在获取 {code} (三六零) 的详细数据...\n")
    
    detail = get_stock_detail(code)
    
    if detail:
        print("=" * 80)
        print("📊 三六零 (601360) 详细数据")
        print("=" * 80)
        
        # 基本信息
        print(f"\n📋 基本信息:")
        print(f"  股票名称: {detail.get('f58', 'N/A')}")
        print(f"  股票代码: {detail.get('f57', 'N/A')}")
        print(f"  最新价: ¥{detail.get('f43', 0):.2f}")
        print(f"  涨跌额: {detail.get('f169', 0):+.2f}")
        print(f"  涨跌幅: {detail.get('f170', 0):+.2f}%")
        print(f"  今开: ¥{detail.get('f46', 0):.2f}")
        print(f"  昨收: ¥{detail.get('f60', 0):.2f}")
        print(f"  最高: ¥{detail.get('f44', 0):.2f}")
        print(f"  最低: ¥{detail.get('f45', 0):.2f}")
        
        # 成交信息
        print(f"\n📈 成交信息:")
        print(f"  成交量: {detail.get('f47', 0):,.0f}")
        print(f"  成交额: ¥{detail.get('f48', 0):,.0f}")
        print(f"  换手率: {detail.get('f168', 0):.2f}%")
        print(f"  量比: {detail.get('f171', 0):.2f}")
        
        # 市值信息
        print(f"\n💰 市值信息:")
        print(f"  总市值: ¥{detail.get('f116', 0):,.0f}")
        print(f"  流通市值: ¥{detail.get('f117', 0):,.0f}")
        
        # 财务指标
        print(f"\n📊 财务指标:")
        pe = detail.get('f162', 0)
        pb = detail.get('f163', 0)
        roe = detail.get('f173', 0)
        gross_margin = detail.get('f174', 0)
        net_margin = detail.get('f175', 0)
        debt_ratio = detail.get('f176', 0)
        
        print(f"  市盈率(PE): {pe:.2f}" if pe else "  市盈率(PE): N/A")
        print(f"  市净率(PB): {pb:.2f}" if pb else "  市净率(PB): N/A")
        print(f"  ROE: {roe:.2f}%" if roe else "  ROE: N/A")
        print(f"  毛利率: {gross_margin:.2f}%" if gross_margin else "  毛利率: N/A")
        print(f"  净利率: {net_margin:.2f}%" if net_margin else "  净利率: N/A")
        print(f"  资产负债率: {debt_ratio:.2f}%" if debt_ratio else "  资产负债率: N/A")
        
        # 股息率
        dy = detail.get('f188', 0)
        print(f"  股息率: {dy:.2f}%" if dy else "  股息率: N/A")
        
        # 保存原始数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'360_data_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(detail, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 原始数据已保存至: {filename}")
        
        return detail
    
    return None


if __name__ == "__main__":
    main()
