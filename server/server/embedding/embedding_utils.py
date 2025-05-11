# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 20:44
# @Author : 寻梦
# @File : embedding_utils
# @Project : langchain-ChatBA

from langchain.docstore.document import Document
from typing import List,Dict
from server.controller.utils import BaseResponse
from configs import logger,ONLINE_EMBED_MODEL,EMBEDDING_MODEL
from server.utils import list_local_embed_models,list_online_embed_models


def get_embeddings_online(model:str=EMBEDDING_MODEL):
    kwargs=ONLINE_EMBED_MODEL.get(model)
    if model.startswith("bge-"):
        from langchain_community.embeddings import QianfanEmbeddingsEndpoint
        embedding=QianfanEmbeddingsEndpoint(**kwargs)
    return embedding

def embed_texts(
        texts: List[str],
        embed_model: str = EMBEDDING_MODEL,
        to_query: bool = False,
) -> BaseResponse:
    '''
    对文本进行向量化。返回数据格式：BaseResponse(data=List[List[float]])
    '''
    try:

        if embed_model in list_online_embed_models():
            embeddings=get_embeddings_online(model=embed_model)
            if embeddings is not None:
                return BaseResponse(data=embeddings.embed_documents(texts))

        elif embed_model in list_local_embed_models():  # 使用本地Embeddings模型
            from server.utils import load_local_embeddings

            embeddings = load_local_embeddings(model=embed_model)
            return BaseResponse(data=embeddings.embed_documents(texts))
        else:
            return BaseResponse(code=500, msg=f"指定的模型 {embed_model} 不支持 Embeddings 功能。")
    except Exception as e:
        logger.error(e)
        return BaseResponse(code=500, msg=f"文本向量化过程中出现错误：{e}")


def embed_documents(
        docs: List[Document],
        embed_model: str = EMBEDDING_MODEL,
        to_query: bool = False,
) -> Dict:
    """
    将 List[Document] 向量化，转化为 VectorStore.add_embeddings 可以接受的参数
    """
    texts = [x.page_content for x in docs]
    metadatas = [x.metadata for x in docs]
    embeddings = embed_texts(texts=texts, embed_model=embed_model, to_query=to_query).data
    if embeddings is not None:
        return {
            "texts": texts,
            "embeddings": embeddings,
            "metadatas": metadatas,
        }



