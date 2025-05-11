import { getRequest,postRequest,uploadFile } from "@/plugins/axios";

// 创建对话
export const createWin=(data)=>{
    return postRequest('/api/chat/conversation/create',data)
}

// 获取对话列表
export const getWinList=()=>{
    return getRequest('/api/chat/conversation/list')
}

// 删除对话列表
export const deleteWin=(winId)=>{
    return postRequest(`/api/chat/conversation/delete/${winId}`,null,null)
}

// 获取历史对话信息
export const getHistoryMessageList=(winId)=>{
    return getRequest(`/api/chat/conversation/message/history/list/${winId}`,null,null)
}