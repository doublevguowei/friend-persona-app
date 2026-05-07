# friend-persona-app

产品名称：群友人格档案馆

一个给 6 个朋友日常娱乐使用的网页 MVP。朋友打开分享链接后选择自己的身份，每天投票贴标签，系统会生成今日结果、个人档案和历史人格排行榜。

## 功能

- 6 个固定用户选择身份进入。
- 每天自动生成 4 道相同投票题。
- 近 7 天出现过的问题会尽量不重复。
- 每人每天每题只能投一次，不能投给自己。
- 投票会写入历史记录，并给被投票人的对应人格属性加 1。
- 今日结果支持并列第一和毒舌点评。
- 个人档案展示 10 项人格数值、最近称号、今日被投票次数、历史累计被投票次数。
- 排行榜使用全部历史投票记录实时聚合排序。

## 技术栈

- 前端：React + Vite
- 后端：FastAPI + SQLite + SQLAlchemy
- 部署：前后端分离。前端推荐 Vercel / Netlify，后端推荐 Render / Railway / Fly.io。
- 额外支持：根目录 Dockerfile 可把前端和后端打成一个服务，适合快速上线到 Railway / Fly.io / Render Docker。

## 目录结构

```text
friend-persona-app/
  backend/
    main.py
    database.py
    models.py
    schemas.py
    seed.py
    seed_data.py
    requirements.txt
    Dockerfile
    Procfile
    .env.example
  frontend/
    src/
    package.json
    vite.config.js
    vercel.json
    netlify.toml
    .env.example
    .env.production.example
  render.yaml
  Dockerfile
  README.md
```

## 本地运行

### 后端

```bash
cd backend
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

后端默认地址：

```text
http://localhost:8000
```

接口文档：

```text
http://localhost:8000/docs
```

### 前端

```bash
cd frontend
npm install
```

创建 `frontend/.env`：

```env
VITE_API_BASE_URL=http://localhost:8000
```

启动：

```bash
npm run dev
```

前端默认地址：

```text
http://localhost:5173
```

## 环境变量

### 后端

| 名称 | 示例 | 说明 |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///./friend_persona.db` | SQLite 数据库地址 |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` | 允许访问 API 的前端域名，多个域名用英文逗号分隔 |
| `APP_TIMEZONE` | `Asia/Shanghai` | 生成“今日”数据使用的时区 |

### 前端

| 名称 | 示例 | 说明 |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `https://your-api.onrender.com` | 后端 API 地址 |

## 页面

- `/`：首页，选择身份。
- `/vote?user_id=1`：今日投票页。
- `/results`：今日结果页，可复制链接分享。
- `/profile/:user_id`：个人人格档案页。
- `/profiles`：档案选择页。
- `/leaderboard`：历史人格排行榜。

## 接口

- `GET /users`
- `GET /daily-questions`
- `GET /daily-questions?user_id=xxx`
- `POST /vote`
- `GET /results/today`
- `GET /profile/{user_id}`
- `GET /leaderboard`

## 数据初始化

运行：

```bash
cd backend
python seed.py
```

脚本会自动：

- 创建数据库表。
- 插入 6 个固定用户。
- 插入 50 道题库。
- 已存在的数据不会重复插入。

后端启动时也会自动检查并补齐基础数据。

## 推荐上线方案

最省心的方案：

1. 后端部署到 Render。
2. 前端部署到 Vercel。
3. 在 Vercel 设置 `VITE_API_BASE_URL` 为 Render 后端地址。
4. 在 Render 设置 `CORS_ORIGINS` 为 Vercel 前端地址。

最快发给朋友玩的方案：

1. 使用根目录 `Dockerfile` 部署成一个服务。
2. 这个服务会同时提供网页和 API。
3. 前端会用同域名请求 API，不需要单独设置 `VITE_API_BASE_URL`。

## 后端部署到 Render

### 方式一：Blueprint

项目根目录已经提供 `render.yaml`。把代码推到 GitHub 后：

1. 打开 Render。
2. 选择 New + Blueprint。
3. 连接这个仓库。
4. Render 会读取根目录的 `render.yaml` 并创建 `friend-persona-api` 服务。

默认环境变量：

