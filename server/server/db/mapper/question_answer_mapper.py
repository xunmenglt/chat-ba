# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 14:34
# @Author : 寻梦
# @File : knowledge_file_mapper
# @Project : langchain-ChatBA


from server.db.models.question_answer_model import QuestionAnswerModel
from server.db.session import with_session
from sqlalchemy.orm import Session
from typing import Dict,List


@with_session
def list_from_db(session,
                    file_path:str='',
                    sort:int=-1,
                    query:str=None):
    '''
        根据条件查询结果
    '''
    qas=[]
    if not file_path:
        return qas
    if sort>=0:
        qas=session.query(QuestionAnswerModel).filter(QuestionAnswerModel.file_path.ilike(file_path),
                                                              QuestionAnswerModel.sort==sort)
    elif query:
        qas=session.query(QuestionAnswerModel).filter(QuestionAnswerModel.file_path.ilike(file_path),
                                                      QuestionAnswerModel.question.like("%"+query+"%")).order_by(QuestionAnswerModel.sort.asc())
    else:
        qas=session.query(QuestionAnswerModel).filter(QuestionAnswerModel.file_path.ilike(file_path)).order_by(QuestionAnswerModel.sort.asc())
    return [{"id": qa.id, 
             "file_path": qa.file_path,
             "sort":qa.sort,
             "question":qa.question,
             "answer":qa.answer} for qa in qas]

@with_session
def delete_from_db(session,
                    file_path:str=''):
    if file_path:
        qas=session.query(QuestionAnswerModel).filter(QuestionAnswerModel.file_path.ilike(file_path))
        if qas:
            for qa in qas:
                session.delete(qa)

@with_session
def add_qa_to_db(session,
                   file_path: str,
                   question: str = '',
                   answer: str = '',
                   sort: int = -1,
                   ):
    new_qa=QuestionAnswerModel(
            file_path=file_path,
            question=question,
            answer=answer,
            sort=sort
    )
    session.add(new_qa)
    return True