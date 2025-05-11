import os
from fastapi import APIRouter,Query,Body
from server.controller.report.db.mappers import (
    select_qiye_all_list,
    select_gsxt_info_by_credit_code,
    select_judicial_case_list_by_credit_code,
    select_key_persons_by_credit_code,
    select_patent_list_by_credit_code,
    select_shareholder_list_by_credit_code
)
from server.controller.utils import BaseResponse

tables_app=APIRouter(tags=["企业报告表格数据api"],prefix="/tables")


# 获取首页数据
@tables_app.get("/index",description="获取首页列表数据")
async def index_list(
    page_number:int=Query(default=1,ge=1,description="页码"),
page_size: int = Query(default=10, ge=1, description="每页显示的记录数")
)->BaseResponse:
    index_list=select_qiye_all_list(page_number=page_number,page_size=page_size)
    return BaseResponse(code=200,data=index_list,msg="success")


# 获取工商信息
@tables_app.get("/gsxt",description="获取工商信息")
async def get_gsxt_data(
    credit_code: str=Query(description="社会统一信用号"),
):
    if not credit_code:
        BaseResponse(code=500,data={},msg="请检查参数")
    
    info=select_gsxt_info_by_credit_code(credit_code=credit_code)
    
    return BaseResponse(code=200,data=info,msg="success")

# 获取主要人员
@tables_app.get("/key_persons",description="获取主要人员")
async def key_person_list(
    credit_code: str=Query(description="社会统一信用号"),
    page_number:int=Query(default=1,ge=1,description="页码"),
    page_size: int = Query(default=10, ge=1, description="每页显示的记录数")
)->BaseResponse:
    data=select_key_persons_by_credit_code(credit_code=credit_code,page_number=page_number,page_size=page_size)
    return BaseResponse(code=200,data=data,msg="success")

# 获取股东信息
@tables_app.get("/shareholders",description="获取股东信息")
async def shareholder_list(
    credit_code: str=Query(description="社会统一信用号"),
    page_number:int=Query(default=1,ge=1,description="页码"),
    page_size: int = Query(default=10, ge=1, description="每页显示的记录数")
)->BaseResponse:
    data=select_shareholder_list_by_credit_code(credit_code=credit_code,page_number=page_number,page_size=page_size)
    return BaseResponse(code=200,data=data,msg="success")

# 获取司法案件
@tables_app.get("/judicial_cases",description="获取司法案件列表数据")
async def judicial_case_list(
    credit_code: str=Query(description="社会统一信用号"),
    page_number:int=Query(default=1,ge=1,description="页码"),
    page_size: int = Query(default=10, ge=1, description="每页显示的记录数")
)->BaseResponse:
    data=select_judicial_case_list_by_credit_code(credit_code=credit_code,page_number=page_number,page_size=page_size)
    return BaseResponse(code=200,data=data,msg="success")

# 获取发明专利
@tables_app.get("/patents",description="获取发明专利列表数据")
async def patent_lsit(
    credit_code: str=Query(description="社会统一信用号"),
    page_number:int=Query(default=1,ge=1,description="页码"),
    page_size: int = Query(default=10, ge=1, description="每页显示的记录数")
)->BaseResponse:
    data=select_patent_list_by_credit_code(credit_code=credit_code,page_number=page_number,page_size=page_size)
    return BaseResponse(code=200,data=data,msg="success")
