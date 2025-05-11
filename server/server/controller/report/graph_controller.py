import os
from fastapi import APIRouter,Query,Body
from server.controller.report.db.mappers import (
    select_outward_investment_info_by_credit_code
)
from server.controller.utils import BaseResponse
from .llm import model
from .templetes import (
    graph_outward_investment_investment_industry_template,
    graph_outward_investment_registration_status_template,
    graph_outward_investment_investment_hell_template,
    graph_outward_investment_investment_trend_template
)
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain_core.messages.human import HumanMessage
from langchain_core.output_parsers.json import JsonOutputParser

graphs_app=APIRouter(tags=["企业报告图表数据api"],prefix="/graphs")

# 投资行业饼状图echarts信息
@graphs_app.get("/investment_industry_graph",description="投资行业饼状图")
async def get_outward_investment_investment_industry_graph(
    credit_code: str=Query(description="社会统一信用号"),
):
    if not credit_code:
        BaseResponse(code=500,data={},msg="请检查参数")
    
    info=select_outward_investment_info_by_credit_code(credit_code=credit_code)
    context=info["outward_investment_markdown"]
    query=graph_outward_investment_investment_industry_template.replace("{context}",context)
    chain= model | JsonOutputParser()
    data=chain.invoke(input=query)
    return BaseResponse(code=200,data=data,msg="success")


# 登记状态饼状图echarts信息
@graphs_app.get("/registration_status_graph",description="登记状态饼状图")
async def get_outward_investment_registration_status_graph(
    credit_code: str=Query(description="社会统一信用号"),
):
    if not credit_code:
        BaseResponse(code=500,data={},msg="请检查参数")
    
    info=select_outward_investment_info_by_credit_code(credit_code=credit_code)
    context=info["outward_investment_markdown"]
    query=graph_outward_investment_registration_status_template.replace("{context}",context)
    chain= model | JsonOutputParser()
    data=chain.invoke(input=query)
    return BaseResponse(code=200,data=data,msg="success")


# 投资区域echarts信息
@graphs_app.get("/investment_hell_graph",description="投资区域地图")
async def get_outward_investment_investment_hell_graph(
    credit_code: str=Query(description="社会统一信用号"),
):
    if not credit_code:
        BaseResponse(code=500,data={},msg="请检查参数")
    
    info=select_outward_investment_info_by_credit_code(credit_code=credit_code)
    context=info["outward_investment_markdown"]
    query=graph_outward_investment_investment_hell_template.replace("{context}",context)
    chain= model | JsonOutputParser()
    data=chain.invoke(input=query)
    return BaseResponse(code=200,data=data,msg="success")

# 投资趋势echarts信息
@graphs_app.get("/investment_trend_graph",description="投资区域地图")
async def get_outward_investment_investment_trend_graph(
    credit_code: str=Query(description="社会统一信用号"),
):
    if not credit_code:
        BaseResponse(code=500,data={},msg="请检查参数")
    
    info=select_outward_investment_info_by_credit_code(credit_code=credit_code)
    context=info["outward_investment_markdown"]
    query=graph_outward_investment_investment_trend_template.replace("{context}",context)
    chain= model | JsonOutputParser()
    data=chain.invoke(input=query)
    return BaseResponse(code=200,data=data,msg="success")



