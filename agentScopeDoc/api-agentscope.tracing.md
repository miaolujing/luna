Toggle table of contents sidebar

The tracing interface class in agentscope.

setup\_tracing(*endpoint*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_setup.html#setup_tracing)[¶](#agentscope.tracing.setup_tracing "Link to this definition")

Set up the AgentScope tracing by configuring the endpoint URL.

参数:

**endpoint** (str) -- The endpoint URL for the tracing exporter.

返回类型:

None

trace(*name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace)[¶](#agentscope.tracing.trace "Link to this definition")

A generic tracing decorator for synchronous and asynchronous functions.

参数:

**name** (str) -- The name of the span to be created.

返回:

Returns a decorator that wraps the given function with OpenTelemetry tracing.

返回类型:

Callable

trace\_llm(*func*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace_llm)[¶](#agentscope.tracing.trace_llm "Link to this definition")

Trace the LLM call with OpenTelemetry.

参数:

**func** (Callable) -- The function to be traced, which should be a coroutine that returns either a ChatResponse or an AsyncGenerator of ChatResponse.

返回:

A wrapper function that traces the LLM call and handles input/output and exceptions.

返回类型:

Callable

trace\_reply(*func*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace_reply)[¶](#agentscope.tracing.trace_reply "Link to this definition")

Trace the agent reply call with OpenTelemetry.

参数:

**func** (Callable\[..., Coroutine\[Any, Any, Msg\]\]) -- The agent async reply function to be traced.

返回:

A wrapper function that traces the agent reply call and handles input/output and exceptions.

返回类型:

Callable\[..., Coroutine\[Any, Any, Msg\]\]

trace\_format(*func*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace_format)[¶](#agentscope.tracing.trace_format "Link to this definition")

Trace the format function of the formatter with OpenTelemetry.

参数:

**func** (Callable\[..., Coroutine\[Any, Any, list\[dict\]\]\]) -- The async format function to be traced.

返回:

An async wrapper function that traces the format call and handles input/output and exceptions.

返回类型:

Callable\[..., Coroutine\[Any, Any, list\[dict\]\]\]

trace\_toolkit(*func*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace_toolkit)[¶](#agentscope.tracing.trace_toolkit "Link to this definition")

Trace the toolkit call\_tool\_function method with OpenTelemetry.

参数:

**func** (*Callable**\[**\[**...**\]**,* *Coroutine**\[**Any**,* *Any**,* *AsyncGenerator**\[*[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool.ToolResponse")*,* *None**\]**\]**\]*)

返回类型:

*Callable*\[\[...\], *Coroutine*\[*Any*, *Any*, *AsyncGenerator*\[[ToolResponse](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool.ToolResponse"), None\]\]\]

trace\_embedding(*func*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tracing/_trace.html#trace_embedding)[¶](#agentscope.tracing.trace_embedding "Link to this definition")

Trace the embedding call with OpenTelemetry.

参数:

**func** (*Callable**\[**\[**...**\]**,* *Coroutine**\[**Any**,* *Any**,* [*EmbeddingResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingResponse "agentscope.embedding.EmbeddingResponse")*\]**\]*)

返回类型:

*Callable*\[\[...\], *Coroutine*\[*Any*, *Any*, [EmbeddingResponse](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingResponse "agentscope.embedding.EmbeddingResponse")\]\]