# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 14:34
# @Author : 寻梦
# @File : knowledge_file_mapper
# @Project : langchain-ChatBA


from server.db.models.knowledge_base_model import KnowledgeBaseModel
from server.db.session import with_session
from server.db.models import KnowledgeFileModel,FileDocModel
from server.knowledge_file_utils.konwledgefile import KnowLedgeFile
from sqlalchemy.orm import Session
from typing import Dict,List
from server.utils import get_file_path
from server.db.mapper import question_answer_mapper

@with_session
def list_docs_from_db(session,
                      kb_name: str,
                      file_name: str = None,
                      metadata: Dict = {},
                      ) -> List[Dict]:
    '''
    列出某知识库某文件对应的所有Document。
    返回形式：[{"id": str, "metadata": dict}, ...]
    '''
    docs = session.query(FileDocModel).filter(FileDocModel.kb_name.ilike(kb_name))
    if file_name:
        docs = docs.filter(FileDocModel.file_name.ilike(file_name))
    for k, v in metadata.items():
        docs = docs.filter(FileDocModel.meta_data[k].as_string() == str(v))

    return [{"id": x.doc_id, "metadata": x.metadata} for x in docs.all()]


@with_session
def select_file_by_id(session,file_id):
    file: KnowledgeFileModel = (session.query(KnowledgeFileModel)
                                .filter(KnowledgeFileModel.id==file_id)
                                .first())
    if file:
        return {
            "id":file.id,
            "kb_name": file.kb_name,
            "file_name": file.file_name,
            "file_ext": file.file_ext,
            "document_loader": file.document_loader_name,
            "text_splitter": file.text_splitter_name,
            "create_time": file.create_time,
            "file_size": file.file_size,
            "docs_count": file.docs_count,
        }
    else:
        return {}


@with_session
def delete_docs_from_db(session,
                        kb_name: str,
                        file_name: str = None,
                        ) -> List[Dict]:
    '''
    删除某知识库某文件对应的所有Document，并返回被删除的Document。
    返回形式：[{"id": str, "metadata": dict}, ...]
    '''
    docs = list_docs_from_db(kb_name=kb_name, file_name=file_name)
    query = session.query(FileDocModel).filter(FileDocModel.kb_name.ilike(kb_name))
    if file_name:
        query = query.filter(FileDocModel.file_name.ilike(file_name))
    query.delete(synchronize_session=False)
    session.commit()
    return docs


@with_session
def add_docs_to_db(session,
                   kb_name: str,
                   file_name: str,
                   doc_infos: List[Dict]):
    '''
    将某知识库某文件对应的所有Document信息添加到数据库。
    doc_infos形式：[{"id": str, "metadata": dict}, ...]
    '''
    # ! 这里会出现doc_infos为None的情况，需要进一步排查
    if doc_infos is None:
        print("输入的doc_infos参数为None")
        return False
    for d in doc_infos:
        obj = FileDocModel(
            kb_name=kb_name,
            file_name=file_name,
            doc_id=d["id"],
            meta_data=d["metadata"],
        )
        session.add(obj)
    return True

"""
=============================================
"""


@with_session
def get_file_detail(session, kb_name: str, filename: str) -> dict:
    file: KnowledgeFileModel = (session.query(KnowledgeFileModel)
                                .filter(KnowledgeFileModel.file_name.ilike(filename),
                                        KnowledgeFileModel.kb_name.ilike(kb_name))
                                .first())
    if file:
        return {
            "id":file.id,
            "kb_name": file.kb_name,
            "file_name": file.file_name,
            "file_ext": file.file_ext,
            "document_loader": file.document_loader_name,
            "text_splitter": file.text_splitter_name,
            "create_time": file.create_time,
            "file_size": file.file_size,
            "docs_count": file.docs_count,
        }
    else:
        return {}


# 根据知识库名获取文件列表
@with_session
def get_file_list_in_db(session:Session,kb_name:str)->List[Dict]:
    files:List[KnowledgeFileModel]=(session.query(KnowledgeFileModel)
           .filter(KnowledgeFileModel.kb_name.ilike(kb_name))
           .order_by(KnowledgeFileModel.create_time)).all()
    return [{"id":file.id,
             "file_name":file.file_name,
             "file_ext":file.file_ext,
             "kb_name":file.kb_name,
             "document_loader_name":file.document_loader_name,
             "text_splitter_name":file.text_splitter_name,
             "file_size":file.file_size,
             "docs_count":file.docs_count,
             "create_time":file.create_time} for file in files]


"""
======================================================
"""

@with_session
def delete_files_from_db(session, knowledge_base_name: str):
    session.query(KnowledgeFileModel).filter(KnowledgeFileModel.kb_name.ilike(knowledge_base_name)).delete(
        synchronize_session=False)
    session.query(FileDocModel).filter(FileDocModel.kb_name.ilike(knowledge_base_name)).delete(
        synchronize_session=False)
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(knowledge_base_name)).first()
    if kb:
        kb.file_count = 0

    session.commit()
    return True




@with_session
def delete_file_from_db(session:Session,kb_file:KnowLedgeFile):
    existing_file=(
        session.query(KnowledgeFileModel)
        .filter(
            KnowledgeFileModel.kb_name.ilike(kb_file.factory_name),
            KnowledgeFileModel.file_name.ilike(kb_file.filename))
        .first()
    )
    if existing_file:
        session.delete(existing_file)
        delete_docs_from_db(kb_name=kb_file.factory_name, file_name=kb_file.filename)
        session.commit()
        kb=session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_file.factory_name)).first()
        if kb:
            kb.file_count-=1
            # 判断该文件是否时jsonl文件
            if(kb_file.ext and kb_file.ext.__contains__("json")):
                question_answer_mapper.delete_from_db(get_file_path(kb_file.factory_name,kb_file.filename))
            session.commit()
    return True


"""
=================================================
"""
@with_session
def add_file_to_db(session,
                   kb_file: KnowLedgeFile,
                   docs_count: int = 0,
                   custom_docs: bool = False,
                   doc_infos: List[Dict] = [],  # 形式：[{"id": str, "metadata": dict}, ...]
                   ):
    kb = session.query(KnowledgeBaseModel).filter_by(kb_name=kb_file.factory_name).first()
    if kb:
        # 如果已经存在该文件，则更新文件信息与版本号
        existing_file: KnowledgeFileModel = (session.query(KnowledgeFileModel)
                                             .filter(KnowledgeFileModel.kb_name.ilike(kb_file.factory_name),
                                                     KnowledgeFileModel.file_name.ilike(kb_file.filename))
                                             .first())
        size = kb_file.get_size()

        if existing_file:
            existing_file.file_size = size
            existing_file.docs_count = docs_count
            existing_file.custom_docs = custom_docs
        # 否则，添加新文件
        else:
            new_file = KnowledgeFileModel(
                file_name=kb_file.filename,
                file_ext=kb_file.ext,
                kb_name=kb_file.factory_name,
                document_loader_name=kb_file.document_loader_name,
                text_splitter_name=kb_file.text_splitter_name or "SpacyTextSplitter",
                file_size=size,
                docs_count=docs_count
            )
            kb.file_count += 1
            session.add(new_file)
        add_docs_to_db(kb_name=kb_file.factory_name, file_name=kb_file.filename, doc_infos=doc_infos)
    return True