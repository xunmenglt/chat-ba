import {readChatbotReply} from '@/plugins/fetchchat'
export const DialogueChat = (data,readCallback,endCallback)=>{
    readChatbotReply('/api/chat/dialogue',data,readCallback,endCallback)
}
export const RetrievalChat = (data,readCallback,endCallback)=>{
    readChatbotReply('/api/chat/retrieval',data,readCallback,endCallback)
}
// qa数据生成
export const QAGeneration = (data,readCallback,endCallback)=>{
    readChatbotReply('/api/chat/generation/qa_generation',data,readCallback,endCallback)
}