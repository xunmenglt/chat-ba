from sqlalchemy import create_engine, Column, Integer, String, Text, BigInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.controller.report.db.base import Qiye_Base

class AllInfos(Qiye_Base):
    """企业信息数据表"""
    __tablename__ = 'all_infos'
    credit_code = Column(String(30), primary_key=True, nullable=False, comment='企业统一社会信用代码')
    qiye_name = Column(String(100), comment='企业名称')
    gsxt_info_markdown = Column(Text, comment='工商信息MarkDown格式数据')
    key_personnels_markdown = Column(Text, comment='主要人员MarkDown格式数据')
    shareholders_markdown = Column(Text, comment='公司股东MarkDown格式数据')
    outward_investment_markdown = Column(Text, comment='对外投资MarkDown格式数据')
    judicial_case_markdown = Column(Text, comment='司法案件MarkDown格式数据')
    patents_markdown = Column(Text, comment='发明专利MarkDown格式数据')
    tags = Column(String(300), comment='标签')

class Gsxt(Qiye_Base):
    """工商信息表"""
    __tablename__ = 'gsxt'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='唯一标识ID')
    name = Column(String(200), nullable=False, comment='企业名称')
    credit_code = Column(String(30), nullable=False, comment='统一社会信用代码')
    legal_representative = Column(String(50), comment='法定代表人')
    registration_status = Column(String(50), comment='登记状态')
    establishment_date = Column(String(10), comment='成立日期')
    registered_capital = Column(String(50), comment='注册资本')
    capital_paid = Column(String(50), comment='实缴资本')
    business_number = Column(String(30), comment='工商注册号')
    taxpayer_number = Column(String(30), comment='纳税人识别号')
    organization_code = Column(String(30), comment='组织机构代码')
    operating_term = Column(String(30), comment='营业期限')
    taxpayer_qualification = Column(String(30), comment='纳税人资质')
    approval_date = Column(String(30), comment='核准日期')
    enterprise_type = Column(String(30), comment='企业类型')
    personnel_size = Column(String(50), comment='人员规模')
    registration_authority = Column(String(50), comment='登记机关')
    registered_address = Column(String(100), comment='注册地址')
    business_scope = Column(Text, comment='经营范围')
    logo = Column(Text, comment='企业logo')

class JudicialCase(Qiye_Base):
    """司法案件信息表"""
    __tablename__ = 'judicial_case'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='唯一标识ID')
    credit_code = Column(String(30), comment='所属企业统一社会信用代码')
    judicial_name = Column(String(500), comment='案件名称')
    judicial_number = Column(String(100), comment='相关案号')
    cause = Column(String(50), comment='案由')
    type = Column(String(50), comment='案件类型')
    case_identity = Column(String(50), comment='案件身份')
    current_proceeding = Column(String(50), comment='当前审理程序')
    proceeding_date = Column(String(10), comment='当前审理程序日期')
    court = Column(String(100), comment='法院')

class KeyPersonnels(Qiye_Base):
    """主要人员信息表"""
    __tablename__ = 'key_personnels'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='唯一标识ID')
    credit_code = Column(String(30), comment='所属企业统一社会信用代码')
    name = Column(String(30), nullable=False, comment='姓名')
    position = Column(String(30), comment='职位')
    shareholding_ratio = Column(String(10), comment='持股比例')
    beneficial_share = Column(String(10), comment='最终受益股份')

class Patents(Qiye_Base):
    """发明专利信息表"""
    __tablename__ = 'patents'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='唯一标识ID')
    credit_code = Column(String(30), comment='所属企业统一社会信用代码')
    application_date = Column(String(10), comment='申请日期')
    patent_name = Column(String(100), comment='专利名称')
    patent_type = Column(String(50), comment='专利类型')
    patent_status = Column(String(50), comment='专利状态')
    application_id = Column(String(30), comment='申请号')
    inventor = Column(String(500), comment='发明人（可多个）')

class Shareholders(Qiye_Base):
    """股东信息表"""
    __tablename__ = 'shareholders'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='唯一标识')
    credit_code = Column(String(30), comment='所属企业统一社会信用代码')
    name = Column(String(50), comment='股东名称')
    shareholding_ratio = Column(String(10), comment='持股比例')
    capital_contribution = Column(String(30), comment='认缴出资额(万元)')
    contribution_time = Column(String(10), comment='认缴出资日期')
    contribution_first = Column(String(10), comment='首次持股日期')