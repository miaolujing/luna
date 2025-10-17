Toggle table of contents sidebar

The pipeline module in AgentScope, that provides syntactic sugar for complex workflows and multi-agent conversations.

*class* MsgHub[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub)[¶](#agentscope.pipeline.MsgHub "Link to this definition")

基类：`object`

MsgHub class that controls the subscription of the participated agents.

示例

In the following example, the reply message from agent1, agent2, and agent3 will be broadcasted to all the other agents in the MsgHub.

```
with MsgHub(participant=[agent1, agent2, agent3]):
    agent1()
    agent2()

```

Actually, it has the same effect as the following code, but much more easy and elegant!

```
x1 = agent1()
agent2.observe(x1)
agent3.observe(x1)

x2 = agent2()
agent1.observe(x2)
agent3.observe(x2)

```

\_\_init\_\_(*participants*, *announcement\=None*, *enable\_auto\_broadcast\=True*, *name\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub.__init__)[¶](#agentscope.pipeline.MsgHub.__init__ "Link to this definition")

Initialize a MsgHub context manager.

参数:

-   **participants** (list\[AgentBase\]) -- A list of agents that participate in the MsgHub.
    
-   **None****)** (*announcement （list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message.Msg")*\]* *|* [*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message.Msg") *|*) -- The message that will be broadcast to all participants when entering the MsgHub.
    
-   **enable\_auto\_broadcast** (bool, defaults to True) -- Whether to enable automatic broadcasting of the replied message from any participant to all other participants. If disabled, the MsgHub will only serve as a manual message broadcaster with the announcement argument and the broadcast() method.
    
-   **name** (str | None) -- The name of this MsgHub. If not provided, a random ID will be generated.
    
