import operator
from abc import ABC, abstractmethod

import os
from pathlib import Path
import numpy as np
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document
from server.db.mapper.knowledge_file_mapper import delete_files_from_db,list_docs_from_db
from typing import List,Dict,Union

from server.db.mapper.knowledge_factory_mapper import (
    add_kb_to_db,delete_kb_from_db,load_kb_from_db
)

from server.db.mapper.knowledge_file_mapper import (delete_file_from_db,add_file_to_db)

from server.utils import (
    get_kb_path, get_doc_path
)
from configs import (kbs_config, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD,
                     EMBEDDING_MODEL, KB_INFO)

from server.embedding.embedding_utils import embed_documents
from server.knowledge_file_utils.konwledgefile import KnowLedgeFile
from server.embedding.embedding_utils import embed_texts



def normalize(embeddings: List[List[float]]) -> np.ndarray:
    '''
    sklearn.preprocessing.normalize 的替代（使用 L2），避免安装 scipy, scikit-learn
    '''
    norm = np.linalg.norm(embeddings, axis=1)
    norm = np.reshape(norm, (norm.shape[0], 1))
    norm = np.tile(norm, (1, len(embeddings[0])))
    return np.divide(embeddings, norm)



class SupportedVSType:
    QDRANT="qdrant"


"""
知识库里面包含：
    知识库名
    知识库文件存储地址
    知识库对应的embedding工具
    知识库对应的向量库
"""
class KBService(ABC):
    """
    knowledge_factory_name: 知识库名称
    embed_model：嵌入向量类型
    """
    def __init__(self,
                 knowledge_factory_name: str,
                 embed_model: str = EMBEDDING_MODEL,
                 ):
        self.kb_name = knowledge_factory_name # 知识库名字
        self.kb_info = KB_INFO.get(knowledge_factory_name, f"关于{knowledge_factory_name}的知识库") # 知识库描述信息
        self.embed_model = embed_model # 嵌入向量模型名称
        self.kb_path = get_kb_path(self.kb_name) # 知识库路径
        self.doc_path = get_doc_path(self.kb_name) # 知识库文件存放路径
        self.do_init()

    def __repr__(self) -> str:
        return f"{self.kb_name} @ {self.embed_model}"


    # 保存向量库
    def save_vector_store(self):
        '''
        保存向量库:FAISS保存到磁盘，milvus保存到数据库。PGVector暂未支持
        '''
        pass

    @abstractmethod
    def do_create_kb(self):
        """
        创建知识库子类实自己逻辑
        """
        pass


    @abstractmethod
    def do_delete_doc(self,
                      kb_file: KnowLedgeFile):
        """
        从知识库删除文档子类实自己逻辑
        """
        pass

    @abstractmethod
    def do_add_doc(self,
                   docs: List[Document],
                   **kwargs,
                   ) -> List[Dict]:
        """
        向知识库添加文档子类实自己逻辑
        """
        pass
    @abstractmethod
    def do_drop_kb(self):
        """
        删除知识库自身
        """
        pass

    @abstractmethod
    def do_search(self,
                  query: str,
                  top_k: int,
                  score_threshold: float,
                  ) -> List[Document]:
        """
        搜索知识库子类实自己逻辑
        """
        pass


    # 添加知识库到数据库中
    def create_kb(self):
        """
        创建知识库
        """
        if not os.path.exists(self.doc_path):
            os.makedirs(self.doc_path)
        if not self.do_create_kb(): # 用于向量数据库去创建知识库
            return 0
        status = add_kb_to_db(self.kb_name, self.kb_info, self.vs_type(), self.embed_model)
        return status


    def get_ids_arr(self,file:KnowLedgeFile):
        return list_docs_from_db(kb_name=file.factory_name,file_name=file.filename)

    def _docs_to_embeddings(self,docs:List[Document])->Dict:
        '''
        将 List[Document] 转换成 VectorStore.add_embeddings 可接受的参数
        '''
        return embed_documents(docs=docs, embed_model=self.embed_model, to_query=False)

    def add_doc(self,kb_file:KnowLedgeFile,**kwargs):
        """
        向知识库中添加文件
        """
        docs=kb_file.file2text()
        if docs:
            for doc in docs:
                try:
                    source = doc.metadata.get("source", "")
                    if os.path.isabs(source):
                        rel_path = Path(source).relative_to(self.doc_path);
                        doc.metadata["source"]=str(rel_path.as_posix().strip("/"))
                        doc.metadata["factory_name"]=self.kb_name
                        doc.metadata["file_name"]=kb_file.filename
                        doc.metadata["file_ext"]=kb_file.ext
                except Exception as e:
                    print(f"cannot convert absolute path ({source}) to relative path. error is : {e}")
            # 删除原来的文档
            self.delete_doc(kb_file)

            #  todo 继承 添加文档
            doc_infos = self.do_add_doc(docs=docs, kwargs=kwargs)

            # 添加文件信息到知识库中
            status = add_file_to_db(kb_file,
                                    docs_count=len(docs),
                                    doc_infos=doc_infos)
        else:
            status=False

        return status



    def delete_doc(self, kb_file: KnowLedgeFile, delete_content: bool = False, **kwargs):
        """
        从知识库删除文件
        """
        # 从向量库中删除文档todo
        self.do_delete_doc(kb_file, **kwargs)
        status = delete_file_from_db(kb_file)
        if delete_content and os.path.exists(kb_file.filepath):
            os.remove(kb_file.filepath)
        return status

    def update_doc(self, kb_file: KnowLedgeFile, docs: List[Document] = [], **kwargs):
        """
        使用content中的文件更新向量库
        如果指定了docs，则使用自定义docs，并将数据库对应条目标为custom_docs=True
        """
        if os.path.exists(kb_file.filepath):
            self.delete_doc(kb_file, **kwargs)
            return self.add_doc(kb_file, docs=docs, **kwargs)


    def delete_kb(self):
        """
       删除知识库
        """
        status=self.do_drop_kb()
        if not status:
            return status
        status = delete_kb_from_db(self.kb_name)
        return status

    def search_docs(self,
                    query: str,
                    top_k: int = VECTOR_SEARCH_TOP_K,
                    score_threshold: float = SCORE_THRESHOLD,
                    ) ->List[Document]:
        docs = self.do_search(query, top_k, score_threshold)
        if docs is None:
            return docs
        return docs


