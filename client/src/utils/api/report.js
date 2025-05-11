// 获取知识库列表
import { getRequest,postRequest } from "@/plugins/axios";

// 第一个参数是data 第二个是param
export const getIndexList=(page_number=1,page_size=10)=>{
    let params={page_number,page_size}
    return getRequest('/api/report/tables/index',null,params)
}
export const getGsxtInfo=(credit_code)=>{
    let params={credit_code}
    return getRequest('/api/report/tables/gsxt',null,params)
}
export const getKeyPersonsList=(credit_code,page_number=1,page_size=10)=>{
    let params={credit_code,page_number,page_size}
    return getRequest('/api/report/tables/key_persons',null,params)
}
export const getShareholderList=(credit_code,page_number=1,page_size=10)=>{
    let params={credit_code,page_number,page_size}
    return getRequest('/api/report/tables/shareholders',null,params)
}
export const getJudicialCaseList=(credit_code,page_number=1,page_size=10)=>{
    let params={credit_code,page_number,page_size}
    return getRequest('/api/report/tables/judicial_cases',null,params)
}
export const getPatentList=(credit_code,page_number=1,page_size=10)=>{
    let params={credit_code,page_number,page_size}
    return getRequest('/api/report/tables/patents',null,params)
}

// 获取投资行业图表
export const getInvestmentIndustry=(credit_code)=>{
    let params={credit_code}
    return getRequest('/api/report/graphs/investment_industry_graph',null,params)
}
// 获取登记状态图表
export const getRegistrationStatus=(credit_code)=>{
    let params={credit_code}
    return getRequest('/api/report/graphs/registration_status_graph',null,params)
}
// 获取投资地域图表
export const getInvestmentHell=(credit_code)=>{
    let params={credit_code}
    return getRequest('/api/report/graphs/investment_hell_graph',null,params)
}
// 获取投资趋势图表
export const getInvestmentTrend=(credit_code)=>{
    let params={credit_code}
    return getRequest('/api/report/graphs/investment_trend_graph',null,params)
}