-   **announcement** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *|* *list**\[*[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")*\]* *|* *None*)
    

返回类型:

None

add(*new\_participant*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub.add)[¶](#agentscope.pipeline.MsgHub.add "Link to this definition")

Add new participant into this hub

参数:

**new\_participant** (*list**\[*[*AgentBase*](https://doc.agentscope.io/zh_CN/api/agentscope.agent.html#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase")*\]* *|* [*AgentBase*](https://doc.agentscope.io/zh_CN/api/agentscope.agent.html#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase"))

返回类型:

None

delete(*participant*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub.delete)[¶](#agentscope.pipeline.MsgHub.delete "Link to this definition")

Delete agents from participant.

参数:

**participant** (*list**\[*[*AgentBase*](https://doc.agentscope.io/zh_CN/api/agentscope.agent.html#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase")*\]* *|* [*AgentBase*](https://doc.agentscope.io/zh_CN/api/agentscope.agent.html#agentscope.agent.AgentBase "agentscope.agent._agent_base.AgentBase"))

返回类型:

None

*async* broadcast(*msg*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub.broadcast)[¶](#agentscope.pipeline.MsgHub.broadcast "Link to this definition")

Broadcast the message to all participants.

参数:

**msg** (list\[Msg\] | Msg) -- Message(s) to be broadcast among all participants.

返回类型:

None

set\_auto\_broadcast(*enable*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_msghub.html#MsgHub.set_auto_broadcast)[¶](#agentscope.pipeline.MsgHub.set_auto_broadcast "Link to this definition")

Enable automatic broadcasting of the replied message from any participant to all other participants.

参数:

**enable** (bool) -- Whether to enable automatic broadcasting. If disabled, the MsgHub will only serve as a manual message broadcaster with the announcement argument and the broadcast() method.

返回类型:

None

*class* SequentialPipeline[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#SequentialPipeline)[¶](#agentscope.pipeline.SequentialPipeline "Link to this definition")

基类：`object`

An async sequential pipeline class, which executes a sequence of agents sequentially. Compared with functional pipeline, this class can be re-used.

\_\_init\_\_(*agents*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#SequentialPipeline.__init__)[¶](#agentscope.pipeline.SequentialPipeline.__init__ "Link to this definition")

Initialize a sequential pipeline class

参数:

**agents** (list\[AgentBase\]) -- A list of agents.

返回类型:

None

*async* \_\_call\_\_(*msg\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#SequentialPipeline.__call__)[¶](#agentscope.pipeline.SequentialPipeline.__call__ "Link to this definition")

Execute the sequential pipeline

参数:

**msg** (Msg | list\[Msg\] | None, defaults to None) -- The initial input that will be passed to the first agent.

返回类型:

[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") | list\[[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")\] | None

*async* sequential\_pipeline(*agents*, *msg\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_functional.html#sequential_pipeline)[¶](#agentscope.pipeline.sequential_pipeline "Link to this definition")

An async syntactic sugar pipeline that executes a sequence of agents sequentially. The output of the previous agent will be passed as the input to the next agent. The final output will be the output of the last agent.

示例

```
agent1 = ReActAgent(...)
agent2 = ReActAgent(...)
agent3 = ReActAgent(...)

msg_input = Msg("user", "Hello", "user")

msg_output = await sequential_pipeline(
    [agent1, agent2, agent3],
    msg_input
)

```

参数:

-   **agents** (list\[AgentBase\]) -- A list of agents.
    
-   **msg** (Msg | list\[Msg\] | None, defaults to None) -- The initial input that will be passed to the first agent.
    

返回:

The output of the last agent in the sequence.

返回类型:

Msg | list\[Msg\] | None

*class* FanoutPipeline[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#FanoutPipeline)[¶](#agentscope.pipeline.FanoutPipeline "Link to this definition")

基类：`object`

An async fanout pipeline class, which distributes the same input to multiple agents. Compared with functional pipeline, this class can be re-used and configured with default parameters.

\_\_init\_\_(*agents*, *enable\_gather\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#FanoutPipeline.__init__)[¶](#agentscope.pipeline.FanoutPipeline.__init__ "Link to this definition")

Initialize a fanout pipeline class

参数:

-   **agents** (list\[AgentBase\]) -- A list of agents to execute.
    
-   **enable\_gather** (bool, defaults to True) -- Whether to execute agents concurrently using asyncio.gather(). If False, agents are executed sequentially.
    

返回类型:

None

*async* \_\_call\_\_(*msg\=None*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_class.html#FanoutPipeline.__call__)[¶](#agentscope.pipeline.FanoutPipeline.__call__ "Link to this definition")

Execute the fanout pipeline

参数:

-   **msg** (Msg | list\[Msg\] | None, defaults to None) -- The input message that will be distributed to all agents.
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments passed to each agent during execution.
    

返回:

A list of output messages from all agents.

返回类型:

list\[Msg\]

*async* fanout\_pipeline(*agents*, *msg\=None*, *enable\_gather\=True*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/pipeline/_functional.html#fanout_pipeline)[¶](#agentscope.pipeline.fanout_pipeline "Link to this definition")

A fanout pipeline that distributes the same input to multiple agents. This pipeline sends the same message (or a deep copy of it) to all agents and collects their responses. Agents can be executed either concurrently using asyncio.gather() or sequentially depending on the enable\_gather parameter.

示例

```css
agent1 = ReActAgent(...)
agent2 = ReActAgent(...)
agent3 = ReActAgent(...)

msg_input = Msg("user", "Hello", "user")

# Concurrent execution (default)
results = await fanout_pipeline(
    [agent1, agent2, agent3],
    msg_input
)

# Sequential execution
results = await fanout_pipeline(
    [agent1, agent2, agent3],
    msg_input,
    enable_gather=False
)

```

参数:

-   **agents** (list\[AgentBase\]) -- A list of agents.
    
-   **msg** (Msg | list\[Msg\] | None, defaults to None) -- The initial input that will be passed to all agents.
    
-   **enable\_gather** (bool, defaults to True) -- Whether to execute agents concurrently using asyncio.gather(). If False, agents are executed sequentially.
    
-   **\*\*kwargs** (Any) -- Additional keyword arguments passed to each agent during execution.
    

返回:

A list of response messages from each agent.

返回类型:

list\[Msg\]