class KBServiceFactory:


    # 获取知识库服务
    @staticmethod
    def get_service(kb_name: str,
                    vector_store_type: Union[str, SupportedVSType],
                    embed_model: str = EMBEDDING_MODEL,
                    ) -> KBService:
        if isinstance(vector_store_type, str):
            vector_store_type = getattr(SupportedVSType, vector_store_type.upper())
        if SupportedVSType.QDRANT == vector_store_type:
            from server.services.knowledge_base.vector_store.qdrant_kb_service import Qdrant_KBService
            return Qdrant_KBService(kb_name, embed_model=embed_model)

    # 通过知识库名获取知识库仓库
    @staticmethod
    def get_service_by_name(kb_name: str) -> KBService:
        # 从数据库中加载是否包含该知识库
        _, vs_type, embed_model = load_kb_from_db(kb_name)
        if _ is None:  # kb not in db, just return None
            return None
        return KBServiceFactory.get_service(kb_name, vs_type, embed_model)


    # 获取默认的知识库服务
    @staticmethod
    def get_default():
        return KBServiceFactory.get_service("default", SupportedVSType.DEFAULT)



class EmbeddingsFunAdapter(Embeddings):
    def __init__(self, embed_model: str = EMBEDDING_MODEL):
        self.embed_model = embed_model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = embed_texts(texts=texts, embed_model=self.embed_model, to_query=False).data
        return normalize(embeddings).tolist()

    def embed_query(self, text: str) -> List[float]:
        embeddings = embed_texts(texts=[text], embed_model=self.embed_model, to_query=True).data
        query_embed = embeddings[0]
        query_embed_2d = np.reshape(query_embed, (1, -1))  # 将一维数组转换为二维数组
        normalized_query_embed = normalize(query_embed_2d)
        return normalized_query_embed[0].tolist()  # 将结果转换为一维数组并返回


