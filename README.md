# 📊 A股投资组合分析系统

> **A-Share Investment Portfolio Analyzer**
> 
> 一个功能完整的A股投资组合实时监控与分析平台，支持实时行情获取、估值分析、深度财务分析和智能股票管理。

---

## ✨ 核心功能

### 📈 实时行情监控
- 实时获取A股价格、涨跌幅、PE(TTM)、PB等核心指标
- 数据源：腾讯财经API（实时）+ 东方财富（财务指标）
- 每5分钟自动更新（仅A股交易时间）
- 交易时间外自动静默，节省资源

### 💰 科学估值模型
- **PE估值**：基于行业历史均值计算合理PE区间
- **PB估值**：市净率横向对比分析
- **股息率估算**：基于真实PE和行业分红率
- **三维度买点**：理想买点 / 合理买点 / 谨慎买点

### 🔬 深度财务分析
- **现金流质量**：经营现金流/净利润比率分析
- **利润质量**：ROE、ROA、毛利率综合评估
- **债务风险**：资产负债率、流动比率分析
- **同业对比**：同板块股票横向估值比较
- **行业自适应评分**：银行/非金融行业差异化标准

### 🎯 智能股票管理
- 输入股票名称或代码即可添加到投资组合
- 自动计算估值买点和投资建议
- 点击股票查看完整分析报告
- 支持批量添加和删除

---

## 🏗️ 技术架构

> **当前标准入口以仓库实际文件为准：** `main.py` → `src/api/app.py`

```
investment-portfolio-analyzer/
├── main.py                         # 标准 Python 启动入口
├── start.sh                        # 标准启动脚本（唯一推荐入口）
├── src/api/app.py                  # Flask 后端 API 服务
├── index.html                      # 默认前端页面
├── enhanced_index.html             # 增强版页面
├── munger_index.html               # 芒格风格页面
├── reports/                        # 分析报告产物
├── logs/                           # 运行日志
├── tmp/                            # 实验脚本（非正式入口）
└── requirements.txt                # Python 依赖
```

### 技术栈
| 层级 | 技术 |
|------|------|
| **前端** | HTML5 + CSS3 + JavaScript (原生) |
| **后端** | Python 3 + Flask + Flask-CORS |
| **数据源** | 腾讯财经API + 东方财富API |
| **部署** | Cloudflare Tunnel (公网暴露) |
| **自动化** | Cron定时任务 (每5分钟) |

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/chengbenchao/investment-portfolio-analyzer.git
cd investment-portfolio-analyzer

# 2. 安装依赖
python3 -m pip install -r requirements.txt

# 3. 标准启动方式（推荐）
./start.sh

# 或直接使用 Python 入口
python3 main.py
```

服务将在 `http://127.0.0.1:8002` 启动。

### 访问网页

打开浏览器访问：`http://127.0.0.1:8002`

### 公网暴露（标准化入口）

```bash
# 仅启动 tunnel（要求本地 8002 服务已启动）
./start_tunnel.sh

# 一键拉起本地服务 + tunnel
./start_public.sh
```

约定：tunnel 永远代理到 `http://127.0.0.1:8002`。
如果未安装 `cloudflared`，脚本会直接报错并提示安装。

### 最小健康检查 / smoke test

健康检查接口：

```bash
curl http://127.0.0.1:8002/healthz
```

数据状态接口：

```bash
curl http://127.0.0.1:8002/api/status
```

启动前自检：

```bash
./selfcheck.sh
```

手动触发一次数据更新：

```bash
./update_data.sh
```

在本地服务启动后执行 smoke test：

```bash
./smoke_test.sh
```

它会验证：
- `/`
- `/classic`
- `/healthz`
- `/api/search?keyword=600519`
- `/api/munger/biases`
- `/api/get_stocks`

---

## 📡 API接口文档

更完整的结构说明见：`docs/architecture.md`

### 健康检查
```
GET /healthz
```
返回服务是否存活，以及当前启用的关键能力。

### 获取数据状态
```
GET /api/status
```

返回最近一次更新尝试时间、成功时间、错误信息、交易窗口信息等。

### 获取所有股票数据
```
GET /api/get_stocks
```
**响应示例：**
```json
{
  "success": true,
  "stocks": [
    {
      "code": "601088",
      "name": "中国神华",
      "currentPrice": 47.73,
      "pe": 20.08,
      "pb": 2.07,
      "dividendYield": 3.24,
      "idealBuy": 22.75,
      "reasonableBuy": 26.16,
      "cautiousBuy": 29.57
    }
  ],
  "count": 7
}
```

