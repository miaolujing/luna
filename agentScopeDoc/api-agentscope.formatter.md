The formatter module in agentscope.

*class* FormatterBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_formatter_base.html#FormatterBase)[¶](#agentscope.formatter.FormatterBase "Link to this definition")

基类：`object`

The base class for formatters.

*abstract async* format(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_formatter_base.html#FormatterBase.format)[¶](#agentscope.formatter.FormatterBase.format "Link to this definition")

Format the Msg objects to a list of dictionaries that satisfy the API requirements.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

list\[dict\[str, *Any*\]\]

*static* assert\_list\_of\_msgs(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_formatter_base.html#FormatterBase.assert_list_of_msgs)[¶](#agentscope.formatter.FormatterBase.assert_list_of_msgs "Link to this definition")

Assert that the input is a list of Msg objects.

参数:

**msgs** (list\[Msg\]) -- A list of Msg objects to be validated.

返回类型:

None

*static* convert\_tool\_result\_to\_string(*output*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_formatter_base.html#FormatterBase.convert_tool_result_to_string)[¶](#agentscope.formatter.FormatterBase.convert_tool_result_to_string "Link to this definition")

Turn the tool result list into a textual output to be compatible with the LLM API that doesn't support multimodal data.

参数:

**output** (str | List\[TextBlock | ImageBlock | AudioBlock\]) -- The output of the tool response, including text and multimodal data like images and audio.

返回:

A string representation of the tool result, with text blocks concatenated and multimodal data represented by file paths or URLs.

返回类型:

str

*class* TruncatedFormatterBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase)[¶](#agentscope.formatter.TruncatedFormatterBase "Link to this definition")

基类：[`FormatterBase`](#agentscope.formatter.FormatterBase "agentscope.formatter._formatter_base.FormatterBase"), `ABC`

Base class for truncated formatters, which formats input messages into required formats with tokens under a specified limit.

\_\_init\_\_(*token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase.__init__)[¶](#agentscope.formatter.TruncatedFormatterBase.__init__ "Link to this definition")

Initialize the TruncatedFormatterBase.

参数:

-   **token\_counter** (TokenCounterBase | None, optional) -- A token counter instance used to count tokens in the messages. If not provided, the formatter will format the messages without considering token limits.
    
-   **max\_tokens** (int | None, optional) -- The maximum number of tokens allowed in the formatted messages. If not provided, the formatter will not truncate the messages.
    

返回类型:

None

*async* format(*msgs*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase.format)[¶](#agentscope.formatter.TruncatedFormatterBase.format "Link to this definition")

Format the input messages into the required format. If token counter and max token limit are provided, the messages will be truncated to fit the limit.

参数:

-   **msgs** (list\[Msg\]) -- The input messages to be formatted.
    
-   **kwargs** (*Any*)
    

返回:

The formatted messages in the required format.

返回类型:

list\[dict\[str, Any\]\]

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase._format)[¶](#agentscope.formatter.TruncatedFormatterBase._format "Link to this definition")

Format the input messages into the required format. This method should be implemented by the subclasses.

参数:

**msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)

返回类型:

list\[dict\[str, *Any*\]\]

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase._format_tool_sequence)[¶](#agentscope.formatter.TruncatedFormatterBase._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the LLM API.

参数:

**msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)

返回类型:

list\[dict\[str, *Any*\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_truncated_formatter_base.html#TruncatedFormatterBase._format_agent_message)[¶](#agentscope.formatter.TruncatedFormatterBase._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the LLM API.

参数:

-   **msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)
    
-   **is\_first** (*bool*)
    

返回类型:

list\[dict\[str, *Any*\]\]

*class* DashScopeChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeChatFormatter)[¶](#agentscope.formatter.DashScopeChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Formatter for DashScope messages.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.DashScopeChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= False*[¶](#agentscope.formatter.DashScopeChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.DashScopeChatFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.DashScopeChatFormatter.supported_blocks "Link to this definition")

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeChatFormatter._format)[¶](#agentscope.formatter.DashScopeChatFormatter._format "Link to this definition")

Format message objects into DashScope API format.

参数:

**msgs** (list\[Msg\]) -- The list of message objects to format.

返回:

The formatted messages as a list of dictionaries.

返回类型:

list\[dict\[str, Any\]\]

*class* DashScopeMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeMultiAgentFormatter)[¶](#agentscope.formatter.DashScopeMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

DashScope formatter for multi-agent conversations, where more than a user and an agent are involved.

备注

This formatter will combine previous messages (except tool calls/results) into a history section in the first system message with the conversation history prompt.

备注

For tool calls/results, they will be presented as separate messages as required by the DashScope API. Therefore, the tool calls/ results messages are expected to be placed at the end of the input messages.

小技巧

Telling the assistant's name in the system prompt is very important in multi-agent conversations. So that LLM can know who it is playing as.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.DashScopeMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.DashScopeMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.DashScopeMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.DashScopeMultiAgentFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeMultiAgentFormatter.__init__)[¶](#agentscope.formatter.DashScopeMultiAgentFormatter.__init__ "Link to this definition")

Initialize the DashScope multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to use for the conversation history section.
    
-   **token\_counter** (TokenCounterBase | None, optional) -- The token counter used for truncation.
    
-   **max\_tokens** (int | None, optional) -- The maximum number of tokens allowed in the formatted messages. If None, no truncation will be applied.
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.DashScopeMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the DashScope API.

参数:

**msgs** (list\[Msg\]) -- The list of messages containing tool calls/results to format.

返回:

A list of dictionaries formatted for the DashScope API.

返回类型:

list\[dict\[str, Any\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_dashscope_formatter.html#DashScopeMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.DashScopeMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into a user message with conversation history tags. For the first agent message, it will include the conversation history prompt.

参数:

-   **msgs** (list\[Msg\]) -- A list of Msg objects to be formatted.
    
-   **is\_first** (bool, defaults to True) -- Whether this is the first agent message in the conversation. If True, the conversation history prompt will be included.
    

返回:

A list of dictionaries formatted for the DashScope API.

返回类型:

list\[dict\[str, Any\]\]

*class* OpenAIChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIChatFormatter)[¶](#agentscope.formatter.OpenAIChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

The class used to format message objects into the OpenAI API required format.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.OpenAIChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.OpenAIChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversation

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.OpenAIChatFormatter.support_vision "Link to this definition")

Whether support vision models

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.OpenAIChatFormatter.supported_blocks "Link to this definition")

Supported message blocks for OpenAI API

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIChatFormatter._format)[¶](#agentscope.formatter.OpenAIChatFormatter._format "Link to this definition")

Format message objects into OpenAI API required format.

参数:

**msgs** (list\[Msg\]) -- The list of Msg objects to format.

返回:

A list of dictionaries, where each dictionary has "name", "role", and "content" keys.

返回类型:

list\[dict\[str, Any\]\]

*class* OpenAIMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIMultiAgentFormatter)[¶](#agentscope.formatter.OpenAIMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

OpenAI formatter for multi-agent conversations, where more than a user and an agent are involved. .. tip:: This formatter is compatible with OpenAI API and OpenAI-compatible services like vLLM, Azure OpenAI, and others.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.OpenAIMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.OpenAIMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversation

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.OpenAIMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision models

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.OpenAIMultiAgentFormatter.supported_blocks "Link to this definition")

Supported message blocks for OpenAI API

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIMultiAgentFormatter.__init__)[¶](#agentscope.formatter.OpenAIMultiAgentFormatter.__init__ "Link to this definition")

Initialize the OpenAI multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to use for the conversation history section.
    
-   **token\_counter** ([*TokenCounterBase*](https://doc.agentscope.io/zh_CN/api/agentscope.token.html#agentscope.token.TokenCounterBase "agentscope.token._token_base.TokenCounterBase") *|* *None*)
    
-   **max\_tokens** (*int* *|* *None*)
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.OpenAIMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the OpenAI API.

参数:

**msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)

返回类型:

list\[dict\[str, *Any*\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_openai_formatter.html#OpenAIMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.OpenAIMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the OpenAI API.

参数:

-   **msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)
    
-   **is\_first** (*bool*)
    

返回类型:

list\[dict\[str, *Any*\]\]

*class* AnthropicChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicChatFormatter)[¶](#agentscope.formatter.AnthropicChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Formatter for Anthropic messages.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.AnthropicChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= False*[¶](#agentscope.formatter.AnthropicChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.AnthropicChatFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.AnthropicChatFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicChatFormatter._format)[¶](#agentscope.formatter.AnthropicChatFormatter._format "Link to this definition")

Format message objects into Anthropic API format.

参数:

**msgs** (list\[Msg\]) -- The list of message objects to format.

返回:

The formatted messages as a list of dictionaries.

返回类型:

list\[dict\[str, Any\]\]

备注

Anthropic suggests always passing all previous thinking blocks back to the API in subsequent calls to maintain reasoning continuity. For more details, please refer to [Anthropic's documentation](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#preserving-thinking-blocks).

*class* AnthropicMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicMultiAgentFormatter)[¶](#agentscope.formatter.AnthropicMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Anthropic formatter for multi-agent conversations, where more than a user and an agent are involved.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.AnthropicMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.AnthropicMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.AnthropicMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.AnthropicMultiAgentFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicMultiAgentFormatter.__init__)[¶](#agentscope.formatter.AnthropicMultiAgentFormatter.__init__ "Link to this definition")

Initialize the DashScope multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to use for the conversation history section.
    
-   **token\_counter** ([*TokenCounterBase*](https://doc.agentscope.io/zh_CN/api/agentscope.token.html#agentscope.token.TokenCounterBase "agentscope.token._token_base.TokenCounterBase") *|* *None*)
    
-   **max\_tokens** (*int* *|* *None*)
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.AnthropicMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the Anthropic API.

参数:

**msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)

返回类型:

list\[dict\[str, *Any*\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_anthropic_formatter.html#AnthropicMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.AnthropicMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the Anthropic API.

参数:

-   **msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)
    
-   **is\_first** (*bool*)
    

返回类型:

list\[dict\[str, *Any*\]\]

*class* GeminiChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiChatFormatter)[¶](#agentscope.formatter.GeminiChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

The formatter for Google Gemini API.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.GeminiChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= False*[¶](#agentscope.formatter.GeminiChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.GeminiChatFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.VideoBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.GeminiChatFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

supported\_extensions*: dict\[str, list\[str\]\]* *\= {'audio': \['mp3', 'wav', 'aiff', 'aac', 'ogg', 'flac'\], 'image': \['png', 'jpeg', 'webp', 'heic', 'heif'\], 'video': \['mp4', 'mpeg', 'mov', 'avi', 'x-flv', 'mpg', 'webm', 'wmv', '3gpp'\]}*[¶](#agentscope.formatter.GeminiChatFormatter.supported_extensions "Link to this definition")

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiChatFormatter._format)[¶](#agentscope.formatter.GeminiChatFormatter._format "Link to this definition")

Format message objects into Gemini API required format.

参数:

**msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]*)

返回类型:

list\[dict\]

*class* GeminiMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiMultiAgentFormatter)[¶](#agentscope.formatter.GeminiMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

The multi-agent formatter for Google Gemini API, where more than a user and an agent are involved.

备注

This formatter will combine previous messages (except tool calls/results) into a history section in the first system message with the conversation history prompt.

备注

For tool calls/results, they will be presented as separate messages as required by the Gemini API. Therefore, the tool calls/ results messages are expected to be placed at the end of the input messages.

小技巧

Telling the assistant's name in the system prompt is very important in multi-agent conversations. So that LLM can know who it is playing as.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.GeminiMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.GeminiMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.GeminiMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.VideoBlock'>, <class 'agentscope.message.\_message\_block.AudioBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.GeminiMultiAgentFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiMultiAgentFormatter.__init__)[¶](#agentscope.formatter.GeminiMultiAgentFormatter.__init__ "Link to this definition")

Initialize the Gemini multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to be used for the conversation history section.
    
-   **token\_counter** (TokenCounterBase | None, optional) -- The token counter used for truncation.
    
-   **max\_tokens** (int | None, optional) -- The maximum number of tokens allowed in the formatted messages. If None, no truncation will be applied.
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.GeminiMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the Gemini API.

参数:

**msgs** (list\[Msg\]) -- The list of messages containing tool calls/results to format.

返回:

A list of dictionaries formatted for the Gemini API.

返回类型:

list\[dict\[str, Any\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_gemini_formatter.html#GeminiMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.GeminiMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the Gemini API.

参数:

-   **msgs** (list\[Msg\]) -- A list of Msg objects to be formatted.
    
-   **is\_first** (bool, defaults to True) -- Whether this is the first agent message in the conversation. If True, the conversation history prompt will be included.
    

返回:

A list of dictionaries formatted for the Gemini API.

返回类型:

list\[dict\[str, Any\]\]

*class* OllamaChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaChatFormatter)[¶](#agentscope.formatter.OllamaChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Formatter for Ollama messages.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.OllamaChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= False*[¶](#agentscope.formatter.OllamaChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.OllamaChatFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.OllamaChatFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaChatFormatter._format)[¶](#agentscope.formatter.OllamaChatFormatter._format "Link to this definition")

Format message objects into Ollama API format.

参数:

**msgs** (list\[Msg\]) -- The list of message objects to format.

返回:

The formatted messages as a list of dictionaries.

返回类型:

list\[dict\[str, Any\]\]

*class* OllamaMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaMultiAgentFormatter)[¶](#agentscope.formatter.OllamaMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Ollama formatter for multi-agent conversations, where more than a user and an agent are involved.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.OllamaMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.OllamaMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= True*[¶](#agentscope.formatter.OllamaMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ImageBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.OllamaMultiAgentFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaMultiAgentFormatter.__init__)[¶](#agentscope.formatter.OllamaMultiAgentFormatter.__init__ "Link to this definition")

Initialize the Ollama multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to use for the conversation history section.
    
-   **token\_counter** (TokenCounterBase | None, optional) -- The token counter used for truncation.
    
-   **max\_tokens** (int | None, optional) -- The maximum number of tokens allowed in the formatted messages. If None, no truncation will be applied.
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.OllamaMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the Ollama API.

参数:

**msgs** (list\[Msg\]) -- The list of messages containing tool calls/results to format.

返回:

A list of dictionaries formatted for the Ollama API.

返回类型:

list\[dict\[str, Any\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_ollama_formatter.html#OllamaMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.OllamaMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the Ollama API.

参数:

-   **msgs** (list\[Msg\]) -- A list of Msg objects to be formatted.
    
-   **is\_first** (bool, defaults to True) -- Whether this is the first agent message in the conversation. If True, the conversation history prompt will be included.
    

返回:

A list of dictionaries formatted for the ollama API.

返回类型:

list\[dict\[str, Any\]\]

*class* DeepSeekChatFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekChatFormatter)[¶](#agentscope.formatter.DeepSeekChatFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

Formatter for DeepSeek messages.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.DeepSeekChatFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= False*[¶](#agentscope.formatter.DeepSeekChatFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= False*[¶](#agentscope.formatter.DeepSeekChatFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.DeepSeekChatFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

*async* \_format(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekChatFormatter._format)[¶](#agentscope.formatter.DeepSeekChatFormatter._format "Link to this definition")

Format message objects into DeepSeek API format.

参数:

**msgs** (list\[Msg\]) -- The list of message objects to format.

返回:

The formatted messages as a list of dictionaries.

返回类型:

list\[dict\[str, Any\]\]

*class* DeepSeekMultiAgentFormatter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekMultiAgentFormatter)[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter "Link to this definition")

基类：[`TruncatedFormatterBase`](#agentscope.formatter.TruncatedFormatterBase "agentscope.formatter._truncated_formatter_base.TruncatedFormatterBase")

DeepSeek formatter for multi-agent conversations, where more than a user and an agent are involved.

support\_tools\_api*: bool* *\= True*[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter.support_tools_api "Link to this definition")

Whether support tools API

support\_multiagent*: bool* *\= True*[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter.support_multiagent "Link to this definition")

Whether support multi-agent conversations

support\_vision*: bool* *\= False*[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter.support_vision "Link to this definition")

Whether support vision data

supported\_blocks*: list\[type\]* *\= \[<class 'agentscope.message.\_message\_block.TextBlock'>, <class 'agentscope.message.\_message\_block.ToolUseBlock'>, <class 'agentscope.message.\_message\_block.ToolResultBlock'>\]*[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter.supported_blocks "Link to this definition")

The list of supported message blocks

\_\_init\_\_(*conversation\_history\_prompt\='# Conversation History\\nThe content between <history></history> tags contains your conversation history\\n'*, *token\_counter\=None*, *max\_tokens\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekMultiAgentFormatter.__init__)[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter.__init__ "Link to this definition")

Initialize the DeepSeek multi-agent formatter.

参数:

-   **conversation\_history\_prompt** (str) -- The prompt to use for the conversation history section.
    
-   **token\_counter** (TokenCounterBase | None, optional) -- A token counter instance used to count tokens in the messages. If not provided, the formatter will format the messages without considering token limits.
    
-   **max\_tokens** (int | None, optional) -- The maximum number of tokens allowed in the formatted messages. If not provided, the formatter will not truncate the messages.
    

返回类型:

None

*async* \_format\_tool\_sequence(*msgs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekMultiAgentFormatter._format_tool_sequence)[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter._format_tool_sequence "Link to this definition")

Given a sequence of tool call/result messages, format them into the required format for the DeepSeek API.

参数:

**msgs** (list\[Msg\]) -- The list of messages containing tool calls/results to format.

返回:

A list of dictionaries formatted for the DeepSeek API.

返回类型:

list\[dict\[str, Any\]\]

*async* \_format\_agent\_message(*msgs*, *is\_first\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/formatter/_deepseek_formatter.html#DeepSeekMultiAgentFormatter._format_agent_message)[¶](#agentscope.formatter.DeepSeekMultiAgentFormatter._format_agent_message "Link to this definition")

Given a sequence of messages without tool calls/results, format them into the required format for the DeepSeek API.

参数:

-   **msgs** (list\[Msg\]) -- A list of Msg objects to be formatted.
    
-   **is\_first** (bool, defaults to True) -- Whether this is the first agent message in the conversation. If True, the conversation history prompt will be included.
    

返回:

A list of dictionaries formatted for the DeepSeek API.

返回类型:

list\[dict\[str, Any\]\]