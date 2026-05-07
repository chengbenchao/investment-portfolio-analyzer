# script-governance.md

## 目标
明确本项目所有 `.sh` 脚本的身份，避免“多个脚本都像主入口”。

---

## 一类：正式脚本（推荐长期保留）
这些脚本是当前标准入口，README / AGENTS / 后续 AI 改造应优先使用它们。

- `start.sh`：标准本地启动入口
- `start_public.sh`：标准公网入口（本地服务 + tunnel）
- `start_tunnel.sh`：标准 tunnel 入口
- `update_data.sh`：标准数据更新入口
- `selfcheck.sh`：启动前自检
- `smoke_test.sh`：最小烟雾测试
- `check-consistency.sh`：一致性检查

---

## 二类：兼容脚本（已迁移到 `legacy/`）
这些脚本存在的目的主要是平滑迁移旧习惯。它们不应继续承载独立逻辑。

- `legacy/start_service.sh`
- `legacy/run_simple.sh`
- `legacy/launch_tunnel.sh`
- `legacy/start_and_tunnel.sh`
- `legacy/start_tunnel_and_get_url.sh`
- `legacy/run_update_now.sh`
- `legacy/run_data_update.sh`

治理原则：
- 不再放在仓库根目录冒充正式入口
- 内部只做转发（`exec ./start.sh` / `exec ./start_tunnel.sh` / `exec ./update_data.sh`）
- 后续如确认无人使用，可进一步删除

---

## 三类：遗留/待处置脚本（已迁移到 `legacy/`）
这些脚本要么依赖旧路径、旧端口，要么依赖未落地的旧方案，不应再被视为默认路径。

- `legacy/restart_stocks.sh`：旧 8000 端口 + 旧目录逻辑
- `legacy/start_enhanced.sh`：依赖 `enhanced_app.py` / `venv/` 旧路径
- `legacy/setup_cron.sh`：旧 cron 配置方式，引用路径已失真
- `legacy/update_crontab.sh`：旧 cron 覆盖逻辑，需重写后才能正式使用
- `legacy/start_munger.sh`：可运行，但角色与 `start.sh` 重叠，应当视为历史变体而非标准入口

治理原则：
- 暂不删除
- 明确标注“非标准入口”
- 后续决定是重写、迁移还是删除

---

## 规则
1. 不再新增新的“主启动脚本”。
2. 新能力优先进入正式脚本，而不是新建一个平行入口。
3. 兼容脚本不得继续长业务逻辑。
4. 如果某脚本不是正式入口，必须在文件头注明。
