## 项目简介

本项目是一个企业级后端接口，基于 FastAPI 框架开发。项目功能包括用户注册、用户认证、权限控制、以及从数据库读取和写入数据。有以下几个需求：

1. 把接口api作为Service分离开 
2. 接口功能是从数据库中读取一张表tbl_example的内容 
3. 将数据库连接等配置信息独立出来 
4. 使用poetry管理项目的python包 
5. 增加注册服务，使用户能够注册新账户
6. 增加权限认证功能，用户可以通过发送 POST 请求到 /auth/token 路由使用注册的新用户登录，并提供用户名和密码来获取访问令牌。只有通过认证的用户才能访问api 
7. 编写一些单元测试用例



## 目录结构
首先定义项目的目录结构：

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── base.py
│   │   └── database.py
│   ├── init_db.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── example.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── user.py
│   │   └── example.py
│   │   └── query.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── example.py
│   │   ├── nlp.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── query_tool.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── api_v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── user.py
│   │   │   │   └── example.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_example.py
│   └── test_user.py
├── .env
├── pyproject.toml
└── README.md
```

## 安装步骤

### 1. 克隆项目仓库

``` bash
git clone https://github.com/your_username/your_project.git
cd your_project
```

### 2. 使用 Poetry 安装依赖

确保已安装 Poetry，然后运行：

``` bash
poetry install
```

### 3. 配置环境变量

在 `app/core/config.py` 中设置必要的配置项：

``` python
class Settings:
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
```

### 4. 初始化数据库

创建 SQLite 数据库并生成数据表：

``` bash
poetry run python -m app.db.base
```

### 5. 运行项目

使用 Uvicorn 启动项目：

``` bash
poetry run uvicorn app.main:app --reload
```

## 测试用例

- 测试注册用户 (test_register)： 确保用户可以成功注册。
- 测试用户登录 (test_login)： 确保用户可以成功登录并获得访问令牌。
- 未授权访问测试 (test_read_example_unauthorized)： 确保在没有提供令牌的情况下，访问受保护的路由会返回401状态码。
- 创建示例测试 (test_create_example)： 使用有效令牌测试创建一个新示例。
- 读取示例测试 (test_read_example)： 使用有效令牌测试读取已创建的示例。