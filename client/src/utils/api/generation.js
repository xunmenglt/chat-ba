import { getRequest,postRequest,uploadFile ,getBaseUrl} from "@/plugins/axios";
export const uploadKnowledgeFileApi=(data)=>{
    if(data){
        const formData = new FormData();
        data.files.forEach(file => {
            formData.append("files",file)
        });
        return uploadFile('/api/chat/generation/uploadfile',formData)
    }else{
        return null
    }
    
}

export const getEvalQAScore=(qa_box_id,file_id)=>{
    if (qa_box_id){
        return getRequest(`/api/chat/generation/qa_score/${qa_box_id}/${file_id}`)
    }
}

export const downLoadQAFileAPI=async (data)=>{
    const result = await postRequest('/api/chat/generation/downloadqa',data);
    const blob = new Blob([result], { type: result.type });
    const downloadElement = document.createElement("a");
    const href = window.URL.createObjectURL(blob);
    downloadElement.href = href;
    downloadElement.download = `${data.file_name}-${data.qa_box_id}-${data.file_id}.csv`;//给下载文件命名，避免重复
    document.body.appendChild(downloadElement);
    downloadElement.click();
    document.body.removeChild(downloadElement); //移除元素；防止连续点击创建多个a标签
    window.URL.revokeObjectURL(href);
}