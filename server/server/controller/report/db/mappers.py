import json
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List,Dict

from server.controller.report.db.session import with_session
from server.controller.report.db.models import (
    Gsxt,
    AllInfos,
    KeyPersonnels,
    Patents,
    JudicialCase,
    Shareholders
)

@with_session
def select_qiye_all_list(session:Session,page_number=1,page_size=10)->List[Dict]:
    # 联表查询AllInfos和Gsxt表，并实现分页
    paginate_query = session.query(
        AllInfos.credit_code,
        AllInfos.qiye_name,
        AllInfos.tags,
        Gsxt
    ).join(
        Gsxt,  # 直接使用Gsxt表进行连接
        AllInfos.credit_code == Gsxt.credit_code  # 连接条件
    ).limit(
        page_size
    ).offset((page_number - 1) * page_size)
    # 获取分页查询的结果
    paginate_result = paginate_query.all()
    # 打印结果
    rows=[]
    for result in paginate_result:
        credit_code, qiye_name, tags, gsxt_info = result
        row=dict(
            credit_code=credit_code,
            qiye_name=qiye_name,
            tags=tags,
            legal_representative=gsxt_info.legal_representative,
            registration_status=gsxt_info.registration_status,
            establishment_date=gsxt_info.establishment_date,
            registered_capital=gsxt_info.registered_capital,
            capital_paid=gsxt_info.capital_paid,
            business_number=gsxt_info.business_number,
            taxpayer_number=gsxt_info.taxpayer_number,
            organization_code=gsxt_info.organization_code,
            operating_term=gsxt_info.operating_term,
            taxpayer_qualification=gsxt_info.taxpayer_qualification,
            approval_date=gsxt_info.approval_date,
            enterprise_type=gsxt_info.enterprise_type,
            personnel_size=gsxt_info.personnel_size,
            registration_authority=gsxt_info.registration_authority,
            registered_address=gsxt_info.registered_address,
            business_scope=gsxt_info.business_scope,
            logo=gsxt_info.logo
        )
        rows.append(row)
    return rows

@with_session
def select_gsxt_info_by_credit_code(session:Session,credit_code)->Dict:
    # 联表查询AllInfos和Gsxt表，并实现分页
    query = session.query(
        AllInfos.credit_code,
        AllInfos.qiye_name,
        AllInfos.tags,
        Gsxt
    ).join(
        Gsxt,  # 直接使用Gsxt表进行连接
        AllInfos.credit_code == Gsxt.credit_code  # 连接条件
    ).filter(
        AllInfos.credit_code == credit_code
    )
    # 获取分页查询的结果
    result = query.first()
    if result is None:
        return {}
    credit_code, qiye_name, tags, gsxt_info = result
    row=dict(
        credit_code=credit_code,
        qiye_name=qiye_name,
        tags=tags,
        legal_representative=gsxt_info.legal_representative,
        registration_status=gsxt_info.registration_status,
        establishment_date=gsxt_info.establishment_date,
        registered_capital=gsxt_info.registered_capital,
        capital_paid=gsxt_info.capital_paid,
        business_number=gsxt_info.business_number,
        taxpayer_number=gsxt_info.taxpayer_number,
        organization_code=gsxt_info.organization_code,
        operating_term=gsxt_info.operating_term,
        taxpayer_qualification=gsxt_info.taxpayer_qualification,
        approval_date=gsxt_info.approval_date,
        enterprise_type=gsxt_info.enterprise_type,
        personnel_size=gsxt_info.personnel_size,
        registration_authority=gsxt_info.registration_authority,
        registered_address=gsxt_info.registered_address,
        business_scope=gsxt_info.business_scope
    )
    return row


@with_session
def select_key_persons_by_credit_code(session: Session, credit_code: str, page_number: int = 1, page_size: int = 10) -> List[Dict]:
    # 分页查询KeyPersonnels表
    paginate_result = session.query(
            KeyPersonnels
        ).filter(
            KeyPersonnels.credit_code == credit_code
        ).limit(
            page_size
        ).offset((page_number - 1) * page_size)
    # 将查询结果转换为字典列表
    key_personnels_list = []
    for key_personnel in paginate_result.all():
        key_personnels_dict = {
            'id': key_personnel.id,
            'credit_code': key_personnel.credit_code,
            'name': key_personnel.name,
            'position': key_personnel.position,
            'shareholding_ratio': key_personnel.shareholding_ratio,
            'beneficial_share': key_personnel.beneficial_share
        }
        key_personnels_list.append(key_personnels_dict)
    
    return key_personnels_list

