# -*- coding:UTF-8 -*-
# @Time : 2024/3/8 15:27
# @Author : 寻梦
# @File : qdrant_kb_service
# @Project : langchain-ChatBA

import uuid
from typing import List, Dict
from langchain_core.documents import Document
from langchain.vectorstores.qdrant import Qdrant
from server.knowledge_file_utils.konwledgefile import KnowLedgeFile
from server.services.knowledge_base.base import KBService,SupportedVSType
from server.services.knowledge_base.base import EmbeddingsFunAdapter
import qdrant_client
from qdrant_client.http.models import VectorParams,Distance
from configs import kbs_config

class Qdrant_KBService(KBService):

    qdrant:Qdrant


    def vs_type(self)->str:
        return SupportedVSType.QDRANT

    def do_init(self):
        self._load_qdrant()

    def _load_qdrant(self):
        qdrant_args = kbs_config.get("qdrant")
        self.qdrant = Qdrant(embeddings=EmbeddingsFunAdapter(self.embed_model),
                             collection_name=self.kb_name, client=qdrant_client.QdrantClient(**qdrant_args))

    def do_create_kb(self):
        try:
            self.qdrant.client.create_collection(collection_name=self.kb_name,
                                                 vectors_config=VectorParams(size=1024, distance=Distance.COSINE))
            return True
        except Exception as e:
            return False

    def do_drop_kb(self):
        status=self.qdrant.client.delete_collection(collection_name=self.kb_name)
        return status

    def do_delete_doc(self, kb_file: KnowLedgeFile,**kwargs):
        doc_infos=self.get_ids_arr(kb_file)
        ids=[doc_info["id"] for doc_info in doc_infos]
        if ids is not None and len(ids)>0:
            self.qdrant.delete(ids)
        return True

    def do_add_doc(self, docs: List[Document],**kwargs) -> List[Dict]:
        doc_infos = []
        metadatas=[doc.metadata for doc in docs]
        ids=self.qdrant.add_documents(docs)
        # data = self._docs_to_embeddings(docs)
        # ids = [str(uuid.uuid1()) for _ in range(len(data["texts"]))]
        #
        # for _id, text, embedding, metadata in zip(ids, data["texts"], data["embeddings"], data["metadatas"]):
        #     self.qdrant.client.add(ids=_id, embeddings=embedding, metadatas=metadata, documents=text,collection_name=self.kb_name)
        #     doc_infos.append({"id": _id, "metadata": metadata})
        for _id,metadata in zip(ids,metadatas):
            doc_infos.append({"id": _id, "metadata": metadata})
        return doc_infos

    def do_search(self, query: str, top_k: int, score_threshold: float) -> List[Document]:
        return self.qdrant.similarity_search(query=query,k=top_k,score_threshold=score_threshold)

