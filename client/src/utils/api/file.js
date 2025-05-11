import { getRequest,postRequest,uploadFile ,getBaseUrl} from "@/plugins/axios";

// 根据id获取文件
export const getFileSrc=(fileId)=>{
    return `${getBaseUrl()}/api/comment/file/view/${fileId}`
}

// 条件查询QA问答对数据
export const getQAList=(params)=>{
    return getRequest(
        "/api/comment/file/qa/list",
        null,
        params
    )
}