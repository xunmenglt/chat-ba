# -*- coding:UTF-8 -*-
# @Time : 2024/3/6 16:08
# @Author : 寻梦
# @File : knowledge_factory_mapper
# @Project : langchain-ChatBA
from server.db.models.knowledge_base_model import KnowledgeBaseModel
from server.db.models.knowledge_file_model import KnowledgeFileModel,FileDocModel
from server.db.session import with_session

# 更具知识库名字获取知识库在数据库中的信息
@with_session
def get_kb_from_db(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        kb_name, vs_type, embed_model = kb.kb_name, kb.vs_type, kb.embed_model
    else:
        kb_name, vs_type, embed_model = None, None, None
    return kb_name, vs_type, embed_model


# 添加知识库到数据库中
@with_session
def add_kb_to_db(session, kb_name, kb_info, vs_type, embed_model):
    # 创建知识库实例
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if not kb:
        kb = KnowledgeBaseModel(kb_name=kb_name, kb_info=kb_info, vs_type=vs_type, embed_model=embed_model)
        session.add(kb)
    else:  # update kb with new vs_type and embed_model
        kb.kb_info = kb_info
        kb.vs_type = vs_type
        kb.embed_model = embed_model
    return True


@with_session
def delete_kb_from_db(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        # 删除对应的docs
        docs=session.query(FileDocModel).filter(FileDocModel.kb_name.ilike(kb_name))
        if docs:
            for doc in docs:
                session.delete(doc)
        files=session.query(KnowledgeFileModel).filter(KnowledgeFileModel.kb_name.ilike(kb_name))

        if files:
            for file in files:
                session.delete(file)
        session.delete(kb)
    return True


@with_session
def load_kb_from_db(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        kb_name, vs_type, embed_model = kb.kb_name, kb.vs_type, kb.embed_model
    else:
        kb_name, vs_type, embed_model = None, None, None
    return kb_name, vs_type, embed_model


@with_session
def get_list_kb_from_db(session, min_file_count: int = -1):
    kbs = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.file_count > min_file_count).order_by(KnowledgeBaseModel.create_time.desc()).all()
    kbs=[{"id":kb.id,"kb_name":kb.kb_name,"embed_model":kb.embed_model,"vs_type":kb.vs_type,"file_count":kb.file_count,"kb_info":kb.kb_info,"createTime":kb.create_time} for kb in kbs]
    return kbs




@with_session
def get_kb_detail(session, kb_name: str) -> dict:
    kb: KnowledgeBaseModel = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        return {
            "kb_name": kb.kb_name,
            "kb_info": kb.kb_info,
            "vs_type": kb.vs_type,
            "embed_model": kb.embed_model,
            "file_count": kb.file_count,
            "create_time": kb.create_time,
        }
    else:
        return {}