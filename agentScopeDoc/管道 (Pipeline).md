Toggle table of contents sidebar

对于多智能体编排，AgentScope 提供了 `agentscope.pipeline` 模块 作为将智能体链接在一起的语法糖，具体包括

-   **MsgHub**: 用于多个智能体之间消息的广播
    
-   **sequential\_pipeline** 和 **SequentialPipeline**: 以顺序方式执行多个智能体的函数式和类式实现
    
-   **fanout\_pipeline** 和 **FanoutPipeline**: 将相同输入分发给多个智能体的函数式和类式实现
    

```python
import os, asyncio

from agentscope.formatter import DashScopeMultiAgentFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.agent import ReActAgent
from agentscope.pipeline import MsgHub

```

## 使用 MsgHub 进行广播[¶](#msghub "Link to this heading")

`MsgHub` 类是一个 **异步上下文管理器**，它接收一个智能体列表作为其参与者。 当一个参与者生成回复消息时，将通过调用所有其他参与者的 `observe` 方法广播该消息。 这意味着在 `MsgHub` 上下文中，开发者无需手动将回复消息从一个智能体发送到另一个智能体。

这里我们创建四个智能体：Alice、Bob、Charlie 和 David。 然后我们让 Alice、Bob 和 Charlie 通过自我介绍开始一个会议。需要注意的是 David 没有包含在这个会议中。

```python
def create_agent(name: str, age: int, career: str) -> ReActAgent:
    """根据给定信息创建智能体对象。"""
    return ReActAgent(
        name=name,
        sys_prompt=f"你是{name}，一个{age}岁的{career}",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.environ["DASHSCOPE_API_KEY"],
        ),
        formatter=DashScopeMultiAgentFormatter(),
    )


alice = create_agent("Alice", 50, "老师")
bob = create_agent("Bob", 35, "工程师")
charlie = create_agent("Charlie", 28, "设计师")
david = create_agent("David", 30, "开发者")

```

然后我们创建一个 `MsgHub` 上下文，并让他们自我介绍:

提示

`announcement` 中的消息将在进入 `MsgHub` 上下文时广播给所有参与者。

```python
async def example_broadcast_message():
    """使用 MsgHub 广播消息的示例。"""

    # 创建消息中心
    async with MsgHub(
        participants=[alice, bob, charlie],
        announcement=Msg(
            "user",
            "现在请简要介绍一下自己，包括你的姓名、年龄和职业。",
            "user",
        ),
    ) as hub:
        # 无需手动消息传递的群聊
        await alice()
        await bob()
        await charlie()


asyncio.run(example_broadcast_message())

```

Alice: 您好，我叫Alice，今年50岁，是一名教师。很高兴认识您！如果您有任何问题想要了解或讨论，都欢迎随时告诉我。
Alice: 您好，我叫Alice，今年50岁，是一名教师。很高兴认识您！如果您有任何问题想要了解或讨论，都欢迎随时告诉我。
Bob: 您好，Alice！我是Bob，今年35岁，我是一名工程师。很高兴认识您！作为一名教师，您教授的是哪个科目呢？
Charlie: 您好，Alice和Bob！我叫Charlie，今年28岁，是一名设计师。我的工作主要集中在视觉设计方面，包括品牌标识、网页界面以及一些图形材料的设计。很高兴遇到你们两位，我们各自的职业背景都挺有趣的。Alice，您是教哪个年龄段的学生呢？

现在让我们检查 Bob、Charlie 和 David 是否收到了 Alice 的消息。

```
async def check_broadcast_message():
    """检查消息是否正确广播。"""
    user_msg = Msg(
        "user",
        "你知道 Alice 是谁吗，她是做什么的？",
        "user",
    )

    await bob(user_msg)
    await charlie(user_msg)
    await david(user_msg)


asyncio.run(check_broadcast_message())

```

Bob: Alice 是我们对话中的一位老师，今年50岁。她还没有具体提到她教授的科目和学生的年龄段。如果您想了解更多关于她的信息，我可以帮您询问。
Charlie: Alice 是一位50岁的教师。在之前的对话中她提到自己很高兴认识我们，但没有具体说明她教授的科目或学生的年龄段。我刚刚询问了她这个问题，不过她还没有回答。您是想知道她的更多信息吗？如果需要的话，我可以再问一次。
David: Alice这个名字比较常见，没有更多的背景信息很难确定是哪位特定的Alice。如果你能提供更多的细节，比如她的职业、成就或者她所在的领域，我可能能够帮助你找到更多关于她的信息。是否有其他的信息可以分享以便我能更准确地回答你的问题？