```env
DATABASE_URL=sqlite:///./friend_persona.db
APP_TIMEZONE=Asia/Shanghai
CORS_ORIGINS=*
```

第一次跑通后，建议把 `CORS_ORIGINS` 改成你的 Vercel 域名，例如：

```env
CORS_ORIGINS=https://friend-persona-app.vercel.app
```

### 方式二：手动创建 Web Service

1. New Web Service。
2. Root Directory：`backend`
3. Build Command：

```bash
pip install -r requirements.txt
```

4. Start Command：

```bash
python start.py
```

5. 设置环境变量：

```env
DATABASE_URL=sqlite:///./friend_persona.db
APP_TIMEZONE=Asia/Shanghai
CORS_ORIGINS=*
```

Render 免费实例的本地文件系统可能在服务重建后丢失 SQLite 文件。长期使用建议挂载 Persistent Disk，或升级成托管 PostgreSQL。

## 后端部署到 Railway

1. 新建 Railway 项目并连接仓库。
2. 服务目录设置为 `backend`。
3. Start Command：

```bash
python start.py
```

4. 设置环境变量：

```env
DATABASE_URL=sqlite:///./friend_persona.db
APP_TIMEZONE=Asia/Shanghai
CORS_ORIGINS=https://你的前端域名
```

## 后端 Docker 部署

后端已经提供 `backend/Dockerfile`：

```bash
cd backend
docker build -t friend-persona-api .
docker run -p 8000:8000 -e APP_TIMEZONE=Asia/Shanghai friend-persona-api
```

生产环境如果要保留 SQLite 数据，请把数据库文件目录挂载出来，并设置 `DATABASE_URL` 指向挂载路径。

## 一体化 Docker 部署

根目录已经提供 `Dockerfile`，会先构建前端，再把 `frontend/dist` 放进 FastAPI 服务里。部署后朋友只需要访问一个域名。

本地测试：

```bash
docker build -t friend-persona-app .
docker run -p 8000:8000 friend-persona-app
```

访问：

```text
http://localhost:8000
```

部署到 Railway / Fly.io / Render Docker 时，使用根目录作为构建目录即可。建议设置：

```env
APP_TIMEZONE=Asia/Shanghai
DATABASE_URL=sqlite:///./friend_persona.db
CORS_ORIGINS=*
```

如果部署平台支持持久磁盘，建议把 SQLite 文件放在持久目录，例如：

```env
DATABASE_URL=sqlite:////data/friend_persona.db
```

## 前端部署到 Vercel

项目已提供 `frontend/vercel.json`，支持刷新 `/profile/1`、`/leaderboard` 等前端路由。

1. New Project。
2. Root Directory：`frontend`
3. Build Command：

```bash
npm run build
```

4. Output Directory：

```text
dist
```

5. Environment Variables：

```env
VITE_API_BASE_URL=https://你的后端域名
```

部署完成后，你拿到的 Vercel 域名就是可以分享给朋友的访问链接。

## 前端部署到 Netlify

项目已提供 `frontend/netlify.toml`。

1. Base directory：`frontend`
2. Build command：

```bash
npm run build
```

3. Publish directory：

```text
dist
```

4. Environment Variables：

```env
VITE_API_BASE_URL=https://你的后端域名
```

## 上线后检查

后端：

```text
https://你的后端域名/health
```

应该返回：

```json
{"ok": true, "date": "YYYY-MM-DD"}
```

前端：

1. 打开前端域名。
2. 选择身份。
3. 完成一题投票。
4. 打开 `/results` 看今日结果。
5. 打开 `/leaderboard` 看历史排行榜。

## 数据保留提醒

当前 MVP 使用 SQLite。它适合小群娱乐，但数据保留取决于部署平台的磁盘策略。

- 本地运行：数据库文件在 `backend/friend_persona.db`。
- Render 免费实例：重建服务可能丢数据，需要 Persistent Disk。
- Fly.io：建议挂载 volume。
- Railway：注意服务文件系统策略，长期建议使用 PostgreSQL。

后续如果需要更稳定的线上数据，可以把 `DATABASE_URL` 改为 PostgreSQL，并把模型保持不变继续使用 SQLAlchemy。
