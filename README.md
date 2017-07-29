# GitDigger

## 快速开始

### 安装依赖

GitDigger 依赖于以下软件：

- [Flask](https://github.com/pallets/flask) - a microframework for Python
- [Flask-Script](https://github.com/smurfix/flask-script) - Flask extension to help writing external scripts for Flask applications.
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) - Adds SQLAlchemy support to Flask
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) - SQLAlchemy database migrations for Flask applications using Alembic
- [Flask-Login](https://github.com/maxcountryman/flask-login) - Flask user session management. 
- [Flask-WTF](https://github.com/lepture/flask-wtf) - Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration.
- [GitHub-Flask](https://github.com/cenkalti/github-flask) - Flask extension for authenticating users with GitHub and making requests to the API. 
- [Psycopg2](https://github.com/psycopg/psycopg2) - PostgreSQL database adapter for the Python programming language
- [PostgreSQL](https://www.postgresql.org/download/) - The world's most advanced open source database

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


## 最后

直接使用以下命令运行程序：

    python main.py
