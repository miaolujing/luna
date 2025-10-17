[Back to top](#)

Toggle table of contents sidebar

The exception module in agentscope.

*exception* AgentOrientedExceptionBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/exception/_exception_base.html#AgentOrientedExceptionBase)[¶](#agentscope.exception.AgentOrientedExceptionBase "Link to this definition")

基类：`Exception`

The base class for all agent-oriented exceptions. These exceptions are expect to the captured and exposed to the agent during runtime, so that agents can handle the error appropriately during the runtime.

\_\_init\_\_(*message*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/exception/_exception_base.html#AgentOrientedExceptionBase.__init__)[¶](#agentscope.exception.AgentOrientedExceptionBase.__init__ "Link to this definition")

Initialize the exception with a message.

参数:

**message** (*str*)

*exception* ToolInterruptedError[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/exception/_tool.html#ToolInterruptedError)[¶](#agentscope.exception.ToolInterruptedError "Link to this definition")

基类：[`AgentOrientedExceptionBase`](#agentscope.exception.AgentOrientedExceptionBase "agentscope.exception._exception_base.AgentOrientedExceptionBase")

Exception raised when a tool calling was interrupted by the user.

*exception* ToolNotFoundError[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/exception/_tool.html#ToolNotFoundError)[¶](#agentscope.exception.ToolNotFoundError "Link to this definition")

基类：[`AgentOrientedExceptionBase`](#agentscope.exception.AgentOrientedExceptionBase "agentscope.exception._exception_base.AgentOrientedExceptionBase")

Exception raised when a tool was not found.

*exception* ToolInvalidArgumentsError[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/exception/_tool.html#ToolInvalidArgumentsError)[¶](#agentscope.exception.ToolInvalidArgumentsError "Link to this definition")

基类：[`AgentOrientedExceptionBase`](#agentscope.exception.AgentOrientedExceptionBase "agentscope.exception._exception_base.AgentOrientedExceptionBase")

Exception raised when the arguments passed to a tool are invalid.