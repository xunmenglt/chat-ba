import { postRequest } from "@/plugins/axios";
import {readChatbotReply} from '@/plugins/fetchchat'
// pk对话
export const PKChat = (data,readCallback,endCallback,onStart,onError)=>{
    readChatbotReply('/api/chat/pk/dialogue',data,readCallback,endCallback,onStart,onError)
}

// 生成PK信息
export const PkReport = (model_box_list)=>{
    let data={
        "model_box_list":model_box_list,
        "tig":0
    }
    return postRequest('/api/chat/pk/report',data,null)
}