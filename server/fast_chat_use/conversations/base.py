from fastchat.conversation import Conversation,register_conv_template


class OpenBAConversation(Conversation):
    def get_prompt(self) -> str:
        """Get the prompt for generation."""
        system_prompt = self.system_template.format(system_message=self.system_message)
        ret = system_prompt + self.sep
        print("当前messages为:",self.messages)
        import pdb;pdb.set_trace()
        for role, message in self.messages:
            if message:
                ret += role + ": " + message + self.sep
            else:
                ret += role + ":"
        prompt="<S> {content}Assistant:  <extra_id_0>"
        prompt=prompt.format_map(dict(content=ret))
        print("当前prompt为：",prompt)
        return prompt

# register_conv_template(
#     OpenBAConversation(
#         name="openba-chat",
#         roles=("Human","Assistant"),
#         sep=" </s> "
#     )
# )