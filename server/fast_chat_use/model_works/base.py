from fastchat.serve.model_worker import ModelWorker
from fastchat.conversation import Conversation

class XmModelWorker(ModelWorker):
    def make_conv_template(
        self,
        conv_template: str = None,
        model_path: str = None,
    ) -> Conversation:
        """
        can be overrided to costomize the conversation template for different model workers.
        """
        from fastchat.conversation import get_conv_template
        from fastchat.model.model_adapter import get_conversation_template

        if conv_template:
            conv = get_conv_template(conv_template)
        else:
            conv = get_conversation_template(model_path)
        return conv