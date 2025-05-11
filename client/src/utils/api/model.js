import { getRequest,postRequest,uploadFile } from "@/plugins/axios";

// 获取模型列表
export const getModelList=()=>{
    return getRequest('/api/comment/model/list')
}
