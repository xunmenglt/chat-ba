# -*- coding:UTF-8 -*-
# @Time : 2024/3/7 11:09
# @Author : 寻梦
# @File : konwledgeDocController
# @Project : langchain-ChatBA


from fastapi import APIRouter,Body,UploadFile,File,Form
from configs import logger,log_verbose,CHUNK_SIZE,OVERLAP_SIZE
from server.utils import (get_file_path,run_in_thread_pool,validate_factory_name)
from server.services.knowledge_base.base import KBServiceFactory
from server.db.mapper.knowledge_file_mapper import get_file_detail
from server.controller.utils import *
from server.knowledge_file_utils.konwledgefile import KnowLedgeFile,files2docs_in_thread



konwledge_doc_app=APIRouter(tags=["文件文档管理api"],prefix="/konwledge_doc")



# @konwledge_doc_app.post("/upload_files",description="上传文件")
'''
多线程保存文件
'''

def _save_files_in_thread(files: List[UploadFile],
                          factory_name: str,
                          override: bool):
    """
    通过多线程将上传的文件保存到对应知识库目录内。
    生成器返回保存结果：{"code":200, "msg": "xxx", "data": {"knowledge_base_name":"xxx", "file_name": "xxx"}}
    """

    def save_file(file: UploadFile, factory_name: str, override: bool) -> dict:
        '''
        保存单个文件。
        '''
        try:
            filename = file.filename
            file_path = get_file_path(factory_name=factory_name, doc_name=filename)
            data = {"factory_name": factory_name, "file_name": filename}
            file_content = file.file.read()  # 读取上传文件的内容
            if (os.path.isfile(file_path)
                    and not override
                    and os.path.getsize(file_path) == len(file_content)
            ):
                file_status = f"文件 {filename} 已存在。"
                logger.warn(file_status)
                return dict(code=404, msg=file_status, data=data)

            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "wb") as f:
                f.write(file_content)
            return dict(code=200, msg=f"成功上传文件 {filename}", data=data)
        except Exception as e:
            msg = f"{filename} 文件上传失败，报错信息为: {e}"
            logger.error(f'{e.__class__.__name__}: {msg}',
                         exc_info=e if log_verbose else None)
            return dict(code=500, msg=msg, data=data)

    params = [{"file": file, "factory_name": factory_name, "override": override} for file in files]
    for result in run_in_thread_pool(save_file, params=params):
        yield result



# 更新知识库文档
# @konwledge_doc_app.post("/update_docs",description="上传文件")
def update_docs(
        factory_name:str=Body(...,description="知识库名称",examples=["myfactory"]),
        file_names:List[str]=Body(...,description="支持文件名称，支持多文件",examples=[["file_name_1.txt","file_name_2.pdf"]]),
        chunk_size:int=Body(CHUNK_SIZE,description="知识库中单段文本最大长度"),
        chunk_overlap:int=Body(OVERLAP_SIZE,description="知识库中相邻文本重合长度"),
)->BaseResponse:


    if not validate_factory_name(factory_name):
        return BaseResponse(code=403,msg="不要对我进行注入操作，谢谢")
    konwledge_factory=KBServiceFactory.get_service_by_name(factory_name)

    # 判断知识库是否存在
    if konwledge_factory is None:
        return BaseResponse(code=404,msg=f"知识库 {factory_name} 不存在")

    failed_files=[]

    kb_files=[KnowLedgeFile(filename=file_name,factory_name=factory_name) for file_name in file_names]

    # 从文件生成文档
    for status, result in files2docs_in_thread(kb_files,
                                               chunk_size=chunk_size,
                                               chunk_overlap=chunk_overlap):
        if status:
            factory_name, file_name, new_docs = result
            kb_file = KnowLedgeFile(filename=file_name,
                                    factory_name=factory_name)
            kb_file.splited_docs = new_docs

            konwledge_factory.update_doc(kb_file, not_refresh_vs_cache=True)
        else:
            factory_name, file_name, error = result
            failed_files.append({"file_name":file_name,"msg":error})

    return BaseResponse(code=200, msg=f"更新文档完成", data={"failed_files": failed_files})


"""
上传文件，并都文件信息进行保存，和向量化
"""
@konwledge_doc_app.post("/upload_docs",description="上传文档（可多个上传）")
async def upload_docs(
        files:List[UploadFile]=File(...,description="上传文件，支持多个文件"),
        factory_name:str=Form(...,description="知识库名字"),
        override:bool=Form(False,description="是否覆盖已有的文件,默认为False"),
        is_vector_store:bool=Form(True,description="上传文件后是否进行向量化"),
        chunk_size:int=Form(CHUNK_SIZE,description="生成向量时文本最大长度"),
        chunk_overlap:int=Form(OVERLAP_SIZE,description="切分文本重叠长度"),
)->BaseResponse:
    if not validate_factory_name(factory_name):
        return BaseResponse(code=403,msg="不要进行注入操作")
    konwledge_factory=KBServiceFactory.get_service_by_name(factory_name)
    if konwledge_factory is None:
        return BaseResponse(code=404,msg=f"知识库 {factory_name} 未创建")
    failed_files=[] # 失败上传的文件
    success_files=set()
    for result in _save_files_in_thread(files,factory_name,override):
        filename=result['data']["file_name"]
        if result["code"]!=200:
            failed_files.append({"file_name":filename,"msg":result["msg"]})
        if filename not in success_files:
            success_files.add(filename)

    # 对文件进行向量化
    if is_vector_store:
        ## 上传文档
        result=update_docs(
            factory_name=factory_name,
            file_names=success_files,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        failed_files=failed_files+result.data["failed_files"]

    return BaseResponse(code=200, msg="文件上传与向量化完成", data={"failed_files": failed_files})




@konwledge_doc_app.post("/delete_konwledge_file",description="根据知识库名和文件名删除知识文件")
async def delete_file_by_action(
        factory_name:str=Body(...,description="知识库名字",examples=["medical","mytest"]),
        file_name:str=Body(...,description="文件名",examples=["a.pdf"])
    )->BaseResponse:

    # 首先根据知识库名获取知识库对象
    factory_service=KBServiceFactory.get_service_by_name(kb_name=factory_name)
    kb_file=KnowLedgeFile(filename=file_name,factory_name=factory_name)
    status=factory_service.delete_doc(kb_file,delete_content=True)
    if status:
        return BaseResponse(code=200,msg=f"知识库 {factory_name} 中的 {file_name} 删除成功")
    return BaseResponse(code=500,msg="删除失败")


