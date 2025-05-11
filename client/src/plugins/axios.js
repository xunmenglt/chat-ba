import axios from "axios";
import router from "@/router";
import {applicationContext} from '@/utils/resources.js'
import { showTextMessage } from "@/plugins/toastification";

//设置基路径
// axios.defaults.baseURL = "http://"+endIp+"/businc/v1/api"
axios.defaults.baseURL = applicationContext.protocol+"://"+applicationContext.host+':'+applicationContext.port+applicationContext.prefix

// 设置请求拦截器，对请求操作进行拦截
axios.interceptors.request.use(config=>{
    //如果存在token，那么请求就携带该token
    const token=window.localStorage.getItem('og_token')
    
    if(token){
        config.headers['Authorization']=token
    }
    
    return config
},
error=>{
    showTextMessage('error','请求拦截未知错误')
})

// 设置响应拦截器，对响应结果进行拦截
axios.interceptors.response.use(
  (success) => {
    return success.data;
  },
  (error) => {
    if (error.response) {
      if (error.response.status == 504 || error.response.status == 404) {
        showTextMessage("error", "服务器被吃了＞︿＜");
      } else if (error.response.status == 403) {
        showTextMessage("error", "权限不足，请联系管理员");
      } else if (error.response.status == 401) {
        showTextMessage("error", error.response.data.message);
        window.localStorage.removeItem("og_token");
        router.replace("/index");
      } else {
        if (error.response.data.message) {
          showTextMessage("error", error.response.data.message);
        } else {
          showTextMessage("error", "未知错误≡(▔﹏▔)≡");
        }
      }
    } else {
      showTextMessage("error", "请稍后重试，服务器更新中");
    }
    return;
  }
);

let base=''

//传送json格式的post请求
export const postRequest=(url,data,params)=>{
    return axios({
        method:'post',
        url:`${base}${url}`,
        data,
        params
    })
}

//传送json格式的get请求
export const getRequest=(url,data,params)=>{
    return axios({
        method:'get',
        url:`${base}${url}`,
        data:data,
        params:params
    })
}


//传送json格式的delete请求
export const deleteRequest=(url,data,params)=>{
    return axios({
        method:'delete',
        url:`${base}${url}`,
        data,
        params
    })
}

//传送json格式的put请求
export const putRequest=(url,params)=>{
    return axios({
        method:'put',
        url:`${base}${url}`,
        data:params
    })
}

export const uploadFile=(url,formData)=>{
    return axios({
      url: `${base}${url}`,
      method: 'post',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' },
    })
}

export const getBaseUrl=()=>{
  return axios.defaults.baseURL
}