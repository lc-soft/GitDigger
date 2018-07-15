# GitDigger

## 简述

一个为开源项目而生的社区，用于帮助开发者发现感兴趣的开源项目以及相关的新鲜事，让他们能够方便的了解到各个开源项目都有哪些需要解决的问题、有哪些问题是自己能够提供帮助的，以此为开源项目吸引更多的贡献者。

目前还处于开发阶段，很多功能未完成，如果你是经验丰富的 Python 开发者，可以向此项目提供技术支持，包括但不仅限于：数据库表结构设计、性能优化、代码规范、模块规划、国际化。

## 需求及目标

作为普通开发者，平常无聊的时候会想看看其他人在干什么，长长见识，比如写了什么代码、都在讨论什么问题（Issue）、有哪些有意思的问题和问题评论、哪些项目发布了新版本等等。对于在某些领域有丰富经验的人，可能还会想知道哪些项目正遇到自己擅长领域的问题，看看自己能不能帮上忙。像 GitHub 等代码托管平台主要专注于源代码托管，用户的认知范围都仅限于自己的项目，没有提供多少途径让用户去发现其他开发者和开源项目的动态。

作为开源项目作者或维护者，一个人的时间和精力都是有限的，有时会被一些琐碎的问题浪费很多时间，例如：各种小 bug，添加各种小功能。同类型的问题处理多了会很感到枯燥，但又不得不去做，做多了又会耽误主线任务开发进度，还会浪费动力。当遇到一些大点问题时，会希望有人能给予技术支持，例如：

- 这块代码是否有更好的实现
- 要实现这种功能，有哪些可参考的资料
- 如何调整数据结构和算法以提升性能
- 如何更好的重构代码
- 如何正确命名标识符
- 如何设计目录结构
- 如何让代码更简单易读
- 有哪些需要注意的坑
- 怎样写好 README.md

自己搜索相关资料比较费时，可能会找不到答案，而去某些问答网站提问的话，需要写详尽的描述，还可能需要提供最小示例，比较麻烦也费时间，还很有可能得不到答案。这只是开发方面，对于普通开发者，不管项目的代码更新得有多频繁，也不会有人知道这个项目，除非主动去推广，通常的推广手段是在各大平台发布版本更新资讯，但持续时间有限，过了一两周又会回到无人问津的状态。

要解决上述问题，需要有个平台能够：

- 挖掘开源项目的各种信息，包括：问题（Issues）、拉取请求（Pull Requests）、评论、发行版新闻（Releases），供用户浏览。
- 展示开源项目及相关的动态，让用户能够方便的找到近期活跃的项目，也能够从最近动态中了解到大家都在干什么。
- 支持让开源项目作者将一些问题（Issue）标记为“需要帮助”来获得更多的曝光，吸引更多有经验的人来向作者提供帮助。

## 技术栈

- 服务端
  - 服务器：[Nginx](http://nginx.org/)
  - 编程语言：[Python](https://www.python.org/)
  - Web 框架：[Flask](http://flask.pocoo.org/)
  - 数据库：[PostgreSQL](https://www.postgresql.org/)、[Redis](https://redis.io/)
  - 任务队列：[Celery](http://www.celeryproject.org/)
- 前端
  - 库：[jQuery](http://jquery.com/)
  - UI 组件库：[Bootstrap](http://getbootstrap.com/)
  - CSS 预编译器：[Sass](http://sass-lang.com/)
  - 构建工具：[Webpack](http://webpack.github.io/)
  - 特性：响应式布局

为减少项目的开发时间和复杂度，网站页面以服务端渲染为主，即便作者是个 Web 前端程序员也不打算浪费时间去折腾前后端分离、单页应用等技术，除非有人能长期负责全职开发此项目的后端。

## 相关网站

- [CodeTriage](https://www.codetriage.com/) - Free community tools for contributing to Open Source projects

## 安装与配置

### 依赖

GitDigger 依赖于以下软件：

- [Flask](https://github.com/pallets/flask) - a microframework for Python.
- [Flask-Script](https://github.com/smurfix/flask-script) - Flask extension to help writing external scripts for Flask applications.
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) - Adds SQLAlchemy support to Flask.
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) - SQLAlchemy database migrations for Flask applications using Alembic
- [Flask-Login](https://github.com/maxcountryman/flask-login) - Flask user session management. 
- [Flask-Paginate](https://github.com/lixxu/flask-paginate) - Pagination support for flask. 
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

- github.py - GitHub 应用信息配置
- database.py - 数据库配置

具体示例可参考与它们名称对应的 .example 文件，建议直接复制它们并去掉 .example 后缀名。

### 服务器

如需将此网站部署到线上生产环境中，则需要以下步骤。

修改 `config/nginx/sites-avaliable/gitdigger.com.conf` 文件，将里面的路径改成你的实际路径。之后，复制 `config/nginx` 目录到 nginx 的配置目录：

    cp -r config/nginx/* /etc/nginx

为配置文件建立软连接，以启用该配置文件：

    ln -s /etc/nginx/sites-available/gitdigger.com.conf /etc/nginx/sites-enabled/gitdigger.com.conf

修改 `config/uwsgi.ini`，将里面的路径改成你的实际路径。之后启动 uwsgi 服务：

    uwsgi --ini config/uwsgi.ini

### 数据库

以 PostgreSQL 为例，先创建 gitdigger 用户：

    sudo -u postgres createuser gitdigger -P

之后为 gitdigger 用户创建 gitdigger_development 数据库：

    sudo -u postgres createdb -O gitdigger gitdigger_development

创建数据库迁移文件，然后升级数据库：

    pipenv run python manage.py db migrate
    pipenv run python manage.py db upgrade

### 任务队列

    celery worker -A app.worker -l info
    celery beat -A app.worker

## 资源

安装 NodeJS 依赖包：

    npm install

构建 CSS、JavaScript 等相关资源文件：

    npm run build

## 启动

先确保 PostgreSQL 和 Redis 服务器已经启动，然后使用以下命令运行网站主程序：

    pipenv run python main.py
