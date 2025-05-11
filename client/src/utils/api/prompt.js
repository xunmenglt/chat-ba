import { getRequest } from "@/plugins/axios";

// 获取模板名称列表
export const getPromptList=(params)=>{
    return getRequest('/api/comment/prompt/list',null,params)
}
// 获取模板信息
export const getPromptInfo=(params)=>{
    return getRequest('/api/comment/prompt/info',null,params)
}