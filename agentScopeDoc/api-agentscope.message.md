Toggle table of contents sidebar

The message module in agentscope.

*class* TextBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#TextBlock)[¶](#agentscope.message.TextBlock "Link to this definition")

基类：`TypedDict`

The text block.

type*: Required\[Literal\['text'\]\]*[¶](#agentscope.message.TextBlock.type "Link to this definition")

The type of the block

text*: str*[¶](#agentscope.message.TextBlock.text "Link to this definition")

The text content

*class* ThinkingBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ThinkingBlock)[¶](#agentscope.message.ThinkingBlock "Link to this definition")

基类：`TypedDict`

The thinking block.

type*: Required\[Literal\['thinking'\]\]*[¶](#agentscope.message.ThinkingBlock.type "Link to this definition")

The type of the block

thinking*: str*[¶](#agentscope.message.ThinkingBlock.thinking "Link to this definition")

*class* Base64Source[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#Base64Source)[¶](#agentscope.message.Base64Source "Link to this definition")

基类：`TypedDict`

The base64 source

type*: Required\[Literal\['base64'\]\]*[¶](#agentscope.message.Base64Source.type "Link to this definition")

The type of the src, must be base64

media\_type*: Required\[str\]*[¶](#agentscope.message.Base64Source.media_type "Link to this definition")

The media type of the data, e.g. image/jpeg or audio/mpeg

data*: Required\[str\]*[¶](#agentscope.message.Base64Source.data "Link to this definition")

The base64 data, in format of RFC 2397

*class* URLSource[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#URLSource)[¶](#agentscope.message.URLSource "Link to this definition")

基类：`TypedDict`

The URL source

type*: Required\[Literal\['url'\]\]*[¶](#agentscope.message.URLSource.type "Link to this definition")

The type of the src, must be url

url*: Required\[str\]*[¶](#agentscope.message.URLSource.url "Link to this definition")

The URL of the image or audio

*class* ImageBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ImageBlock)[¶](#agentscope.message.ImageBlock "Link to this definition")

基类：`TypedDict`

The image block

type*: Required\[Literal\['image'\]\]*[¶](#agentscope.message.ImageBlock.type "Link to this definition")

The type of the block

source*: Required\[[Base64Source](#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source") | [URLSource](#agentscope.message.URLSource "agentscope.message._message_block.URLSource")\]*[¶](#agentscope.message.ImageBlock.source "Link to this definition")

The src of the image

*class* AudioBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#AudioBlock)[¶](#agentscope.message.AudioBlock "Link to this definition")

基类：`TypedDict`

The audio block

type*: Required\[Literal\['audio'\]\]*[¶](#agentscope.message.AudioBlock.type "Link to this definition")

The type of the block

source*: Required\[[Base64Source](#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source") | [URLSource](#agentscope.message.URLSource "agentscope.message._message_block.URLSource")\]*[¶](#agentscope.message.AudioBlock.source "Link to this definition")

The src of the audio

*class* VideoBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#VideoBlock)[¶](#agentscope.message.VideoBlock "Link to this definition")

基类：`TypedDict`

The video block

type*: Required\[Literal\['video'\]\]*[¶](#agentscope.message.VideoBlock.type "Link to this definition")

The type of the block

source*: Required\[[Base64Source](#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source") | [URLSource](#agentscope.message.URLSource "agentscope.message._message_block.URLSource")\]*[¶](#agentscope.message.VideoBlock.source "Link to this definition")

The src of the audio

*class* ToolUseBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ToolUseBlock)[¶](#agentscope.message.ToolUseBlock "Link to this definition")

基类：`TypedDict`

The tool use block.

type*: Required\[Literal\['tool\_use'\]\]*[¶](#agentscope.message.ToolUseBlock.type "Link to this definition")

The type of the block, must be tool\_use

id*: Required\[str\]*[¶](#agentscope.message.ToolUseBlock.id "Link to this definition")

The identity of the tool call

name*: Required\[str\]*[¶](#agentscope.message.ToolUseBlock.name "Link to this definition")

The name of the tool

input*: Required\[dict\[str, object\]\]*[¶](#agentscope.message.ToolUseBlock.input "Link to this definition")

The input of the tool

*class* ToolResultBlock[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ToolResultBlock)[¶](#agentscope.message.ToolResultBlock "Link to this definition")

基类：`TypedDict`

The tool result block.

type*: Required\[Literal\['tool\_result'\]\]*[¶](#agentscope.message.ToolResultBlock.type "Link to this definition")

The type of the block

id*: Required\[str\]*[¶](#agentscope.message.ToolResultBlock.id "Link to this definition")

The identity of the tool call result

output*: Required\[str | List\[[TextBlock](#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") | [ImageBlock](#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") | [AudioBlock](#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")\]\]*[¶](#agentscope.message.ToolResultBlock.output "Link to this definition")

The output of the tool function

name*: Required\[str\]*[¶](#agentscope.message.ToolResultBlock.name "Link to this definition")

The name of the tool function

*class* Msg[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg)[¶](#agentscope.message.Msg "Link to this definition")

基类：`object`

The message class in agentscope.

\_\_init\_\_(*name*, *content*, *role*, *metadata\=None*, *timestamp\=None*, *invocation\_id\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.__init__)[¶](#agentscope.message.Msg.__init__ "Link to this definition")

Initialize the Msg object.

参数:

-   **name** (str) -- The name of the message sender.
    
-   **content** (str | list\[ContentBlock\]) -- The content of the message.
    
-   **role** (Literal\["user", "assistant", "system"\]) -- The role of the message sender.
    
-   **metadata** (dict\[str, JSONSerializableObject\] | None, optional) -- The metadata of the message, e.g. structured output.
    
-   **timestamp** (str | None, optional) -- The created timestamp of the message. If not given, the timestamp will be set automatically.
    
-   **invocation\_id** (str | None, optional) -- The related API invocation id, if any. This is useful for tracking the message in the context of an API call.
    

返回类型:

None

to\_dict()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.to_dict)[¶](#agentscope.message.Msg.to_dict "Link to this definition")

Convert the message into JSON dict data.

返回类型:

dict

*classmethod* from\_dict(*json\_data*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.from_dict)[¶](#agentscope.message.Msg.from_dict "Link to this definition")

Load a message object from the given JSON data.

参数:

**json\_data** (*dict*)

返回类型:

[*Msg*](#agentscope.message.Msg "agentscope.message._message_base.Msg")

has\_content\_blocks(*block\_type\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.has_content_blocks)[¶](#agentscope.message.Msg.has_content_blocks "Link to this definition")

Check if the message has content blocks of the given type.

参数:

**block\_type** (*Literal**\[**"text"**,* *"tool\_use"**,* *"tool\_result"**,* *"image"**,* *"audio"**,* *"video"**\]* *|* *None**,* *defaults to None*) -- The type of the block to be checked. If None, it will check if there are any content blocks.

返回类型:

bool

get\_text\_content()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.get_text_content)[¶](#agentscope.message.Msg.get_text_content "Link to this definition")

Get the pure text blocks from the message content.

返回类型:

str | None

get\_content\_blocks(*block\_type: Literal\['text'\]*) → List\[[TextBlock](#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")\][\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.get_content_blocks)[¶](#agentscope.message.Msg.get_content_blocks "Link to this definition")

get\_content\_blocks(*block\_type: Literal\['tool\_use'\]*) → List\[[ToolUseBlock](#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock")\]

get\_content\_blocks(*block\_type: Literal\['tool\_result'\]*) → List\[[ToolResultBlock](#agentscope.message.ToolResultBlock "agentscope.message._message_block.ToolResultBlock")\]

get\_content\_blocks(*block\_type: Literal\['image'\]*) → List\[[ImageBlock](#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")\]

get\_content\_blocks(*block\_type: Literal\['audio'\]*) → List\[[AudioBlock](#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")\]

get\_content\_blocks(*block\_type: Literal\['video'\]*) → List\[[VideoBlock](#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")\]

get\_content\_blocks(*block\_type: None \= None*) → List\[[ToolUseBlock](#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock") | [ToolResultBlock](#agentscope.message.ToolResultBlock "agentscope.message._message_block.ToolResultBlock") | [TextBlock](#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") | [ThinkingBlock](#agentscope.message.ThinkingBlock "agentscope.message._message_block.ThinkingBlock") | [ImageBlock](#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") | [AudioBlock](#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock") | [VideoBlock](#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")\]

Get the content in block format. If the content is a string, it will be converted to a text block.

参数:

**block\_type** (Literal\["text", "thinking", "tool\_use", "tool\_result", "image", "audio", "video"\] | None, optional) -- The type of the block to be extracted. If None, all blocks will be returned.

返回:

The content blocks.

返回类型:

List\[ContentBlock\]