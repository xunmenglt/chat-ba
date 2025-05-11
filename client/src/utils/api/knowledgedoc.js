import { getRequest,postRequest,uploadFile } from "@/plugins/axios";

// 获取文档列表
export const getKnowledgeFileListApi=(param)=>{
    return getRequest('/api/konwledge_base/konwledge_factory/file_list',null,param)
}

// 根据id获取文件
export const getKnowledgeFileByIDApi=(param)=>{
    return getRequest('/api/konwledge_base/konwledge_factory/file_list',null,param)
}

// 删除文件
export const deleteKnowledgeFileApi=(data)=>{
    return postRequest('/api/konwledge_base/konwledge_doc/delete_konwledge_file',data,null)
}

export const uploadKnowledgeFileApi=(data)=>{
    const formData = new FormData();
    data.files.forEach(file => {
        formData.append("files",file)
    });
    formData.append("chunk_size",data.chunk_size)
    formData.append("chunk_overlap",data.chunk_overlap)
    formData.append("is_vector_store",data.is_vector_store)
    formData.append("override",data.override)
    formData.append("factory_name",data.factory_name)
    return uploadFile('/api/konwledge_base/konwledge_doc/upload_docs',formData)
}