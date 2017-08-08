# GitDigger

一个能够挖掘和推广开源项目各种趣事的网站，在这里你能够：

- 了解到开源社区里都在发生哪些事情
- 看到其他人都在写什么代码，又都在讨论什么问题
- 找到最近比较活跃的开发者和开源项目
- 发现有哪些开源软件发布了新版本
- 分享其它开源项目里的那些长见识的问题（Issue）和拉取请求（PullRequest）

目前还处于开发阶段，很多功能未完成，如果你是 Python 大佬，可以向此项目提供技术支持，包括但不仅限于：数据库表结构设计、性能优化、代码规范、模块规划、国际化。

## 快速开始

### 安装

GitDigger 依赖于以下软件：

- [Flask](https://github.com/pallets/flask) - a microframework for Python.
- [Flask-Script](https://github.com/smurfix/flask-script) - Flask extension to help writing external scripts for Flask applications.
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) - Adds SQLAlchemy support to Flask.
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) - SQLAlchemy database migrations for Flask applications using Alembic
- [Flask-Login](https://github.com/maxcountryman/flask-login) - Flask user session management. 
- [Flask-WTF](https://github.com/lepture/flask-wtf) - Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration.
- [GitHub-Flask](https://github.com/cenkalti/github-flask) - Flask extension for authenticating users with GitHub and making requests to the API. 
- [GitHub-Webhook](https://github.com/bloomberg/python-github-webhook) - A framework for writing webhooks for GitHub, in Python.
- [Psycopg2](https://github.com/psycopg/psycopg2) - PostgreSQL database adapter for the Python programming language.
- [PostgreSQL](https://www.postgresql.org/download/) - The world's most advanced open source database.
- [NodeJS](https://nodejs.org/) - a JavaScript runtime built on Chrome's V8 JavaScript engine.
- [Redis](https://github.com/antirez/redis) - a in-memory database that persists on disk.
- [Celery](https://github.com/celery/celery) - a asynchronous task queue/job queue based on distributed message passing.

Linux 用户可以直接运行 setup.sh 脚本安装这些依赖：

    sh ./setup.sh

### 配置

config 目录下存放着配置文件，其中以下文件需要你按照实际情况来配置：

- site.py - 整个网站的相关信息
- github.py - GitHub 应用信息配置
- database.py - 数据库配置

具体示例可参考与它们名称对应的 .example 文件，建议直接复制它们并去掉 .example 后缀名。

### 数据库

创建数据库迁移文件，然后升级数据库：

    python manage.py db migrate
    python manage.py db upgrade

## 资源

安装 NodeJS 依赖包：

    npm install

构建 CSS、JavaScript 等相关资源文件：

    npm run build

## 启动

先确保 PostgreSQL 和 Redis 服务器已经启动，然后使用以下命令运行网站主程序：

    python main.py

启动任务队列：

    celery worker -A app.worker -l info
    celery beat -A app.worker
