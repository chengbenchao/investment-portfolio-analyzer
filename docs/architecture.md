# architecture.md

## 项目定位
A股投资组合分析系统，目标是把**网页展示、股票搜索、估值分析、深度财务分析、芒格视角分析**收敛为一个本地可运行、可对外暴露的 Flask Web 应用。

---

## 单一运行链路

### 标准启动链路
```text
start.sh
  -> main.py
    -> src/api/app.py
      -> Flask app (port 8002)
```

### 标准公网链路
```text
start_public.sh
  -> 检查/拉起本地服务 (127.0.0.1:8002)
  -> start_tunnel.sh
    -> Cloudflare Quick Tunnel
```

### 标准数据更新链路
```text
update_data.sh
  -> src/data/fetch_real_data.py
    -> logs/data_update_status.json
```

### 设计原则
1. **只认一个本地入口**：`./start.sh`
2. **只认一个 Python 入口**：`python3 main.py`
3. **只认一个后端服务实现**：`src/api/app.py`
4. **只认一个标准端口**：`8002`
5. 历史脚本可以兼容，但必须收敛到标准入口

---

## 目录职责

### 根目录
- `main.py`：标准 Python 入口，负责加载 `src/` 路径并导入 Flask app
- `start.sh`：标准本地启动脚本
- `start_tunnel.sh`：标准 tunnel 脚本
- `start_public.sh`：标准一键公网脚本
- `README.md`：面向人类的使用说明
- `AGENTS.md`：面向 agent / 维护者的规则说明
- `check-consistency.sh`：最小一致性检查

### 前端页面
- `munger_index.html`：**默认首页**（当前 `/` 路由）
- `index.html`：经典版首页（当前 `/classic` 路由）
- `enhanced_index.html`：增强版页面，目前不是默认入口

### 后端
- `src/api/app.py`：Flask API 主体、路由、页面分发
- `src/utils/`：日志、错误处理等公共能力
- `src/core/`：核心分析逻辑（若存在）

### 数据与产物
- `logs/`：运行日志
- `reports/`：分析报告
- `tmp/`：实验脚本，不视为正式架构的一部分

---

## 页面关系

### `/`
返回：`munger_index.html`

含义：
- 当前默认用户入口
- 强调芒格风格的分析视角

### `/classic`
返回：`index.html`

含义：
- 保留的经典前端入口
- 用于兼容旧页面体验

### `enhanced_index.html`
当前不是正式路由默认页。
如果要把它升级成正式入口，必须同步修改：
- `src/api/app.py`
- `README.md`
- `AGENTS.md`
- `check-consistency.sh`

---

## API 分层

### 1. 基础投资组合 API
- `GET /api/get_stocks`
- `GET /api/search?keyword=...`
- `POST /api/add`
- `GET /api/refresh`
- `GET /api/deep_analysis?code=...`

### 2. 芒格分析 API
- `GET /api/munger/score?code=...`
- `GET /api/munger/portfolio`
- `GET /api/munger/checklist`
- `GET /api/munger/biases`

### 3. 健康检查 API
- `GET /healthz`

### 4. 数据状态 API
- `GET /api/status`

### 设计意图
- **基础 API**：解决“数据获取 / 投资组合管理 / 个股分析”
- **芒格 API**：解决“认知框架 / 检查清单 / 心理偏差 / 组合审视”

---

## 当前已知架构约束

1. 本地访问必须以 `127.0.0.1:8002` 为真相源
2. 所有 tunnel 只能代理到 `127.0.0.1:8002`
3. 不允许再增加新的“主启动脚本”
4. `tmp/` 中的实验脚本不能写进标准快速开始
5. 如果首页路由改了，必须同步更新文档与检查脚本

---

## 当前技术债

1. `.venv` 仍然不完整（只有 Python 链接，没有完整 pip/venv 能力）
2. 历史 tunnel / 启动脚本过多，虽然已收敛，但还未彻底清理
3. 前端多页面的定位还没有完全产品化
4. systemd 守护运行还只是样板，尚未安装为正式服务
5. 数据更新目前还没有正式调度器安装，只完成了标准入口与状态落盘

---

## 推荐的后续演进

### 第一阶段（已完成一部分）
- 启动链路标准化
- tunnel 链路标准化
- 文档与脚本一致性检查

### 第二阶段
- API smoke test
- 健康检查 endpoint
- 首页/页面模式显式切换策略

### 第三阶段
- 定时任务、日志、报告产出统一化
- 更明确的数据更新边界
- 把投资分析逻辑与 Web 层进一步解耦
