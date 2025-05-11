import pdfplumber
import dataclasses
import re
import random
import os
from typing import List,Any,Set,Tuple


def random_two_num(x):
    if x <= 0:
        raise ValueError("x必须为正整数")
    
    a1 = random.randint(0, x - 1)
    while True:
        a2 = random.randint(0, x - 1)
        if a2!=a1:
            break
    if a1<a2:
        return a1,a2 
    else:
        return a2,a1

def random_one_num(x):
    if x <= 0:
        raise ValueError("x必须为正整数")
    
    a1 = random.randint(0, x - 1)
    return a1

@dataclasses.dataclass
class TextParser:
    # 文本
    content:str=None
    '''
    文本解析器
    '''
    def text_split(self)->List[str]:
        """
        to do split text
        """
        pass
    

class ChapterRegulationTextParser(TextParser):
    # 随机章节
    history:Set[Tuple]=set()

    chapter_regulation_list:List[Any]=[]

    file_path:str

    def __init__(self,file_path:str,do_split=True):
        if not os.path.isfile(file_path):
            raise FileExistsError(f"{file_path} 文件不存在")
        if not file_path.__contains__(".pdf"):
            raise ValueError(f"{file_path} 该文件不是pdf")
        self.content=ChapterRegulationTextParser.parse_pdf_to_content(file_path)
        if do_split:
            self.text_split(self.content)

    def text_split(self,content) -> List[Any]:
        chapters=self.chapter_regulation_or_split(content)
        prompts=[{"prefix":"","item":[{"text":chapters[0].strip(),"item_index":0}],"chapter_index":0}]
        item_pattern = re.compile(rf"({'第'}\s*[一二三四五六七八九十零百千\d]+\s*{'条'})")
        for chapter_index,chapter in enumerate(chapters):
            items=self.chapter_regulation_or_split(chapter.strip(),prefix="第",suffix="条")
            temp_prompts={"prefix":items[0].strip(),"item":[],"chapter_index":chapter_index}
            for item_index,item in enumerate(items):
                if len(item_pattern.findall(item))!=0:
                    temp_prompts["item"].append({"text":item.strip(),"item_index":item_index})
            # if len(temp_prompts["text"])!=0:
            prompts.append(temp_prompts)
        self.chapter_regulation_list=prompts
        return prompts
        

    def chapter_regulation_or_split(self,content,prefix="第", suffix="章")->List[str]:
        # 构建正则表达式模式，允许章节编号中间有空格
        chapter_pattern = re.compile(rf"({prefix}\s*[一二三四五六七八九十零百千\d]+\s*{suffix})")
        # 使用正则表达式进行切分
        parts = chapter_pattern.split(content)
        # 将切分后的部分重新组合，保留切分符
        chapters = []
        current_chapter = ""
        for part in parts:
            if chapter_pattern.match(part):
                if current_chapter:
                    chapters.append(current_chapter)
                current_chapter = part
            else:
                current_chapter += part
        # 添加最后一个章节
        if current_chapter:
            chapters.append(current_chapter)
        return chapters
    
    def mixed2regulation(self)->Any:
        if not self.chapter_regulation_list:
            raise ValueError("无法获取章节和条例信息")
        chapter_regulation_len=len(self.chapter_regulation_list)
        max_count=len(self.chapter_regulation_list)*2
        while True and max_count>0:
            a1,a2=random_two_num(chapter_regulation_len)
            if len(self.chapter_regulation_list[a1]["item"])!=0 and len(self.chapter_regulation_list[a2]["item"])!=0 and self.chapter_regulation_list[a1]["chapter_index"]!=self.chapter_regulation_list[a2]["chapter_index"]:
                b1=random_one_num(len(self.chapter_regulation_list[a1]["item"]))
                b2=random_one_num(len(self.chapter_regulation_list[a2]["item"]))
                if (a1,b1,a2,b2) not in self.history:
                    self.history.add((a1,b1,a2,b2))
                    return {
                        "chapter_01":self.chapter_regulation_list[a1]["prefix"],
                        "item_01":self.chapter_regulation_list[a1]["item"][b1]["text"],
                        "chapter_02":self.chapter_regulation_list[a2]["prefix"],
                        "item_02":self.chapter_regulation_list[a2]["item"][b2]["text"],
                        "chapter_index":[self.chapter_regulation_list[a1]["chapter_index"],self.chapter_regulation_list[a2]["chapter_index"]],
                        "item_index":[self.chapter_regulation_list[a1]["item"][b1]["item_index"],self.chapter_regulation_list[a2]["item"][b2]["item_index"]]
                    }
            max_count-=1
        return None

    @staticmethod
    def duplicate2word(content):
        preWord=""
        text=""
        if not content:
            return ""
        for word in content:
            if preWord!=word:
                text+=word
                preWord=word
        return text
    
    @staticmethod
    def write_content_to_file(content,file_path):
        with open(file_path,'w',encoding="utf-8") as fp:
            fp.write(content)

    @staticmethod
    def parse_pdf_to_content(pdf_path):
        content=""
        with pdfplumber.open(pdf_path) as reader:
            for page in reader.pages:
                text=page.extract_text()
                content=content+ChapterRegulationTextParser.duplicate2word(text)
        return content


    

if __name__=="__main__":
    file_path='/opt/data/private/liuteng/code/dev/ChatBA-Server/tmp/3395d9902c8c11ef89e3aeacc37799c1/融资担保公司监督管理条例.pdf'
    textParser=ChapterRegulationTextParser(file_path=file_path)
    print(textParser.mixed2regulation())

