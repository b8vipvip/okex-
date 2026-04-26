# 任务管理与执行回传系统 MVP

## 1. 项目结构

- `backend/` FastAPI + SQLAlchemy + Alembic
- `frontend/` Vue3 + Vite + Element Plus
- `examples/import_sample.txt` 导入示例文本

## 2. 本地开发启动

### 2.1 后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 修改 DATABASE_URL / token
alembic upgrade head
python scripts/seed_data.py
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2.2 前端

```bash
cd frontend
npm install
npm run dev
```

默认前端通过 `/api/*` 调后端。

## 3. 生产部署（Ubuntu + 宝塔 + Nginx + systemd）

### 3.1 部署后端到 `/opt/recharge-api/`

```bash
sudo mkdir -p /opt/recharge-api
sudo cp -r backend /opt/recharge-api/
cd /opt/recharge-api/backend
python3 -m venv /opt/recharge-api/.venv
source /opt/recharge-api/.venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
vim .env
alembic upgrade head
```

### 3.2 创建管理员账号和 worker token

在 `.env` 中设置：

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_TOKEN`
- `WORKER_TOKEN`
- `JWT_SECRET`

登录接口 `/api/auth/login` 使用 `ADMIN_USERNAME` 和 `ADMIN_PASSWORD`。

### 3.3 systemd

```bash
sudo cp /opt/recharge-api/backend/deploy/recharge-api.service /etc/systemd/system/recharge-api.service
sudo systemctl daemon-reload
sudo systemctl enable recharge-api
sudo systemctl restart recharge-api
sudo systemctl status recharge-api
```

查看日志：

```bash
journalctl -u recharge-api -f
```

### 3.4 前端构建并部署到宝塔站点目录

```bash
cd frontend
npm install
npm run build
sudo cp -r dist/* /www/wwwroot/your-domain/
```

### 3.5 Nginx 反向代理

参考 `backend/deploy/nginx.conf.example`，重点：

- 前端静态目录：`/www/wwwroot/your-domain/`
- `/api/` -> `http://127.0.0.1:8000/api/`

## 4. API 鉴权说明

- 后台接口：`Authorization: Bearer <admin_token 或登录返回 token>`
- Worker 接口：`X-API-Key: <worker_token>`

## 5. Mock Worker

```bash
cd backend
source .venv/bin/activate
python scripts/mock_worker.py
```

仅演示 heartbeat/claim/start/success/fail 接口调用流程，不含任何第三方自动化逻辑。

## 6. 常见问题排查

1. **前端 401**：检查 localStorage token 是否正确、后端 `.env` 的 `JWT_SECRET` 是否变更。
2. **claim 报错**：检查数据库连接和事务隔离配置，确保 worker 可通过“查询 queued + 条件更新”方式正常抢占任务。
3. **跨域问题**：生产使用同域 Nginx 代理；开发环境使用 Vite proxy。
4. **迁移失败**：检查 `DATABASE_URL` 是否包含 `?charset=utf8mb4`。

## 7. 业务要点覆盖

- UTF-8 txt 导入
- 去空行、去重复、格式校验
- 任务状态流转日志
- 并发安全领取（查询最早 queued 任务 + 条件更新重试）
- 任务分页筛选（默认 id 倒序）
- 仪表盘统计（销售额/成本/利润）


## 8. 代码修改简要记录

- 2026-04-26：新增任务类型（充值/查询价格）贯通后端导入、领取和前端导入/任务列表；新增价格列表页面；批量名称支持按时间自动生成并可手工修改。
