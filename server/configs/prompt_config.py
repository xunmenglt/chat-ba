# LLM对话支持的变量：
#   - input: 用户输入内容

# 知识库和搜索引擎对话支持的变量：
#   - context: 从检索结果拼接的知识文本
#   - question: 用户提出的问题
PROMPT_TEMPLATES = {
    "dialogue": {
        "default":
            '{{input}}',

        "with_history":
            'The following is a friendly conversation between a human and an AI. '
            'The AI is talkative and provides lots of specific details from its context. '
            'If the AI does not know the answer to a question, it truthfully says it does not know.\n\n'
            'Current conversation:\n'
            '{{history}}\n'
            'Human: {{input}}\n'
            'AI:',

        "py":
            '你是一个聪明的代码助手，请你给我写出简单的py代码。 \n'
            '{{ input }}',

        "llama_medical":
            '<s>Human：你是一位医生，请回答：{{input}}\n</s><s>Assistant: ',

        "OpenBA":
            '<S> {{history}}Human: {{input}} </s> Assistant:  <extra_id_0>'
    },


    "retrieval": {
        "default":
            '<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，'
            '不允许在答案中添加编造成分，答案请使用中文。 </指令>\n'
            '<已知信息>{{context}}</已知信息>\n'
            '<问题>{{question}}</问题>\n',

        "text":
            '<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，答案请使用中文。 </指令>\n'
            '<已知信息>{{context}}</已知信息>\n'
            '<问题>{{question}}</问题>\n',

        "empty":  # 搜不到知识库的时候使用
            '请你回答我的问题:\n'
            '{{question}}\n\n',
    },

    "generation":{
        "default":
            "{{context}}\n\n以上是参考文档，其中包括多条信息，请根据参考文档的内容，设计一个相对复杂的问题，尽可能涵盖文档内的信息，并给出答案，"
            "以{'question':问题,'answer':答案}的格式输出。\n",
        "mut":
            "{{context}}\n\n以上是参考文档，请根据参考文档的内容，设计{{count}}个问题和答案，问题相对复杂，且问题应包含一个至多个条例，答案尽可能的详细，且法律的具体名称应该具体说明，法律名称不可用“本法”等通用词代替，以{'question':问题,'answer':答案}的格式输出，每行一个。\n"
    }

}
