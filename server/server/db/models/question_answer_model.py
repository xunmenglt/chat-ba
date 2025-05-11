# -*- coding:UTF-8 -*-
# @File : question_answer_model
# @Project : langchain-ChatBA
from sqlalchemy import Column, Integer, String, DateTime, JSON, func,Text

from server.db.base import Base


class QuestionAnswerModel(Base):
    """
    问答对存储表格
    """
    __tablename__ = 'question_answer'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    file_path = Column(String(255), comment='文件地址')
    sort = Column(Integer, comment='序号')
    question = Column(Text, comment='问题')
    answer = Column(Text, comment='答案')

    def __repr__(self):
        return f"<QuestionAnswerModel(id='{self.id}', file_path='{self.file_path}', sort='{self.sort}', question='{self.question}',answer='{self.answer}')>"