@with_session
def select_shareholder_list_by_credit_code(session: Session, credit_code: str, page_number: int = 1, page_size: int = 10) -> List[Dict]:
    # 分页查询Shareholders表
    paginate_result = session.query(Shareholders)\
                              .filter(Shareholders.credit_code == credit_code)\
                              .limit(page_size)\
                              .offset((page_number - 1) * page_size)
    
    # 将查询结果转换为字典列表
    shareholders_list = []
    for shareholder in paginate_result.all():
        shareholders_dict = {
            'id': shareholder.id,
            'credit_code': shareholder.credit_code,
            'name': shareholder.name,
            'shareholding_ratio': shareholder.shareholding_ratio,
            'capital_contribution': shareholder.capital_contribution,
            'contribution_time': shareholder.contribution_time,
            'contribution_first': shareholder.contribution_first
        }
        shareholders_list.append(shareholders_dict)
    
    return shareholders_list

@with_session
def select_judicial_case_list_by_credit_code(session: Session, credit_code: str, page_number: int = 1, page_size: int = 10) -> List[Dict]:
    # 分页查询JudicialCase表
    paginate_result = session.query(JudicialCase)\
                            .filter(JudicialCase.credit_code == credit_code)\
                            .limit(page_size)\
                            .offset((page_number - 1) * page_size)
    
    # 将查询结果转换为字典列表
    judicial_case_list = []
    for case in paginate_result.all():
        judicial_case_dict = {
            'id': case.id,
            'credit_code': case.credit_code,
            'judicial_name': case.judicial_name,
            'judicial_number': case.judicial_number,
            'cause': case.cause,
            'type': case.type,
            'case_identity': case.case_identity,
            'current_proceeding': case.current_proceeding,
            'proceeding_date': case.proceeding_date,
            'court': case.court
        }
        judicial_case_list.append(judicial_case_dict)
    
    return judicial_case_list

@with_session
def select_patent_list_by_credit_code(session: Session, credit_code: str, page_number: int = 1, page_size: int = 10) -> List[Dict]:
    # 分页查询Patents表
    paginate_result = session.query(Patents)\
                              .filter(Patents.credit_code == credit_code)\
                              .limit(page_size)\
                              .offset((page_number - 1) * page_size)
    
    # 将查询结果转换为字典列表
    patent_list = []
    for patent in paginate_result.all():
        patent_dict = {
            'id': patent.id,
            'credit_code': patent.credit_code,
            'application_date': patent.application_date,
            'patent_name': patent.patent_name,
            'patent_type': patent.patent_type,
            'patent_status': patent.patent_status,
            'application_id': patent.application_id,
            'inventor': patent.inventor
        }
        patent_list.append(patent_dict)
    
    return patent_list

# 获取对外投资信息通过社会统一编号
@with_session
def select_outward_investment_info_by_credit_code(session: Session, credit_code: str):
    # 联表查询AllInfos和Gsxt表，并实现分页
    query = session.query(
        AllInfos.credit_code,
        AllInfos.qiye_name,
        AllInfos.outward_investment_markdown,
    ).filter(
        AllInfos.credit_code == credit_code
    )
    # 获取分页查询的结果
    result = query.first()
    if result is None:
        return {}
    credit_code, qiye_name, outward_investment_markdown = result
    row=dict(
        credit_code=credit_code,
        qiye_name=qiye_name,
        outward_investment_markdown=outward_investment_markdown,
    )
    return row

@with_session
def execute_sql_and_return_json(session: Session, sql: str):
    # 执行SQL语句
    result = session.execute(text(sql))
    # 获取所有记录
    records = result.fetchall()
    # 将记录转换为字典列表
    columns = [column[0] for column in result.keys()]  # 获取列名
    records_list = [dict(zip(columns, record)) for record in records]  # 创建字典列表
    # 将字典列表转换为JSON字符串
    json_result = json.dumps(records_list, ensure_ascii=False)
    return json_result

