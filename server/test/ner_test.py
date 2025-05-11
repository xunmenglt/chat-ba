# -*- coding:UTF-8 -*-
# @Time : 2024/3/12 19:53
# @Author : 寻梦
# @File : ner_test
# @Project : ChatBA-Server
input_str="请说出【资质名称】在文本中是否出现？"
start_index=input_str.index("【")
end_index=input_str.index("】")

print(input_str[start_index+1:end_index])