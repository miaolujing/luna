Toggle table of contents sidebar

The token module in agentscope

*class* TokenCounterBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_token_base.html#TokenCounterBase)[¶](#agentscope.token.TokenCounterBase "Link to this definition")

基类：`object`

The base class for token counting.

*abstract async* count(*messages*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_token_base.html#TokenCounterBase.count)[¶](#agentscope.token.TokenCounterBase.count "Link to this definition")

Count the number of tokens by the given model and messages.

参数:

-   **messages** (*list**\[**dict**\]*)
    
-   **kwargs** (*Any*)
    

返回类型:

int

*class* GeminiTokenCounter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_gemini_token_counter.html#GeminiTokenCounter)[¶](#agentscope.token.GeminiTokenCounter "Link to this definition")

基类：[`TokenCounterBase`](#agentscope.token.TokenCounterBase "agentscope.token._token_base.TokenCounterBase")

The Gemini token counter class.

\_\_init\_\_(*model\_name*, *api\_key*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_gemini_token_counter.html#GeminiTokenCounter.__init__)[¶](#agentscope.token.GeminiTokenCounter.__init__ "Link to this definition")

Initialize the Gemini token counter.

参数:

-   **model\_name** (str) -- The name of the Gemini model to use, e.g. "gemini-2.5-flash".
    
-   **api\_key** (str) -- The API key for Google Gemini.
    
-   **\*\*kwargs** -- Additional keyword arguments that will be passed to the Gemini client.
    

返回类型:

None

*async* count(*messages*, *tools\=None*, *\*\*config\_kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_gemini_token_counter.html#GeminiTokenCounter.count)[¶](#agentscope.token.GeminiTokenCounter.count "Link to this definition")

Count the number of tokens of gemini models.

参数:

-   **messages** (*list**\[**dict**\]*)
    
-   **tools** (*list**\[**dict**\]* *|* *None*)
    
-   **config\_kwargs** (*Any*)
    

返回类型:

int

*class* OpenAITokenCounter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_openai_token_counter.html#OpenAITokenCounter)[¶](#agentscope.token.OpenAITokenCounter "Link to this definition")

基类：[`TokenCounterBase`](#agentscope.token.TokenCounterBase "agentscope.token._token_base.TokenCounterBase")

The OpenAI token counting class.

\_\_init\_\_(*model\_name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_openai_token_counter.html#OpenAITokenCounter.__init__)[¶](#agentscope.token.OpenAITokenCounter.__init__ "Link to this definition")

Initialize the OpenAI token counter.

参数:

**model\_name** (str) -- The name of the OpenAI model to use for token counting.

返回类型:

None

*async* count(*messages*, *tools\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_openai_token_counter.html#OpenAITokenCounter.count)[¶](#agentscope.token.OpenAITokenCounter.count "Link to this definition")

Count the token numbers of the given messages.

备注

OpenAI hasn't provided an official guide for counting tokens with tools. If you have any ideas, please open an issue on our GitHub repository.

参数:

-   **messages** (list\[dict\[str, Any\]\]) -- A list of dictionaries, where role and content fields are required.
    
-   **tools** (list\[dict\], defaults to None)
    
-   **kwargs** (*Any*)
    

返回类型:

int

*class* AnthropicTokenCounter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_anthropic_token_counter.html#AnthropicTokenCounter)[¶](#agentscope.token.AnthropicTokenCounter "Link to this definition")

基类：`object`

The Anthropic token counter class.

\_\_init\_\_(*model\_name*, *api\_key*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_anthropic_token_counter.html#AnthropicTokenCounter.__init__)[¶](#agentscope.token.AnthropicTokenCounter.__init__ "Link to this definition")

Initialize the Anthropic token counter.

参数:

-   **model\_name** (str) -- The name of the Anthropic model to use, e.g. "claude-2".
    
-   **api\_key** (str) -- The API key for Anthropic.
    
-   **kwargs** (*Any*)
    

返回类型:

None

*async* count(*messages*, *tools\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_anthropic_token_counter.html#AnthropicTokenCounter.count)[¶](#agentscope.token.AnthropicTokenCounter.count "Link to this definition")

Count the number of tokens for the given messages

备注

The Anthropic token counting API requires the multimodal data to be in base64 format,

参数:

-   **messages** (list\[dict\]) -- A list of dictionaries, where role and content fields are required.
    
-   **tools** (list\[dict\] | None, defaults to None) -- The tools JSON schemas that the model can use.
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments for the token counting API.
    

返回类型:

int

*class* HuggingFaceTokenCounter[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_huggingface_token_counter.html#HuggingFaceTokenCounter)[¶](#agentscope.token.HuggingFaceTokenCounter "Link to this definition")

基类：[`TokenCounterBase`](#agentscope.token.TokenCounterBase "agentscope.token._token_base.TokenCounterBase")

The token counter for Huggingface models.

\_\_init\_\_(*pretrained\_model\_name\_or\_path*, *use\_mirror\=False*, *use\_fast\=False*, *trust\_remote\_code\=False*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_huggingface_token_counter.html#HuggingFaceTokenCounter.__init__)[¶](#agentscope.token.HuggingFaceTokenCounter.__init__ "Link to this definition")

Initialize the huggingface token counter.

参数:

-   **pretrained\_model\_name\_or\_path** (str) -- The name or path of the pretrained model, which will be used to download the tokenizer from Huggingface Hub.
    
-   **use\_mirror** (bool, defaults to False) -- Whether to enable the HuggingFace mirror, which is useful for users in China.
    
-   **use\_fast** (bool, defaults to False) -- The argument that will be passed to the tokenizer.
    
-   **trust\_remote\_code** (bool, defaults to False) -- The argument that will be passed to the tokenizer.
    
-   **\*\*kwargs** -- Additional keyword arguments that will be passed to the tokenizer.
    

返回类型:

None

*async* count(*messages*, *tools\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/token/_huggingface_token_counter.html#HuggingFaceTokenCounter.count)[¶](#agentscope.token.HuggingFaceTokenCounter.count "Link to this definition")

Count the number of tokens with the tokenizer download from HuggingFace hub.

参数:

-   **messages** (list\[dict\]) -- A list of message dictionaries
    
-   **tools** (list\[dict\] | None, defaults to None) -- The JSON schema of the tools, which will also be involved in the token counting.
    
-   **\*\*kwargs** (Any) -- The additional keyword arguments that will be passed to the tokenizer, e.g. chat\_template, padding, etc.
    

返回类型:

int