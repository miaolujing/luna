Toggle table of contents sidebar

The MCP module in AgentScope, that provides fine-grained control over the MCP servers.

*class* MCPToolFunction[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_mcp_function.html#MCPToolFunction)[¶](#agentscope.mcp.MCPToolFunction "Link to this definition")

基类：`object`

An MCP tool function class that can be called directly.

\_\_init\_\_(*mcp\_name*, *tool*, *wrap\_tool\_result*, *client\_gen\=None*, *session\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_mcp_function.html#MCPToolFunction.__init__)[¶](#agentscope.mcp.MCPToolFunction.__init__ "Link to this definition")

Initialize the MCP function.

参数:

-   **mcp\_name** (*str*)
    
-   **tool** (*Tool*)
    
-   **wrap\_tool\_result** (*bool*)
    
-   **client\_gen** (*Callable**\[**\[**...**\]**,* *\_AsyncGeneratorContextManager**\[**Any**\]**\]* *|* *None*)
    
-   **session** (*ClientSession* *|* *None*)
    

返回类型:

None

name*: str*[¶](#agentscope.mcp.MCPToolFunction.name "Link to this definition")

The name of the tool function.

description*: str*[¶](#agentscope.mcp.MCPToolFunction.description "Link to this definition")

The description of the tool function.

json\_schema*: dict\[str, Any\]*[¶](#agentscope.mcp.MCPToolFunction.json_schema "Link to this definition")

JSON schema of the tool function

*async* \_\_call\_\_(*\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_mcp_function.html#MCPToolFunction.__call__)[¶](#agentscope.mcp.MCPToolFunction.__call__ "Link to this definition")

Call the MCP tool function with the given arguments, and return the result.

参数:

**kwargs** (*Any*)

返回类型:

*CallToolResult* | [*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*class* MCPClientBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_client_base.html#MCPClientBase)[¶](#agentscope.mcp.MCPClientBase "Link to this definition")

基类：`object`

Base class for MCP clients.

\_\_init\_\_(*name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_client_base.html#MCPClientBase.__init__)[¶](#agentscope.mcp.MCPClientBase.__init__ "Link to this definition")

Initialize the MCP client with a name.

参数:

**name** (str) -- The name to identify the MCP server, which should be unique across the MCP servers.

返回类型:

None

*abstract async* get\_callable\_function(*func\_name*, *wrap\_tool\_result\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_client_base.html#MCPClientBase.get_callable_function)[¶](#agentscope.mcp.MCPClientBase.get_callable_function "Link to this definition")

Get a tool function by its name.

参数:

-   **func\_name** (*str*)
    
-   **wrap\_tool\_result** (*bool*)
    

返回类型:

*Callable*

*class* StatefulClientBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase)[¶](#agentscope.mcp.StatefulClientBase "Link to this definition")

基类：[`MCPClientBase`](#agentscope.mcp.MCPClientBase "agentscope.mcp._client_base.MCPClientBase"), `ABC`

The base class for stateful MCP clients in AgentScope, which maintains the session state across multiple tool calls.

The developers should use connect() and close() methods to manage the client lifecycle.

\_\_init\_\_(*name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase.__init__)[¶](#agentscope.mcp.StatefulClientBase.__init__ "Link to this definition")

Initialize the stateful MCP client.

参数:

**name** (str) -- The name to identify the MCP server, which should be unique across the MCP servers.

返回类型:

None

is\_connected*: bool*[¶](#agentscope.mcp.StatefulClientBase.is_connected "Link to this definition")

If connected to the MCP server

*async* connect()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase.connect)[¶](#agentscope.mcp.StatefulClientBase.connect "Link to this definition")

Connect to MCP server.

返回类型:

None

*async* close()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase.close)[¶](#agentscope.mcp.StatefulClientBase.close "Link to this definition")

Clean up the MCP client resources. You must call this method when your application is done.

返回类型:

None

*async* list\_tools()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase.list_tools)[¶](#agentscope.mcp.StatefulClientBase.list_tools "Link to this definition")

Get all available tools from the server.

返回:

A list of available MCP tools.

返回类型:

mcp.types.ListToolsResult

*async* get\_callable\_function(*func\_name*, *wrap\_tool\_result\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stateful_client_base.html#StatefulClientBase.get_callable_function)[¶](#agentscope.mcp.StatefulClientBase.get_callable_function "Link to this definition")

Get an async tool function from the MCP server by its name, so that you can call it directly, wrap it into your own function, or anyway you like.

备注

Currently, only the text, image, and audio results are supported in this function.

参数:

-   **func\_name** (str) -- The name of the tool function to get.
    
-   **wrap\_tool\_result** (bool) -- Whether to wrap the tool result into agentscope's ToolResponse object. If False, the raw result type mcp.types.CallToolResult will be returned.
    

返回:

A callable async function that returns either mcp.types.CallToolResult or ToolResponse when called.

返回类型:

MCPToolFunction

*class* StdIOStatefulClient[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stdio_stateful_client.html#StdIOStatefulClient)[¶](#agentscope.mcp.StdIOStatefulClient "Link to this definition")

基类：[`StatefulClientBase`](#agentscope.mcp.StatefulClientBase "agentscope.mcp._stateful_client_base.StatefulClientBase")

A client class that sets up and manage StdIO MCP server connections, and provides function-level fine-grained control over the MCP servers.

小技巧

The stateful client is recommended for MCP servers that need to maintain session states, e.g. web browsers or other interactive MCP servers.

备注

The stateful client will maintain one session across multiple tool calls, until the client is closed by explicitly calling the close() method.

备注

When multiple StdIOStatefulClient instances are connected, they should be closed following the Last In First Out (LIFO) principle to avoid potential errors. Always close the most recently registered client first, then work backwards to the first one. For more details, please refer to this [issue](https://github.com/modelcontextprotocol/python-sdk/issues/577).

\_\_init\_\_(*name*, *command*, *args\=None*, *env\=None*, *cwd\=None*, *encoding\='utf-8'*, *encoding\_error\_handler\='strict'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_stdio_stateful_client.html#StdIOStatefulClient.__init__)[¶](#agentscope.mcp.StdIOStatefulClient.__init__ "Link to this definition")

Initialize the MCP server with std IO.

参数:

-   **name** (str) -- The name to identify the MCP server, which should be unique across the MCP servers.
    
-   **command** (str) -- The executable to run to start the server.
    
-   **args** (list\[str\] | None, optional) -- Command line arguments to pass to the executable.
    
-   **env** (dict\[str, str\] | None, optional) -- The environment to use when spawning the process.
    
-   **cwd** (str | None, optional) -- The working directory to use when spawning the process.
    
-   **encoding** (str, optional) -- The text encoding used when sending/receiving messages to the server. Defaults to "utf-8".
    
-   **encoding\_error\_handler** (Literal\["strict", "ignore", "replace"\], defaults to "strict") -- The text encoding error handler.
    

返回类型:

None

*class* HttpStatelessClient[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateless_client.html#HttpStatelessClient)[¶](#agentscope.mcp.HttpStatelessClient "Link to this definition")

基类：[`MCPClientBase`](#agentscope.mcp.MCPClientBase "agentscope.mcp._client_base.MCPClientBase")

The sse/streamable HTTP MCP client implementation in AgentScope.

备注

Note this client is stateless, meaning it won't maintain the session state across multiple tool calls. Each tool call will start a new session and close it after the call is done.

stateful*: bool* *\= False*[¶](#agentscope.mcp.HttpStatelessClient.stateful "Link to this definition")

Whether the MCP server is stateful, meaning it will maintain the session state across multiple tool calls, or stateless, meaning it will start a new session for each tool call.

\_\_init\_\_(*name*, *transport*, *url*, *headers\=None*, *timeout\=30*, *sse\_read\_timeout\=300*, *\*\*client\_kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateless_client.html#HttpStatelessClient.__init__)[¶](#agentscope.mcp.HttpStatelessClient.__init__ "Link to this definition")

Initialize the streamable HTTP MCP server.

参数:

-   **name** (str) -- The name to identify the MCP server, which should be unique across the MCP servers.
    
-   **transport** (Literal\["streamable\_http", "sse"\]) -- The transport type of MCP server. Generally, the URL of sse transport should end with /sse, while the streamable HTTP URL ends with /mcp.
    
-   **url** (str) -- The URL of the MCP server.
    
-   **headers** (dict\[str, str\] | None, optional) -- Additional headers to include in the HTTP request.
    
-   **timeout** (float, optional) -- The timeout for the HTTP request in seconds. Defaults to 30.
    
-   **sse\_read\_timeout** (float, optional) -- The timeout for reading Server-Sent Events (SSE) in seconds. Defaults to 300 (5 minutes).
    
-   **\*\*client\_kwargs** (Any) -- The additional keyword arguments to pass to the streamable HTTP client.
    

返回类型:

None

get\_client()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateless_client.html#HttpStatelessClient.get_client)[¶](#agentscope.mcp.HttpStatelessClient.get_client "Link to this definition")

The disposable MCP client object, which is a context manager.

返回类型:

*\_AsyncGeneratorContextManager*\[*Any*\]

*async* get\_callable\_function(*func\_name*, *wrap\_tool\_result\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateless_client.html#HttpStatelessClient.get_callable_function)[¶](#agentscope.mcp.HttpStatelessClient.get_callable_function "Link to this definition")

Get a tool function by its name.

参数:

-   **func\_name** (str) -- The name of the tool function.
    
-   **wrap\_tool\_result** (bool, defaults to True) -- Whether to wrap the tool result into agentscope's ToolResponse object. If False, the raw result type mcp.types.CallToolResult will be returned.
    

返回:

An async tool function that returns either mcp.types.CallToolResult or ToolResponse when called.

返回类型:

Callable\[..., Awaitable\[mcp.types.CallToolResult | ToolResponse\]\]

*async* list\_tools()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateless_client.html#HttpStatelessClient.list_tools)[¶](#agentscope.mcp.HttpStatelessClient.list_tools "Link to this definition")

List all tools available on the MCP server.

返回:

The result containing the list of tools.

返回类型:

mcp.types.ListToolsResult

*class* HttpStatefulClient[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateful_client.html#HttpStatefulClient)[¶](#agentscope.mcp.HttpStatefulClient "Link to this definition")

基类：[`StatefulClientBase`](#agentscope.mcp.StatefulClientBase "agentscope.mcp._stateful_client_base.StatefulClientBase")

The stateful sse/streamable HTTP MCP client implementation in AgentScope.

小技巧

The stateful client is recommended for MCP servers that need to maintain session states, e.g. web browsers or other interactive MCP servers.

备注

The stateful client will maintain one session across multiple tool calls, until the client is closed by explicitly calling the close() method.

备注

When multiple HttpStatefulClient instances are connected, they should be closed following the Last In First Out (LIFO) principle to avoid potential errors. Always close the most recently registered client first, then work backwards to the first one. For more details, please refer to this [issue](https://github.com/modelcontextprotocol/python-sdk/issues/577).

\_\_init\_\_(*name*, *transport*, *url*, *headers\=None*, *timeout\=30*, *sse\_read\_timeout\=300*, *\*\*client\_kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/mcp/_http_stateful_client.html#HttpStatefulClient.__init__)[¶](#agentscope.mcp.HttpStatefulClient.__init__ "Link to this definition")

Initialize the streamable HTTP MCP client.

参数:

-   **name** (str) -- The name to identify the MCP server, which should be unique across the MCP servers.
    
-   **transport** (Literal\["streamable\_http", "sse"\]) -- The transport type of MCP server. Generally, the URL of sse transport should end with /sse, while the streamable HTTP URL ends with /mcp.
    
-   **url** (str) -- The URL to the MCP server.
    
-   **headers** (dict\[str, str\] | None, optional) -- Additional headers to include in the HTTP request.
    
-   **timeout** (float, optional) -- The timeout for the HTTP request in seconds. Defaults to 30.
    
-   **sse\_read\_timeout** (float, optional) -- The timeout for reading Server-Sent Events (SSE) in seconds. Defaults to 300 (5 minutes).
    
-   **\*\*client\_kwargs** (Any) -- The additional keyword arguments to pass to the streamable HTTP client.
    

返回类型:

None