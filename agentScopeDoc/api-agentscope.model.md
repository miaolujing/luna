The model module.

*class* ChatModelBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase)[¶](#agentscope.model.ChatModelBase "Link to this definition")

基类：`object`

Base class for chat models.

\_\_init\_\_(*model\_name*, *stream*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase.__init__)[¶](#agentscope.model.ChatModelBase.__init__ "Link to this definition")

Initialize the chat model base class.

参数:

-   **model\_name** (str) -- The name of the model
    
-   **stream** (bool) -- Whether the model output is streaming or not
    

返回类型:

None

model\_name*: str*[¶](#agentscope.model.ChatModelBase.model_name "Link to this definition")

The model name

stream*: bool*[¶](#agentscope.model.ChatModelBase.stream "Link to this definition")

Is the model output streaming or not

*abstract async* \_\_call\_\_(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase.__call__)[¶](#agentscope.model.ChatModelBase.__call__ "Link to this definition")

Call self as a function.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") | *AsyncGenerator*\[[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None\]

*class* ChatResponse[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_response.html#ChatResponse)[¶](#agentscope.model.ChatResponse "Link to this definition")

基类：`DictMixin`

The response of chat models.

content*: Sequence\[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") | [ToolUseBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock") | ThinkingBlock\]*[¶](#agentscope.model.ChatResponse.content "Link to this definition")

The content of the chat response, which can include text blocks, tool use blocks, or thinking blocks.

id*: str*[¶](#agentscope.model.ChatResponse.id "Link to this definition")

The unique identifier formatter

created\_at*: str*[¶](#agentscope.model.ChatResponse.created_at "Link to this definition")

When the response was created

\_\_init\_\_(*content*, *id=<factory>*, *created\_at=<factory>*, *type=<factory>*, *usage=<factory>*, *metadata=<factory>*)[¶](#agentscope.model.ChatResponse.__init__ "Link to this definition")

参数:

-   **content** (*Sequence**\[*[*TextBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") *|* [*ToolUseBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock") *|* *ThinkingBlock**\]*)
    
-   **id** (*str*)
    
-   **created\_at** (*str*)
    
-   **type** (*Literal**\[**'chat'**\]*)
    
-   **usage** (*ChatUsage* *|* *None*)
    
-   **metadata** (*str* *|* *int* *|* *float* *|* *bool* *|* *None* *|* *list**\[**JSONSerializableObject**\]* *|* *dict**\[**str**,* *JSONSerializableObject**\]*)
    

返回类型:

None

type*: Literal\['chat'\]*[¶](#agentscope.model.ChatResponse.type "Link to this definition")

The type of the response, which is always 'chat'.

usage*: ChatUsage | None*[¶](#agentscope.model.ChatResponse.usage "Link to this definition")

The usage information of the chat response, if available.

metadata*: str | int | float | bool | None | list\[JSONSerializableObject\] | dict\[str, JSONSerializableObject\]*[¶](#agentscope.model.ChatResponse.metadata "Link to this definition")

The metadata of the chat response

*class* DashScopeChatModel[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel)[¶](#agentscope.model.DashScopeChatModel "Link to this definition")

基类：[`ChatModelBase`](#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The DashScope chat model class, which unifies the Generation and MultimodalConversation APIs into one method.

\_\_init\_\_(*model\_name*, *api\_key*, *stream\=True*, *enable\_thinking\=None*, *generate\_kwargs\=None*, *base\_http\_api\_url\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel.__init__)[¶](#agentscope.model.DashScopeChatModel.__init__ "Link to this definition")

Initialize the DashScope chat model.

参数:

-   **model\_name** (str) -- The model names.
    
-   **api\_key** (str) -- The dashscope API key.
    
-   **stream** (bool) -- The streaming output or not
    
-   **enable\_thinking** (bool | None, optional) -- Enable thinking or not, only support Qwen3, QwQ, DeepSeek-R1. Refer to [DashScope documentation](https://help.aliyun.com/zh/model-studio/deep-thinking) for more details.
    
-   **generate\_kwargs** (dict\[str, JSONSerializableObject\] | None, optional) -- The extra keyword arguments used in DashScope API generation, e.g. temperature, seed.
    
-   **base\_http\_api\_url** (str | None, optional) -- The base URL for DashScope API requests. If not provided, the default base URL from the DashScope SDK will be used.
    

返回类型:

None

*async* \_\_call\_\_(*messages*, *tools\=None*, *tool\_choice\=None*, *structured\_model\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel.__call__)[¶](#agentscope.model.DashScopeChatModel.__call__ "Link to this definition")

Get the response from the dashscope Generation/MultimodalConversation API by the given arguments.

备注

We unify the dashscope generation and multimodal conversation APIs into one method, since they support similar arguments and share the same functionality.

参数:

-   **messages** (list\[dict\[str, Any\]\]) -- A list of dictionaries, where role and content fields are required.
    
-   **tools** (list\[dict\] | None, default None) -- The tools JSON schemas that the model can use.
    
-   **tool\_choice** (Literal\["auto", "none", "any", "required"\] | str | None, default None) --
    
    Controls which (if any) tool is called by the model.
    
    Can be "auto", "none", or specific tool name. For more details, please refer to [https://help.aliyun.com/zh/model-studio/qwen-function-calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)
    
-   **structured\_model** (Type\[BaseModel\] | None, default None) --
    
    A Pydantic BaseModel class that defines the expected structure for the model's output. When provided, the model will be forced to return data that conforms to this schema by automatically converting the BaseModel to a tool function and setting tool\_choice to enforce its usage. This enables structured output generation.
    
    备注
    
    When structured\_model is specified, both tools and tool\_choice parameters are ignored, and the model will only perform structured output generation without calling any other tools.
    
-   **\*\*kwargs** (Any) --
    
    The keyword arguments for DashScope chat completions API, e.g. temperature, max\_tokens, top\_p, etc. Please refer to [DashScope documentation](https://help.aliyun.com/zh/dashscope/developer-reference/api-details) for more detailed arguments.
    

返回类型:

[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") | *AsyncGenerator*\[[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None\]

*class* OpenAIChatModel[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel)[¶](#agentscope.model.OpenAIChatModel "Link to this definition")

基类：[`ChatModelBase`](#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The OpenAI chat model class.

\_\_init\_\_(*model\_name*, *api\_key\=None*, *stream\=True*, *reasoning\_effort\=None*, *organization\=None*, *client\_args\=None*, *generate\_kwargs\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel.__init__)[¶](#agentscope.model.OpenAIChatModel.__init__ "Link to this definition")

Initialize the openai client.

参数:

-   **model\_name** (str, default None) -- The name of the model to use in OpenAI API.
    
-   **api\_key** (str, default None) -- The API key for OpenAI API. If not specified, it will be read from the environment variable OPENAI\_API\_KEY.
    
-   **stream** (bool, default True) -- Whether to use streaming output or not.
    
-   **reasoning\_effort** (Literal\["low", "medium", "high"\] | None, optional) -- Reasoning effort, supported for o3, o4, etc. Please refer to [OpenAI documentation](https://platform.openai.com/docs/guides/reasoning?api-mode=chat) for more details.
    
-   **organization** (str, default None) -- The organization ID for OpenAI API. If not specified, it will be read from the environment variable OPENAI\_ORGANIZATION.
    
-   **client\_args** (dict, default None) -- The extra keyword arguments to initialize the OpenAI client.
    
-   **generate\_kwargs** (dict\[str, JSONSerializableObject\] | None, optional) --
    
    The extra keyword arguments used in OpenAI API generation,
    
    e.g. temperature, seed.
    

返回类型:

None

*async* \_\_call\_\_(*messages*, *tools\=None*, *tool\_choice\=None*, *structured\_model\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel.__call__)[¶](#agentscope.model.OpenAIChatModel.__call__ "Link to this definition")

Get the response from OpenAI chat completions API by the given arguments.

参数:

-   **messages** (list\[dict\]) -- A list of dictionaries, where role and content fields are required, and name field is optional.
    
-   **tools** (list\[dict\], default None) -- The tools JSON schemas that the model can use.
    
-   **tool\_choice** (Literal\["auto", "none", "any", "required"\] | str | None, default None) --
    
    Controls which (if any) tool is called by the model.
    
    Can be "auto", "none", "any", "required", or specific tool name. For more details, please refer to [https://platform.openai.com/docs/api-reference/responses/create#responses\_create-tool\_choice](https://platform.openai.com/docs/api-reference/responses/create#responses_create-tool_choice)
    
-   **structured\_model** (Type\[BaseModel\] | None, default None) --
    
    A Pydantic BaseModel class that defines the expected structure for the model's output. When provided, the model will be forced to return data that conforms to this schema by automatically converting the BaseModel to a tool function and setting tool\_choice to enforce its usage. This enables structured output generation.
    
    备注
    
    When structured\_model is specified, both tools and tool\_choice parameters are ignored, and the model will only perform structured output generation without calling any other tools.
    
    For more details, please refer to the [official document](https://platform.openai.com/docs/guides/structured-outputs)
    
-   **\*\*kwargs** (Any) -- The keyword arguments for OpenAI chat completions API, e.g. temperature, max\_tokens, top\_p, etc. Please refer to the OpenAI API documentation for more details.
    

返回:

The response from the OpenAI chat completions API.

返回类型:

ChatResponse | AsyncGenerator\[ChatResponse, None\]

*class* AnthropicChatModel[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel)[¶](#agentscope.model.AnthropicChatModel "Link to this definition")

基类：[`ChatModelBase`](#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Anthropic model wrapper for AgentScope.

\_\_init\_\_(*model\_name*, *api\_key\=None*, *max\_tokens\=2048*, *stream\=True*, *thinking\=None*, *client\_args\=None*, *generate\_kwargs\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel.__init__)[¶](#agentscope.model.AnthropicChatModel.__init__ "Link to this definition")

Initialize the Anthropic chat model.

参数:

-   **model\_name** (str) -- The model names.
    
-   **api\_key** (str) -- The anthropic API key.
    
-   **stream** (bool) -- The streaming output or not
    
-   **max\_tokens** (int) -- Limit the maximum token count the model can generate.
    
-   **thinking** (dict | None, default None) --
    
    Configuration for Claude's internal reasoning process.
    
    Example of thinking[¶](#id4 "Link to this code")
    
    ```
    {
        "type": "enabled" | "disabled",
        "budget_tokens": 1024
    }
    
    ```
    
-   **client\_args** (dict | None, optional) -- The extra keyword arguments to initialize the Anthropic client.
    
-   **generate\_kwargs** (dict\[str, JSONSerializableObject\] | None, optional) -- The extra keyword arguments used in Gemini API generation, e.g. temperature, seed.
    

返回类型:

None

*async* \_\_call\_\_(*messages*, *tools\=None*, *tool\_choice\=None*, *structured\_model\=None*, *\*\*generate\_kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel.__call__)[¶](#agentscope.model.AnthropicChatModel.__call__ "Link to this definition")

Get the response from Anthropic chat completions API by the given arguments.

参数:

-   **messages** (list\[dict\]) -- A list of dictionaries, where role and content fields are required, and name field is optional.
    
-   **tools** (list\[dict\], default None) --
    
    The tools JSON schemas that in format of:
    
    Example of tools JSON schemas[¶](#id5 "Link to this code")
    
    ```
    [
        {
            "type": "function",
            "function": {
                "name": "xxx",
                "description": "xxx",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "..."
                        },
                        # Add more parameters as needed
                    },
                    "required": ["param1"]
            }
        },
        # More schemas here
    ]
    
    ```
    
-   **tool\_choice** (Literal\["auto", "none", "any", "required"\] | str | None, default None) --
    
    Controls which (if any) tool is called by the model.
    
    Can be "auto", "none", "any", "required", or specific tool name. For more details, please refer to [https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
    
-   **structured\_model** (Type\[BaseModel\] | None, default None) --
    
    A Pydantic BaseModel class that defines the expected structure for the model's output. When provided, the model will be forced to return data that conforms to this schema by automatically converting the BaseModel to a tool function and setting tool\_choice to enforce its usage. This enables structured output generation.
    
    备注
    
    When structured\_model is specified, both tools and tool\_choice parameters are ignored, and the model will only perform structured output generation without calling any other tools.
    
-   **\*\*generate\_kwargs** (Any) -- The keyword arguments for Anthropic chat completions API, e.g. temperature, top\_p, etc. Please refer to the Anthropic API documentation for more details.
    

返回:

The response from the Anthropic chat completions API.

返回类型:

ChatResponse | AsyncGenerator\[ChatResponse, None\]

*class* OllamaChatModel[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel)[¶](#agentscope.model.OllamaChatModel "Link to this definition")

基类：[`ChatModelBase`](#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Ollama chat model class in agentscope.

\_\_init\_\_(*model\_name*, *stream\=False*, *options\=None*, *keep\_alive\='5m'*, *enable\_thinking\=None*, *host\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel.__init__)[¶](#agentscope.model.OllamaChatModel.__init__ "Link to this definition")

Initialize the Ollama chat model.

参数:

-   **model\_name** (str) -- The name of the model.
    
-   **stream** (bool, default True) -- Streaming mode or not.
    
-   **options** (dict, default None) -- Additional parameters to pass to the Ollama API. These can include temperature etc.
    
-   **keep\_alive** (str, default "5m") -- Duration to keep the model loaded in memory. The format is a number followed by a unit suffix (s for seconds, m for minutes , h for hours).
    
-   **enable\_thinking** (bool | None, default None) -- Whether enable thinking or not, only for models such as qwen3, deepseek-r1, etc. For more details, please refer to [https://ollama.com/search?c=thinking](https://ollama.com/search?c=thinking)
    
-   **host** (str | None, default None) -- The host address of the Ollama server. If None, uses the default address (typically [http://localhost:11434](http://localhost:11434/)).
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments to pass to the base chat model class.
    

返回类型:

None

*async* \_\_call\_\_(*messages*, *tools\=None*, *tool\_choice\=None*, *structured\_model\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel.__call__)[¶](#agentscope.model.OllamaChatModel.__call__ "Link to this definition")

Get the response from Ollama chat completions API by the given arguments.

参数:

-   **messages** (list\[dict\]) -- A list of dictionaries, where role and content fields are required, and name field is optional.
    
-   **tools** (list\[dict\], default None) -- The tools JSON schemas that the model can use.
    
-   **tool\_choice** (Literal\["auto", "none", "any", "required"\] | str | None, default None) --
    
    Controls which (if any) tool is called by the model.
    
    Can be "auto", "none", "any", "required", or specific tool name.
    
-   **structured\_model** (Type\[BaseModel\] | None, default None) -- A Pydantic BaseModel class that defines the expected structure for the model's output.
    
-   **\*\*kwargs** (Any) -- The keyword arguments for Ollama chat completions API, e.g. [\`](#id2)think\`etc. Please refer to the Ollama API documentation for more details.
    

返回:

The response from the Ollama chat completions API.

返回类型:

ChatResponse | AsyncGenerator\[ChatResponse, None\]

*class* GeminiChatModel[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel)[¶](#agentscope.model.GeminiChatModel "Link to this definition")

基类：[`ChatModelBase`](#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Google Gemini chat model class in agentscope.

\_\_init\_\_(*model\_name*, *api\_key*, *stream\=True*, *thinking\_config\=None*, *client\_args\=None*, *generate\_kwargs\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel.__init__)[¶](#agentscope.model.GeminiChatModel.__init__ "Link to this definition")

Initialize the Gemini chat model.

参数:

-   **model\_name** (str) -- The name of the Gemini model to use, e.g. "gemini-2.5-flash".
    
-   **api\_key** (str) -- The API key for Google Gemini.
    
-   **stream** (bool, default True) -- Whether to use streaming output or not.
    
-   **thinking\_config** (dict | None, optional) --
    
    Thinking config, supported models are 2.5 Pro, 2.5 Flash, etc. Refer to [https://ai.google.dev/gemini-api/docs/thinking](https://ai.google.dev/gemini-api/docs/thinking) for more details.
    
    Example of thinking\_config[¶](#id6 "Link to this code")
    
    ```
    {
        "include_thoughts": True, # enable thoughts or not
        "thinking_budget": 1024   # Max tokens for reasoning
    }
    
    ```
    
-   **client\_args** (dict, default None) -- The extra keyword arguments to initialize the OpenAI client.
    
-   **generate\_kwargs** (dict\[str, JSONSerializableObject\] | None, optional) -- The extra keyword arguments used in Gemini API generation, e.g. temperature, seed.
    

返回类型:

None

*async* \_\_call\_\_(*messages*, *tools\=None*, *tool\_choice\=None*, *structured\_model\=None*, *\*\*config\_kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel.__call__)[¶](#agentscope.model.GeminiChatModel.__call__ "Link to this definition")

Call the Gemini model with the provided arguments.

参数:

-   **messages** (list\[dict\[str, Any\]\]) -- A list of dictionaries, where role and content fields are required.
    
-   **tools** (list\[dict\] | None, default None) -- The tools JSON schemas that the model can use.
    
-   **tool\_choice** (Literal\["auto", "none", "any", "required"\] | str | None, default None) --
    
    Controls which (if any) tool is called by the model.
    
    Can be "auto", "none", "any", "required", or specific tool name. For more details, please refer to [https://ai.google.dev/gemini-api/docs/function-calling?hl=en&example=meeting#function\_calling\_modes](https://ai.google.dev/gemini-api/docs/function-calling?hl=en&example=meeting#function_calling_modes)
    
-   **structured\_model** (Type\[BaseModel\] | None, default None) --
    
    A Pydantic BaseModel class that defines the expected structure for the model's output.
    
    备注
    
    When structured\_model is specified, both tools and tool\_choice parameters are ignored, and the model will only perform structured output generation without calling any other tools.
    
    For more details, please refer to
    
    [https://ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)
    
-   **\*\*config\_kwargs** (Any) -- The keyword arguments for Gemini chat completions API.
    

返回类型:

[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") | *AsyncGenerator*\[[*ChatResponse*](#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None\]