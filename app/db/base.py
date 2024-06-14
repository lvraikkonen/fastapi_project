from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 导入所有的模型，以确保他们能够被正确地注册
from app.models import models