现在我们观察到 Bob 和 Charlie 知道 Alice 和她的职业，而 David 对 Alice 一无所知，因为他没有包含在 `MsgHub` 上下文中。

### 动态管理[¶](#id2 "Link to this heading")

此外，`MsgHub` 支持通过以下方法动态管理参与者：

-   `add`: 添加一个或多个智能体作为新参与者
    
-   `delete`: 从参与者中移除一个或多个智能体，他们将不再接收广播消息
    
-   `broadcast`: 向所有当前参与者广播消息
    

```
async with MsgHub(participants=[alice]) as hub:
    # 添加新参与者
    hub.add(david)

    # 移除参与者
    hub.delete(alice)

    # 向所有当前参与者广播
    await hub.broadcast(
        Msg("system", "现在我们开始...", "system"),
    )

```

## 管道[¶](#id3 "Link to this heading")

管道是 AgentScope 中多智能体编排的一种语法糖。

目前，AgentScope 提供了两种主要的管道实现：

1.  **顺序管道 (Sequential Pipeline)**: 按预定义顺序逐个执行智能体
    
2.  **扇出管道 (Fanout Pipeline)**: 将相同输入分发给多个智能体并收集它们的响应
    

### 顺序管道[¶](#id4 "Link to this heading")

顺序管道逐个执行智能体，前一个智能体的输出成为下一个智能体的输入。

例如，以下两个代码片段是等价的：

代码片段 1: 手动消息传递[¶](#id7 "Link to this code")

```
msg = None
msg = await alice(msg)
msg = await bob(msg)
msg = await charlie(msg)
msg = await david(msg)

```

代码片段 2: 使用顺序管道[¶](#id8 "Link to this code")

```
from agentscope.pipeline import sequential_pipeline

msg = await sequential_pipeline(
    # 按顺序执行的智能体列表
    agents=[alice, bob, charlie, david],
    # 第一个输入消息，可以是 None
    msg=None
)

```

### 扇出管道[¶](#id5 "Link to this heading")

扇出管道将相同的输入消息同时分发给多个智能体并收集所有响应。当你想要收集对同一话题的不同观点或专业意见时，这非常有用。

例如，以下两个代码片段是等价的：

代码片段 3: 手动逐个调用智能体[¶](#id9 "Link to this code")

```python
from copy import deepcopy

msgs = []
msg = None
for agent in [alice, bob, charlie, david]:
    msgs.append(await agent(deepcopy(msg)))

```

代码片段 4: 使用扇出管道[¶](#id10 "Link to this code")

```
from agentscope.pipeline import fanout_pipeline

msgs = await fanout_pipeline(
    # 要执行的智能体列表
    agents=[alice, bob, charlie, david],
    # 输入消息，可以是 None
    msg=None,
    enable_gather=False,
)

```

备注

`enable_gather` 参数控制扇出管道的执行模式：

-   `enable_gather=True` (默认): 使用 `asyncio.gather()` **并发** 执行所有智能体。这为 I/O 密集型操作（如 API 调用）提供更好的性能，因为智能体并行运行。
    
-   `enable_gather=False`: 逐个 **顺序** 执行智能体。当你需要确定性的执行顺序或想要避免并发请求压垮外部服务时，这很有用。
    

选择并发执行以获得更好的性能，或选择顺序执行以获得可预测的顺序和资源控制。

小技巧

通过结合 `MsgHub` 和 `sequential_pipeline` 或 `fanout_pipeline`，你可以非常容易地创建更复杂的工作流。

## 高级管道特性[¶](#id6 "Link to this heading")

此外，为了可重用性，我们还提供了基于类的实现：

使用 SequentialPipeline 类[¶](#id11 "Link to this code")

```
 from agentscope.pipeline import SequentialPipeline

 # 创建管道对象
 pipeline = SequentialPipeline(agents=[alice, bob, charlie, david])

 # 调用管道
 msg = await pipeline(msg=None)

 # 使用不同输入复用管道
 msg = await pipeline(msg=Msg("user", "你好！", "user"))

```

使用 FanoutPipeline 类[¶](#id12 "Link to this code")

```css
from agentscope.pipeline import FanoutPipeline

# 创建管道对象
pipeline = FanoutPipeline(agents=[alice, bob, charlie, david])

# 调用管道
msgs = await pipeline(msg=None)

# 使用不同输入复用管道
msgs = await pipeline(msg=Msg("user", "你好！", "user"))

```

**Total running time of the script:** (0 minutes 17.352 seconds)

[Gallery generated by Sphinx-Gallery](https://sphinx-gallery.github.io/)