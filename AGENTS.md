# AGENTS.md - A股投资组合分析系统

## 项目目标
这是一个 A 股投资组合分析系统：提供网页界面、行情查询、估值分析、深度财务分析与股票搜索 API。

## 单一真相源（重要）
### 标准启动方式
只认这一条：

```bash
./start.sh
```

它会优先使用项目内 `.venv/bin/python`，否则回退到系统 `python3`。

### 标准公网暴露方式
- 只启动 tunnel：`./start_tunnel.sh`
- 本地服务 + tunnel 一起拉起：`./start_public.sh`

约定：tunnel 永远代理到 `http://127.0.0.1:8002`。

### 标准数据更新方式
- 手动更新：`./update_data.sh`
- 状态查看：`GET /api/status`
- 状态文件：`logs/data_update_status.json`

### 标准 Python 入口
只认这一条：

```bash
python3 main.py
```

`main.py` 再导入 `src/api/app.py` 中的 Flask app。

### 标准监听端口
- `8002`

### 标准首页
- `http://127.0.0.1:8002/`

## 目录职责
- `main.py`：项目标准入口
- `src/api/app.py`：Flask API 主服务
- `start.sh`：唯一标准本地启动脚本
- `start_tunnel.sh`：唯一标准 tunnel 启动脚本
- `start_public.sh`：本地服务 + tunnel 一键启动
- `start_service.sh` / `run_simple.sh`：兼容入口，内部转发到 `start.sh`
- `launch_tunnel.sh` / `start_and_tunnel.sh` / `start_tunnel_and_get_url.sh`：历史入口，内部转发到标准公网脚本
- `index.html` / `enhanced_index.html` / `munger_index.html`：不同前端页面
- `update_data.sh`：唯一标准数据更新入口
- `tmp/`：实验脚本，不视为正式入口
- `logs/`：运行日志
- `reports/`：分析报告产物

## 修改规则
1. 不要再新增新的“主启动脚本”或“主 tunnel 脚本”，除非同时废弃旧入口。
2. 如果改了启动方式，必须同步更新：
   - `README.md`
   - `AGENTS.md`
   - `scripts/check-consistency.sh`
3. 如果新增页面模式，要写清楚：
   - 它是否是默认首页
   - 它与 `index.html` / `enhanced_index.html` / `munger_index.html` 的关系
4. 实验性脚本放 `tmp/`，不要把 `tmp/` 内容写进正式 README 快速开始。

## 已知历史遗留
- 旧脚本曾引用不存在的 `app.py`
- 旧脚本曾错误使用 `venv/`，而实际目录是 `.venv/`
- 某些 tunnel / 启动脚本带有实验性质，不应当视为默认路径

## 开发优先级
1. 保持标准启动链路稳定
2. 保持 API 与前端入口一致
3. 优先补充验证脚本，而不是继续增加手工说明

## 交付标准
一个改动至少应满足：
- 能启动
- 首页能打开
- 至少一个 API 可访问
- 文档与真实入口一致
