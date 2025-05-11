// 获取知识库列表
import { getRequest,postRequest } from "@/plugins/axios";
// 第一个参数是data 第二个是param
export const getKnowledgeBaseListApi=()=>{
    return getRequest('/api/konwledge_base/konwledge_factory/list')
}

// 获取向量数据库模型列表
export const getVectorStoreListApi=()=>{
    return getRequest('/api/konwledge_base/vector_store/list')
}


// 获取向量嵌入模型列表
export const getEmbeddingModelListApi=()=>{
    return getRequest('/api/konwledge_base/konwledge_factory/embedding_list')
}


export const createKnowledgeBaseApi=(data)=>{
    return postRequest('/api/konwledge_base/konwledge_factory/create',data,null)
}

export const deleteKnowledgeBaseApi=(kb_name)=>{
    return postRequest(`/api/konwledge_base/konwledge_factory/delete/${kb_name}`,null,null)
}