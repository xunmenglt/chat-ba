# -*- coding:UTF-8 -*-
# @Time : 2024/3/9 15:18
# @Author : 寻梦
# @File : conversation_callback_handler
# @Project : langchain-ChatBA
from typing import Dict, Any, List, Optional
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain.schema import LLMResult
from server.db.mapper.conversation_mapper import update_message


class ConversationCallBackHandler(BaseCallbackHandler):
    raise_error: bool = True


    def __init__(self, conversation_id: str, message_id: str, chat_type: str, query: str):
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.chat_type = chat_type
        self.query = query
        self.start_at = None

    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID,
                            parent_run_id: Optional[UUID] = None, tags: Optional[List[str]] = None,
                            metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        pass
    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        pass

    def on_llm_end(
        self, response: LLMResult, **kwargs: Any
    ) -> Any:
        answer = response.generations[0][0].text
        update_message(self.message_id, answer)