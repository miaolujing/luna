Toggle table of contents sidebar

The memory module.

*class* MemoryBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase)[¶](#agentscope.memory.MemoryBase "Link to this definition")

基类：[`StateModule`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The base class for memory in agentscope.

*abstract async* add(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.add)[¶](#agentscope.memory.MemoryBase.add "Link to this definition")

Add items to the memory.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*abstract async* delete(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.delete)[¶](#agentscope.memory.MemoryBase.delete "Link to this definition")

Delete items from the memory.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*abstract async* retrieve(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.retrieve)[¶](#agentscope.memory.MemoryBase.retrieve "Link to this definition")

Retrieve items from the memory.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*abstract async* size()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.size)[¶](#agentscope.memory.MemoryBase.size "Link to this definition")

Get the size of the memory.

返回类型:

int

*abstract async* clear()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.clear)[¶](#agentscope.memory.MemoryBase.clear "Link to this definition")

Clear the memory content.

返回类型:

None

*abstract async* get\_memory(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.get_memory)[¶](#agentscope.memory.MemoryBase.get_memory "Link to this definition")

Get the memory content.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

list\[[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")\]

*abstract* state\_dict()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.state_dict)[¶](#agentscope.memory.MemoryBase.state_dict "Link to this definition")

Get the state dictionary of the memory.

返回类型:

dict

*abstract* load\_state\_dict(*state\_dict*, *strict\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.load_state_dict)[¶](#agentscope.memory.MemoryBase.load_state_dict "Link to this definition")

Load the state dictionary of the memory.

参数:

-   **state\_dict** (*dict*)
    
-   **strict** (*bool*)
    

返回类型:

None

*class* InMemoryMemory[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory)[¶](#agentscope.memory.InMemoryMemory "Link to this definition")

基类：[`MemoryBase`](#agentscope.memory.MemoryBase "agentscope.memory._memory_base.MemoryBase")

The in-memory memory class for storing messages.

\_\_init\_\_()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.__init__)[¶](#agentscope.memory.InMemoryMemory.__init__ "Link to this definition")

Initialize the in-memory memory object.

返回类型:

None

state\_dict()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.state_dict)[¶](#agentscope.memory.InMemoryMemory.state_dict "Link to this definition")

Convert the current memory into JSON data format.

返回类型:

dict

load\_state\_dict(*state\_dict*, *strict\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.load_state_dict)[¶](#agentscope.memory.InMemoryMemory.load_state_dict "Link to this definition")

Load the memory from JSON data.

参数:

-   **state\_dict** (dict) -- The state dictionary to load, which should have a "content" field.
    
-   **strict** (bool, defaults to True) -- If True, raises an error if any key in the module is not found in the state\_dict. If False, skips missing keys.
    

返回类型:

None

*async* size()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.size)[¶](#agentscope.memory.InMemoryMemory.size "Link to this definition")

The size of the memory.

返回类型:

int

*async* retrieve(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.retrieve)[¶](#agentscope.memory.InMemoryMemory.retrieve "Link to this definition")

Retrieve items from the memory.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*async* delete(*index*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.delete)[¶](#agentscope.memory.InMemoryMemory.delete "Link to this definition")

Delete the specified item by index(es).

参数:

**index** (Union\[Iterable, int\]) -- The index to delete.

返回类型:

None

*async* add(*memories*, *allow\_duplicates\=False*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.add)[¶](#agentscope.memory.InMemoryMemory.add "Link to this definition")

Add message into the memory.

参数:

-   **memories** (Union\[list\[Msg\], Msg, None\]) -- The message to add.
    
-   **allow\_duplicates** (bool, defaults to False) -- If allow adding duplicate messages (with the same id) into the memory.
    

返回类型:

None

*async* get\_memory()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.get_memory)[¶](#agentscope.memory.InMemoryMemory.get_memory "Link to this definition")

Get the memory content.

返回类型:

list\[[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")\]

*async* clear()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.clear)[¶](#agentscope.memory.InMemoryMemory.clear "Link to this definition")

Clear the memory content.

返回类型:

None

*class* LongTermMemoryBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase)[¶](#agentscope.memory.LongTermMemoryBase "Link to this definition")

基类：[`StateModule`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The long-term memory base class, which should be a time-series memory management system.

The record\_to\_memory and retrieve\_from\_memory methods are two tool functions for agent to manage the long-term memory voluntarily. You can choose not to implement these two functions.

The record and retrieve methods are for developers to use. For example, retrieving/recording memory at the beginning of each reply, and adding the retrieved memory to the system prompt.

*async* record(*msgs*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.record)[¶](#agentscope.memory.LongTermMemoryBase.record "Link to this definition")

A developer-designed method to record information from the given input message(s) to the long-term memory.

参数:

-   **msgs** (*list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *None**\]*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*async* retrieve(*msg*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.retrieve)[¶](#agentscope.memory.LongTermMemoryBase.retrieve "Link to this definition")

A developer-designed method to retrieve information from the long-term memory based on the given input message(s). The retrieved information will be added to the system prompt of the agent.

参数:

-   **msg** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]* *|* *None*)
    
-   **kwargs** (*Any*)
    

返回类型:

str

*async* record\_to\_memory(*thinking*, *content*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.record_to_memory)[¶](#agentscope.memory.LongTermMemoryBase.record_to_memory "Link to this definition")

Use this function to record important information that you may need later. The target content should be specific and concise, e.g. who, when, where, do what, why, how, etc.

参数:

-   **thinking** (str) -- Your thinking and reasoning about what to record
    
-   **content** (list\[str\]) -- The content to remember, which is a list of strings.
    
-   **kwargs** (*Any*)
    

返回类型:

[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*async* retrieve\_from\_memory(*keywords*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.retrieve_from_memory)[¶](#agentscope.memory.LongTermMemoryBase.retrieve_from_memory "Link to this definition")

Retrieve the memory based on the given keywords.

参数:

-   **keywords** (list\[str\]) -- The keywords to search for in the memory, which should be specific and concise, e.g. the person's name, the date, the location, etc.
    
-   **kwargs** (*Any*)
    

返回:

A list of messages that match the keywords.

返回类型:

list\[Msg\]

*class* Mem0LongTermMemory[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory)[¶](#agentscope.memory.Mem0LongTermMemory "Link to this definition")

基类：[`LongTermMemoryBase`](#agentscope.memory.LongTermMemoryBase "agentscope.memory._long_term_memory_base.LongTermMemoryBase")

A class that implements the LongTermMemoryBase interface using mem0.

\_\_init\_\_(*agent\_name\=None*, *user\_name\=None*, *run\_name\=None*, *model\=None*, *embedding\_model\=None*, *vector\_store\_config\=None*, *mem0\_config\=None*, *default\_memory\_type\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.__init__)[¶](#agentscope.memory.Mem0LongTermMemory.__init__ "Link to this definition")

Initialize the Mem0LongTermMemory instance

参数:

-   **agent\_name** (str | None, optional) -- The name of the agent. Default is None.
    
-   **user\_name** (str | None, optional) -- The name of the user. Default is None.
    
-   **run\_name** (str | None, optional) -- The name of the run/session. Default is None.
    
-   **model** ([*ChatModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase") *|* *None*)
    
-   **embedding\_model** ([*EmbeddingModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingModelBase "agentscope.embedding._embedding_base.EmbeddingModelBase") *|* *None*)
    
-   **vector\_store\_config** (*Any* *|* *None*)
    
-   **mem0\_config** (*Any* *|* *None*)
    
-   **default\_memory\_type** (*str* *|* *None*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

备注

1.  At least one of agent\_name, user\_name, or run\_name is required.
    
2.  During memory recording, these parameters become metadata for the stored memories.
    
3.  During memory retrieval, only memories with matching metadata values will be returned.
    

model (ChatModelBase | None, optional):

The chat model to use for the long-term memory. If mem0\_config is provided, this will override the LLM configuration. If mem0\_config is None, this is required.

embedding\_model (EmbeddingModelBase | None, optional):

The embedding model to use for the long-term memory. If mem0\_config is provided, this will override the embedder configuration. If mem0\_config is None, this is required.

vector\_store\_config (VectorStoreConfig | None, optional):

The vector store config to use for the long-term memory. If mem0\_config is provided, this will override the vector store configuration. If mem0\_config is None and this is not provided, defaults to Qdrant with on\_disk=True.

mem0\_config (MemoryConfig | None, optional):

The mem0 config to use for the long-term memory. If provided, individual model/embedding\_model/vector\_store\_config parameters will override the corresponding configurations in mem0\_config. If None, a new MemoryConfig will be created using the provided parameters.

default\_memory\_type (str | None, optional):

The type of memory to use. Default is None, to create a semantic memory.

抛出:

**ValueError** -- If mem0\_config is None and either model or embedding\_model is None.

参数:

-   **agent\_name** (*str* *|* *None*)
    
-   **user\_name** (*str* *|* *None*)
    
-   **run\_name** (*str* *|* *None*)
    
-   **model** ([*ChatModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase") *|* *None*)
    
-   **embedding\_model** ([*EmbeddingModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingModelBase "agentscope.embedding._embedding_base.EmbeddingModelBase") *|* *None*)
    
-   **vector\_store\_config** (*Any* *|* *None*)
    
-   **mem0\_config** (*Any* *|* *None*)
    
-   **default\_memory\_type** (*str* *|* *None*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*async* record\_to\_memory(*thinking*, *content*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.record_to_memory)[¶](#agentscope.memory.Mem0LongTermMemory.record_to_memory "Link to this definition")

Use this function to record important information that you may need later. The target content should be specific and concise, e.g. who, when, where, do what, why, how, etc.

参数:

-   **thinking** (str) -- Your thinking and reasoning about what to record.
    
-   **content** (list\[str\]) -- The content to remember, which is a list of strings.
    
-   **kwargs** (*Any*)
    

返回类型:

[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*async* retrieve\_from\_memory(*keywords*, *limit\=5*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.retrieve_from_memory)[¶](#agentscope.memory.Mem0LongTermMemory.retrieve_from_memory "Link to this definition")

Retrieve the memory based on the given keywords.

参数:

-   **keywords** (list\[str\]) -- The keywords to search for in the memory, which should be specific and concise, e.g. the person's name, the date, the location, etc.
    
-   **limit** (int, optional) -- The maximum number of memories to retrieve per search.
    
-   **kwargs** (*Any*)
    

返回:

A ToolResponse containing the retrieved memories as JSON text.

返回类型:

ToolResponse

*async* record(*msgs*, *memory\_type\=None*, *infer\=True*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.record)[¶](#agentscope.memory.Mem0LongTermMemory.record "Link to this definition")

Record the content to the long-term memory.

参数:

-   **msgs** (list\[Msg | None\]) -- The messages to record to memory.
    
-   **memory\_type** (str | None, optional) -- The type of memory to use. Default is None, to create a semantic memory. "procedural\_memory" is explicitly used for procedural memories.
    
-   **infer** (bool, optional) -- Whether to infer memory from the content. Default is True.
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments for the mem0 recording.
    

返回类型:

None

*async* retrieve(*msg*, *limit\=5*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.retrieve)[¶](#agentscope.memory.Mem0LongTermMemory.retrieve "Link to this definition")

Retrieve the content from the long-term memory.

参数:

-   **msg** (Msg | list\[Msg\] | None) -- The message to search for in the memory, which should be specific and concise, e.g. the person's name, the date, the location, etc.
    
-   **limit** (int, optional) -- The maximum number of memories to retrieve per search.
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments.
    

返回:

The retrieved memory

返回类型:

str