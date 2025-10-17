The agent base class.

*class* AgentBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase)[¶](#agentscope.agent.AgentBase "Link to this definition")

基类：[`StateModule`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

Base class for asynchronous agents.

supported\_hook\_types*: list\[str\]* *\= \['pre\_reply', 'post\_reply', 'pre\_print', 'post\_print', 'pre\_observe', 'post\_observe'\]*[¶](#agentscope.agent.AgentBase.supported_hook_types "Link to this definition")

Supported hook types for the agent base class.

\_\_init\_\_()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.__init__)[¶](#agentscope.agent.AgentBase.__init__ "Link to this definition")

Initialize the agent.

返回类型:

None

id*: str*[¶](#agentscope.agent.AgentBase.id "Link to this definition")

The agent's unique identifier, generated using shortuuid.

*async* observe(*msg*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.observe)[¶](#agentscope.agent.AgentBase.observe "Link to this definition")

Receive the given message(s) without generating a reply.

参数:

**msg** (Msg | list\[Msg\] | None) -- The message(s) to be observed.

返回类型:

None

*async* reply(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.reply)[¶](#agentscope.agent.AgentBase.reply "Link to this definition")

The main logic of the agent, which generates a reply based on the current state and input arguments.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

*async* print(*msg*, *last\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.print)[¶](#agentscope.agent.AgentBase.print "Link to this definition")

The function to display the message.

参数:

-   **msg** (Msg) -- The message object to be printed.
    
-   **last** (bool, defaults to True) -- Whether this is the last one in streaming messages. For non-streaming message, this should always be True.
    

返回类型:

None

*async* \_\_call\_\_(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.__call__)[¶](#agentscope.agent.AgentBase.__call__ "Link to this definition")

Call the reply function with the given arguments.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

*async* handle\_interrupt(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.handle_interrupt)[¶](#agentscope.agent.AgentBase.handle_interrupt "Link to this definition")

The post-processing logic when the reply is interrupted by the user or something else.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

*async* interrupt(*msg\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.interrupt)[¶](#agentscope.agent.AgentBase.interrupt "Link to this definition")

Interrupt the current reply process.

参数:

**msg** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]* *|* *None*)

返回类型:

None

register\_instance\_hook(*hook\_type*, *hook\_name*, *hook*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.register_instance_hook)[¶](#agentscope.agent.AgentBase.register_instance_hook "Link to this definition")

Register a hook to the agent instance, which only takes effect for the current instance.

参数:

-   **hook\_type** (str) -- The type of the hook, indicating where the hook is to be triggered.
    
-   **hook\_name** (str) -- The name of the hook. If the name is already registered, the hook will be overwritten.
    
-   **hook** (Callable) -- The hook function.
    

返回类型:

None

remove\_instance\_hook(*hook\_type*, *hook\_name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.remove_instance_hook)[¶](#agentscope.agent.AgentBase.remove_instance_hook "Link to this definition")

Remove an instance-level hook from the agent instance.

参数:

-   **hook\_type** (AgentHookTypes) -- The type of the hook, indicating where the hook is to be triggered.
    
-   **hook\_name** (str) -- The name of the hook to remove.
    

返回类型:

None

*classmethod* register\_class\_hook(*hook\_type*, *hook\_name*, *hook*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.register_class_hook)[¶](#agentscope.agent.AgentBase.register_class_hook "Link to this definition")

The universal function to register a hook to the agent class, which will take effect for all instances of the class.

参数:

-   **hook\_type** (AgentHookTypes) -- The type of the hook, indicating where the hook is to be triggered.
    
-   **hook\_name** (str) -- The name of the hook. If the name is already registered, the hook will be overwritten.
    
-   **hook** (Callable) -- The hook function.
    

返回类型:

None

*classmethod* remove\_class\_hook(*hook\_type*, *hook\_name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.remove_class_hook)[¶](#agentscope.agent.AgentBase.remove_class_hook "Link to this definition")

Remove a class-level hook from the agent class.

参数:

-   **hook\_type** (AgentHookTypes) -- The type of the hook, indicating where the hook is to be triggered.
    
-   **hook\_name** (str) -- The name of the hook to remove.
    

返回类型:

None

*classmethod* clear\_class\_hooks(*hook\_type\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.clear_class_hooks)[¶](#agentscope.agent.AgentBase.clear_class_hooks "Link to this definition")

Clear all class-level hooks.

参数:

**hook\_type** (AgentHookTypes, optional) -- The type of the hook to clear. If not specified, all class-level hooks will be cleared.

返回类型:

None

clear\_instance\_hooks(*hook\_type\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.clear_instance_hooks)[¶](#agentscope.agent.AgentBase.clear_instance_hooks "Link to this definition")

If hook\_type is not specified, clear all instance-level hooks. Otherwise, clear the specified type of instance-level hooks.

参数:

**hook\_type** (*str* *|* *Literal**\[**'pre\_reply'**,* *'post\_reply'**,* *'pre\_print'**,* *'post\_print'**,* *'pre\_observe'**,* *'post\_observe'**\]* *|* *None*)

返回类型:

None

reset\_subscribers(*msghub\_name*, *subscribers*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.reset_subscribers)[¶](#agentscope.agent.AgentBase.reset_subscribers "Link to this definition")

Reset the subscribers of the agent.

参数:

-   **msghub\_name** (str) -- The name of the MsgHub that manages the subscribers.
    
-   **subscribers** (list\[AgentBase\]) -- A list of agents that will receive the reply message from this agent via their observe method.
    

返回类型:

None

remove\_subscribers(*msghub\_name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.remove_subscribers)[¶](#agentscope.agent.AgentBase.remove_subscribers "Link to this definition")

Remove the msghub subscribers by the given msg hub name.

参数:

**msghub\_name** (str) -- The name of the MsgHub that manages the subscribers.

返回类型:

None

disable\_console\_output()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_agent_base.html#AgentBase.disable_console_output)[¶](#agentscope.agent.AgentBase.disable_console_output "Link to this definition")

This function will disable the console output of the agent, e.g. in a production environment to avoid messy logs.

返回类型:

None

*class* ReActAgentBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent_base.html#ReActAgentBase)[¶](#agentscope.agent.ReActAgentBase "Link to this definition")

基类：[`AgentBase`](#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase")

The ReAct agent base class.

To support ReAct algorithm, this class extends the AgentBase class by adding two abstract interfaces: reasoning and acting, while supporting hook functions at four positions: pre-reasoning, post-reasoning, pre-acting, and post-acting by the \_ReActAgentMeta metaclass.

supported\_hook\_types*: list\[str\]* *\= \['pre\_reply', 'post\_reply', 'pre\_print', 'post\_print', 'pre\_observe', 'post\_observe', 'pre\_reasoning', 'post\_reasoning', 'pre\_acting', 'post\_acting'\]*[¶](#agentscope.agent.ReActAgentBase.supported_hook_types "Link to this definition")

Supported hook types for the agent base class.

\_\_init\_\_()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent_base.html#ReActAgentBase.__init__)[¶](#agentscope.agent.ReActAgentBase.__init__ "Link to this definition")

Initialize the ReAct agent base class.

返回类型:

None

*class* ReActAgent[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent)[¶](#agentscope.agent.ReActAgent "Link to this definition")

基类：[`ReActAgentBase`](#agentscope.agent.ReActAgentBase "agentscope.agent._react_agent_base.ReActAgentBase")

A ReAct agent implementation in AgentScope, which supports

-   Realtime steering
    
-   API-based (parallel) tool calling
    
-   Hooks around reasoning, acting, reply, observe and print functions
    
-   Structured output generation
    

finish\_function\_name*: str* *\= 'generate\_response'*[¶](#agentscope.agent.ReActAgent.finish_function_name "Link to this definition")

The function name used to finish replying and return a response to the user.

\_\_init\_\_(*name*, *sys\_prompt*, *model*, *formatter*, *toolkit\=None*, *memory\=None*, *long\_term\_memory\=None*, *long\_term\_memory\_mode\='both'*, *enable\_meta\_tool\=False*, *parallel\_tool\_calls\=False*, *max\_iters\=10*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent.__init__)[¶](#agentscope.agent.ReActAgent.__init__ "Link to this definition")

Initialize the ReAct agent

参数:

-   **name** (str) -- The name of the agent.
    
-   **sys\_prompt** (str) -- The system prompt of the agent.
    
-   **model** (ChatModelBase) -- The chat model used by the agent.
    
-   **formatter** (FormatterBase) -- The formatter used to format the messages into the required format of the model API provider.
    
-   **toolkit** (Toolkit | None, optional) -- A Toolkit object that contains the tool functions. If not provided, a default empty Toolkit will be created.
    
-   **memory** (MemoryBase | None, optional) -- The memory used to store the dialogue history. If not provided, a default InMemoryMemory will be created, which stores messages in a list in memory.
    
-   **long\_term\_memory** (LongTermMemoryBase | None, optional) -- The optional long-term memory, which will provide two tool functions: retrieve\_from\_memory and record\_to\_memory, and will attach the retrieved information to the system prompt before each reply.
    
-   **enable\_meta\_tool** (bool, defaults to False) -- If True, a meta tool function reset\_equipped\_tools will be added to the toolkit, which allows the agent to manage its equipped tools dynamically.
    
-   **long\_term\_memory\_mode** (Literal\['agent\_control', 'static\_control', 'both'\], defaults to both) -- The mode of the long-term memory. If agent\_control, two tool functions retrieve\_from\_memory and record\_to\_memory will be registered in the toolkit to allow the agent to manage the long-term memory. If static\_control, retrieving and recording will happen in the beginning and end of each reply respectively.
    
-   **parallel\_tool\_calls** (bool, defaults to False) -- When LLM generates multiple tool calls, whether to execute them in parallel.
    
-   **max\_iters** (int, defaults to 10) -- The maximum number of iterations of the reasoning-acting loops.
    

返回类型:

None

*property* sys\_prompt*: str*[¶](#agentscope.agent.ReActAgent.sys_prompt "Link to this definition")

The dynamic system prompt of the agent.

*async* reply(*msg\=None*, *structured\_model\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent.reply)[¶](#agentscope.agent.ReActAgent.reply "Link to this definition")

Generate a reply based on the current state and input arguments.

参数:

-   **msg** (Msg | list\[Msg\] | None, optional) -- The input message(s) to the agent.
    
-   **structured\_model** (Type\[BaseModel\] | None, optional) -- The required structured output model. If provided, the agent is expected to generate structured output in the metadata field of the output message.
    

返回:

The output message generated by the agent.

返回类型:

Msg

*async* observe(*msg*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent.observe)[¶](#agentscope.agent.ReActAgent.observe "Link to this definition")

Receive observing message(s) without generating a reply.

参数:

**msg** (Msg | list\[Msg\] | None) -- The message or messages to be observed.

返回类型:

None

*async* handle\_interrupt(*\_msg\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent.handle_interrupt)[¶](#agentscope.agent.ReActAgent.handle_interrupt "Link to this definition")

The post-processing logic when the reply is interrupted by the user or something else.

参数:

**\_msg** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]* *|* *None*)

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

generate\_response(*response*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_react_agent.html#ReActAgent.generate_response)[¶](#agentscope.agent.ReActAgent.generate_response "Link to this definition")

Generate a response. Note only the input argument response is visible to the others, you should include all the necessary information in the response argument.

参数:

-   **response** (str) -- Your response to the user.
    
-   **kwargs** (*Any*)
    

返回类型:

[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*class* UserInputData[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#UserInputData)[¶](#agentscope.agent.UserInputData "Link to this definition")

基类：`object`

The user input data.

blocks\_input*: List\[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") | [ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") | [AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock") | [VideoBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")\]* *\= None*[¶](#agentscope.agent.UserInputData.blocks_input "Link to this definition")

The text input from the user

structured\_input*: dict\[str, Any\] | None* *\= None*[¶](#agentscope.agent.UserInputData.structured_input "Link to this definition")

The structured input from the user

\_\_init\_\_(*blocks\_input\=None*, *structured\_input\=None*)[¶](#agentscope.agent.UserInputData.__init__ "Link to this definition")

参数:

-   **blocks\_input** (*List**\[*[*TextBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") *|* [*ImageBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") *|* [*AudioBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock") *|* [*VideoBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")*\]* *|* *None*)
    
-   **structured\_input** (*dict**\[**str**,* *Any**\]* *|* *None*)
    

返回类型:

None

*class* UserInputBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#UserInputBase)[¶](#agentscope.agent.UserInputBase "Link to this definition")

基类：`object`

The base class used to handle the user input from different sources.

*abstract async* \_\_call\_\_(*agent\_id*, *agent\_name*, *\*args*, *structured\_model\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#UserInputBase.__call__)[¶](#agentscope.agent.UserInputBase.__call__ "Link to this definition")

The user input method, which returns the user input and the required structured data.

参数:

-   **agent\_id** (str) -- The agent identifier.
    
-   **agent\_name** (str) -- The agent name.
    
-   **structured\_model** (Type\[BaseModel\] | None, optional) -- A base model class that defines the structured input format.
    
-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回:

The user input data.

返回类型:

UserInputData

*class* TerminalUserInput[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#TerminalUserInput)[¶](#agentscope.agent.TerminalUserInput "Link to this definition")

基类：[`UserInputBase`](#agentscope.agent.UserInputBase "agentscope.agent._user_input.UserInputBase")

The terminal user input.

\_\_init\_\_(*input\_hint\='User Input: '*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#TerminalUserInput.__init__)[¶](#agentscope.agent.TerminalUserInput.__init__ "Link to this definition")

Initialize the terminal user input with a hint.

参数:

**input\_hint** (*str*)

返回类型:

None

*async* \_\_call\_\_(*agent\_id*, *agent\_name*, *\*args*, *structured\_model\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#TerminalUserInput.__call__)[¶](#agentscope.agent.TerminalUserInput.__call__ "Link to this definition")

Handle the user input from the terminal.

参数:

-   **agent\_id** (str) -- The agent identifier.
    
-   **agent\_name** (str) -- The agent name.
    
-   **structured\_model** (Type\[BaseModel\] | None, optional) -- A base model class that defines the structured input format.
    
-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回:

The user input data.

返回类型:

UserInputData

*class* StudioUserInput[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#StudioUserInput)[¶](#agentscope.agent.StudioUserInput "Link to this definition")

基类：[`UserInputBase`](#agentscope.agent.UserInputBase "agentscope.agent._user_input.UserInputBase")

The class that host the user input on the AgentScope Studio.

\_\_init\_\_(*studio\_url*, *run\_id*, *max\_retries\=3*, *reconnect\_attempts\=3*, *reconnection\_delay\=1*, *reconnection\_delay\_max\=5*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#StudioUserInput.__init__)[¶](#agentscope.agent.StudioUserInput.__init__ "Link to this definition")

Initialize the StudioUserInput object.

参数:

-   **studio\_url** (str) -- The URL of the AgentScope Studio.
    
-   **run\_id** (str) -- The current run identity.
    
-   **max\_retries** (int, defaults to 3) -- The maximum number of retries to get user input.
    
-   **reconnect\_attempts** (*int*)
    
-   **reconnection\_delay** (*int*)
    
-   **reconnection\_delay\_max** (*int*)
    

返回类型:

None

*async* \_\_call\_\_(*agent\_id*, *agent\_name*, *\*args*, *structured\_model\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_input.html#StudioUserInput.__call__)[¶](#agentscope.agent.StudioUserInput.__call__ "Link to this definition")

Get the user input from AgentScope Studio.

参数:

-   **agent\_id** (str) -- The identity of the agent.
    
-   **agent\_name** (str) -- The name of the agent.
    
-   **structured\_model** (Type\[BaseModel\] | None, optional) -- The base model class of the structured input.
    
-   **args** (*Any*)
    

抛出:

**RuntimeError** -- Failed to get user input from AgentScope Studio.

返回:

The user input.

返回类型:

UserInputData

*class* UserAgent[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent)[¶](#agentscope.agent.UserAgent "Link to this definition")

基类：[`AgentBase`](#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase")

The class for user interaction, allowing developers to handle the user input from different sources, such as web UI, cli, and other interfaces.

\_\_init\_\_(*name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.__init__)[¶](#agentscope.agent.UserAgent.__init__ "Link to this definition")

Initialize the user agent with a name.

参数:

**name** (*str*)

返回类型:

None

*async* reply(*msg\=None*, *structured\_model\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.reply)[¶](#agentscope.agent.UserAgent.reply "Link to this definition")

Receive input message(s) and generate a reply message from the user.

参数:

-   **msg** (Msg | list\[Msg\] | None, defaults to None) -- The message(s) to be replied. If None, the agent will wait for user input.
    
-   **structured\_model** (Type\[BaseModel\] | None, defaults to None) -- A child class of pydantic.BaseModel that defines the structured output format. If provided, the user will be prompted to fill in the required fields.
    

返回:

The reply message generated by the user.

返回类型:

Msg

override\_instance\_input\_method(*input\_method*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.override_instance_input_method)[¶](#agentscope.agent.UserAgent.override_instance_input_method "Link to this definition")

Override the input method of the current UserAgent instance.

参数:

**input\_method** (UserInputBase) -- The callable input method, which should be an object of a class that inherits from UserInputBase.

返回类型:

None

*classmethod* override\_class\_input\_method(*input\_method*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.override_class_input_method)[¶](#agentscope.agent.UserAgent.override_class_input_method "Link to this definition")

Override the input method of the current UserAgent class.

参数:

**input\_method** (UserInputBase) -- The callable input method, which should be an object of a class that inherits from UserInputBase.

返回类型:

None

*async* handle\_interrupt(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.handle_interrupt)[¶](#agentscope.agent.UserAgent.handle_interrupt "Link to this definition")

The post-processing logic when the reply is interrupted by the user or something else.

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

*async* observe(*msg*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/agent/_user_agent.html#UserAgent.observe)[¶](#agentscope.agent.UserAgent.observe "Link to this definition")

Observe the message(s) from the other agents or the environment.

参数:

**msg** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]* *|* *None*)

返回类型:

None