### 添加股票
```
POST /api/add
Content-Type: application/json

{
  "keyword": "贵州茅台",
  "sector": "白酒"
}
```

### 深度财务分析
```
GET /api/deep_analysis?code=600036
```

### 搜索股票
```
GET /api/search?keyword=招商银行
```

### 刷新所有数据
```
GET /api/refresh
```

---

## 📊 当前投资组合

| 股票名称 | 代码 | 行业 | 最新价格 | PE(TTM) | 股息率 | 投资建议 |
|---------|------|------|---------|---------|--------|---------|
| 中国神华 | 601088 | 煤炭 | 47.73 | 20.08x | 3.24% | 🔴 观望 |
| 长江电力 | 600900 | 电力 | 27.20 | 18.44x | 3.80% | 🔴 观望 |
| 陕西煤业 | 601225 | 煤炭 | 25.90 | 15.53x | 4.19% | 🔴 观望 |
| 中国石油 | 601857 | 石油 | 11.89 | 13.76x | 3.27% | 🔴 观望 |
| 重庆水务 | 601158 | 水务 | 4.46 | 25.65x | 2.34% | 🟢 理想买点 |
| 中国石化 | 600028 | 石油 | 5.37 | 18.27x | 2.74% | 🟡 合理买点 |
| 招商银行 | 600036 | 银行 | 38.00 | 6.36x | 9.43% | 🔴 观望 |

---

## 🎯 估值方法说明

### 买点计算逻辑
1. 获取行业历史平均PE
2. 计算打折系数：
   - 🟢 **理想买点** = 行业均值 × 50%
   - 🟡 **合理买点** = 行业均值 × 70%
   - 🟠 **谨慎买点** = 行业均值 × 85%
3. 结合当前PE，计算目标价格

### 数据标签说明
| 标签 | 含义 | 示例 |
|------|------|------|
| 🟢 实时 | 腾讯财经API实时获取 | PE、PB、股价 |
| 🟡 估算 | 基于实时数据计算 | 股息率 |
| 🔵 参考 | 行业均值或历史数据 | ROE、毛利率 |

---

## 🔄 自动更新机制

### 更新频率
- **交易时间**：建议每5分钟自动更新
- **非交易时间**：允许跳过，但状态文件仍应记录最近尝试/成功信息

### 标准数据更新入口
```bash
./update_data.sh
```

### A股交易时间
| 时段 | 时间 |
|------|------|
| 上午 | 9:30 - 11:30 |
| 下午 | 13:00 - 15:00 |

---

## 🛠️ 守护运行准备

项目已附带 systemd 服务样板：

- `deploy/investment-portfolio-analyzer.service`

它不是自动安装脚本，但已经把守护运行需要的最小单元文件准备好了。

## 🌐 公网访问

项目已标准化为 Cloudflare Quick Tunnel 方案。

- **本地服务地址**：`http://127.0.0.1:8002`
- **标准 tunnel 脚本**：`./start_tunnel.sh`
- **标准一键公网脚本**：`./start_public.sh`
- **tunnel 日志**：`/tmp/investment-portfolio-tunnel.log`

每次启动 Quick Tunnel 都会生成新的临时地址，格式如：
```
https://xxx-xxx-xxx.trycloudflare.com
```

---

## 📋 开发计划

### 已完成 ✅
- [x] 实时行情获取
- [x] PE/PB估值模型
- [x] 股息率估算
- [x] 添加股票功能
- [x] 深度财务分析
- [x] 行业自适应评分
- [x] 动态股票列表
- [x] 交易时间自动更新

### 进行中 🚧
- [ ] K线图表可视化
- [ ] 实时新闻监控
- [ ] 财报日历提醒

### 计划中 📋
- [ ] 量化回测框架
- [ ] 因子选股模型
- [ ] VaR风险模型
- [ ] 自动调仓系统
- [ ] 港股/美股支持

---

## ⚠️ 免责声明

本项目仅供学习和研究使用，**不构成任何投资建议**。

- 股市有风险，投资需谨慎
- 所有分析数据仅供参考
- 使用者应自行承担投资风险
- 作者不对任何投资损失负责

---

## 📝 License

MIT License

---

## 👨‍💻 作者

**chengbenchao**

- GitHub: https://github.com/chengbenchao

---

## 🙏 致谢

- **数据源**：腾讯财经、东方财富
- **框架**：Flask、Cloudflare Tunnel
- **灵感**：价值投资理念 + 量化分析

---

<p align="center">⭐ 如果这个项目对你有帮助，请给一个Star！</p>
