# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 12:06
# @Author : 寻梦
# @File : init_database_script
# @Project : langchain-ChatBA

from .base import Base,engine
from .models import *
from configs import logger

def create_tables():
    logger.info("开始初始化sqlite数据库...")
    Base.metadata.create_all(bind=engine)
    logger.info("系统数据创建完成!")
def reset_tables():
    Base.metadata.drop_all(bind=engine)


