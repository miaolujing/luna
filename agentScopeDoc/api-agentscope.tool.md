The tool module in agentscope.

*class* Toolkit[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit)[¶](#agentscope.tool.Toolkit "Link to this definition")

基类：[`StateModule`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The class that supports both function- and group-level tool management.

Use the following methods to manage the tool functions:

-   register\_tool\_function
    
-   remove\_tool\_function
    

For group-level management:

-   create\_tool\_group
    
-   update\_tool\_groups
    
-   remove\_tool\_groups
    

MCP related methods:

-   register\_mcp\_server
    
-   remove\_mcp\_servers
    

To run the tool functions or get the data from the activated tools:

-   call\_tool\_function
    
-   get\_json\_schemas
    
-   get\_tool\_group\_notes
    

\_\_init\_\_()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.__init__)[¶](#agentscope.tool.Toolkit.__init__ "Link to this definition")

Initialize the toolkit.

返回类型:

None

create\_tool\_group(*group\_name*, *description*, *active\=False*, *notes\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.create_tool_group)[¶](#agentscope.tool.Toolkit.create_tool_group "Link to this definition")

Create a tool group to organize tool functions

参数:

-   **group\_name** (str) -- The name of the tool group.
    
-   **description** (str) -- The description of the tool group.
    
-   **active** (bool, defaults to False) -- If the group is active, meaning the tool functions in this group are included in the JSON schema.
    
-   **notes** (str | None, optional) -- The notes used to remind the agent how to use the tool functions properly, which can be combined into the system prompt.
    

返回类型:

None

update\_tool\_groups(*group\_names*, *active*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.update_tool_groups)[¶](#agentscope.tool.Toolkit.update_tool_groups "Link to this definition")

Update the activation status of the given tool groups.

参数:

-   **group\_names** (list\[str\]) -- The list of tool group names to be updated.
    
-   **active** (bool) -- If the tool groups should be activated or deactivated.
    

返回类型:

None

remove\_tool\_groups(*group\_names*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_tool_groups)[¶](#agentscope.tool.Toolkit.remove_tool_groups "Link to this definition")

Remove tool functions from the toolkit by their group names.

参数:

**group\_names** (str | list\[str\]) -- The group names to be removed from the toolkit.

返回类型:

None

register\_tool\_function(*tool\_func*, *group\_name\='basic'*, *preset\_kwargs\=None*, *func\_description\=None*, *json\_schema\=None*, *include\_long\_description\=True*, *include\_var\_positional\=False*, *include\_var\_keyword\=False*, *postprocess\_func\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.register_tool_function)[¶](#agentscope.tool.Toolkit.register_tool_function "Link to this definition")

Register a tool function to the toolkit.

参数:

-   **tool\_func** (ToolFunction) -- The tool function, which can be async or sync, streaming or not-streaming, but the response must be a ToolResponse object.
    
-   **group\_name** (str | Literal\["basic"\], defaults to "basic") -- The belonging group of the tool function. Tools in "basic" group is always included in the JSON schema, while the others are only included when their group is active.
    
-   **preset\_kwargs** (dict\[str, JSONSerializableObject\] | None, optional) -- Preset arguments by the user, which will not be included in the JSON schema, nor exposed to the agent.
    
-   **func\_description** (str | None, optional) -- The function description. If not provided, the description will be extracted from the docstring automatically.
    
-   **json\_schema** (dict | None, optional) -- Manually provided JSON schema for the tool function, which should be {"type": "function", "function": {"name": "function\_name": "xx", "description": "xx", "parameters": {...}}}
    
-   **include\_long\_description** (bool, defaults to True) -- When extracting function description from the docstring, if the long description will be included.
    
-   **include\_var\_positional** (bool, defaults to False) -- Whether to include the variable positional arguments (\*args) in the function schema.
    
-   **include\_var\_keyword** (bool, defaults to False) -- Whether to include the variable keyword arguments (\*\*kwargs) in the function schema.
    
-   **postprocess\_func** (Callable\[\[ToolUseBlock, ToolResponse\], ToolResponse | None\] | None, optional) -- A post-processing function that will be called after the tool function is executed, taking the tool call block and tool response as arguments. If it returns None, the tool result will be returned as is. If it returns a ToolResponse, the returned block will be used as the final tool result.
    

返回类型:

None

remove\_tool\_function(*tool\_name*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_tool_function)[¶](#agentscope.tool.Toolkit.remove_tool_function "Link to this definition")

Remove tool function from the toolkit by its name.

参数:

**tool\_name** (str) -- The name of the tool function to be removed.

返回类型:

None

get\_json\_schemas()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.get_json_schemas)[¶](#agentscope.tool.Toolkit.get_json_schemas "Link to this definition")

Get the JSON schemas from the tool functions that belong to the active groups.

备注

The preset keyword arguments is removed from the JSON schema, and the extended model is applied if it is set.

示例

Example of tool function JSON schemas[¶](#id1 "Link to this code")

```
[
    {
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "Search on Google.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    ...
]

```

返回:

A list of function JSON schemas.

返回类型:

list\[dict\]

set\_extended\_model(*func\_name*, *model*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.set_extended_model)[¶](#agentscope.tool.Toolkit.set_extended_model "Link to this definition")

Set the extended model for a tool function, so that the original JSON schema will be extended.

参数:

-   **func\_name** (str) -- The name of the tool function.
    
-   **model** (Union\[Type\[BaseModel\], None\]) -- The extended model to be set.
    

返回类型:

None

*async* remove\_mcp\_clients(*client\_names*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_mcp_clients)[¶](#agentscope.tool.Toolkit.remove_mcp_clients "Link to this definition")

Remove tool functions from the MCP clients by their names.

参数:

**client\_names** (list\[str\]) -- The names of the MCP client, which used to initialize the client instance.

返回类型:

None

*async* call\_tool\_function(*tool\_call*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.call_tool_function)[¶](#agentscope.tool.Toolkit.call_tool_function "Link to this definition")

Execute the tool function by the ToolUseBlock and return the tool response chunk in unified streaming mode, i.e. an async generator of ToolResponse objects.

备注

The tool response chunk is **accumulated**.

参数:

**tool\_call** (ToolUseBlock) -- A tool call block.

生成器:

ToolResponse -- The tool response chunk, in accumulative manner.

返回类型:

*AsyncGenerator*\[[*ToolResponse*](#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse"), None\]

*async* register\_mcp\_client(*mcp\_client*, *group\_name\='basic'*, *enable\_funcs\=None*, *disable\_funcs\=None*, *preset\_kwargs\_mapping\=None*, *postprocess\_func\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.register_mcp_client)[¶](#agentscope.tool.Toolkit.register_mcp_client "Link to this definition")

Register tool functions from an MCP client.

参数:

-   **mcp\_client** (MCPClientBase) -- The MCP client instance to connect to the MCP server.
    
-   **group\_name** (str, defaults to "basic") -- The group name that the tool functions will be added to.
    
-   **enable\_funcs** (list\[str\] | None, optional) -- The functions to be added into the toolkit. If None, all tool functions within the MCP servers will be added.
    
-   **disable\_funcs** (list\[str\] | None, optional) -- The functions that will be filtered out. If None, no tool functions will be filtered out.
    
-   **preset\_kwargs\_mapping** (*dict**\[**str**,* *dict**\[**str**,* *Any**\]**\]* *|* *None*) -- (Optional\[dict\[str, dict\[str, Any\]\]\], defaults to None): The preset keyword arguments mapping, whose keys are the tool function names and values are the preset keyword arguments.
    
-   **postprocess\_func** (Callable\[\[ToolUseBlock, ToolResponse\], ToolResponse | None\] | None, optional) -- A post-processing function that will be called after the tool function is executed, taking the tool call block and tool response as arguments. If it returns None, the tool result will be returned as is. If it returns a ToolResponse, the returned block will be used as the final tool result.
    

返回类型:

None

state\_dict()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.state_dict)[¶](#agentscope.tool.Toolkit.state_dict "Link to this definition")

Get the state dictionary of the toolkit.

返回:

A dictionary containing the active tool group names.

返回类型:

dict\[str, Any\]

load\_state\_dict(*state\_dict*, *strict\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.load_state_dict)[¶](#agentscope.tool.Toolkit.load_state_dict "Link to this definition")

Load the state dictionary into the toolkit.

参数:

-   **state\_dict** (dict) -- The state dictionary to load, which should have "active\_groups" key and its value must be a list of group names.
    
-   **strict** (bool, defaults to True) -- If True, raises an error if any key in the module is not found in the state\_dict. If False, skips missing keys.
    

返回类型:

None

get\_activated\_notes()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.get_activated_notes)[¶](#agentscope.tool.Toolkit.get_activated_notes "Link to this definition")

Get the notes from the active tool groups, which can be used to construct the system prompt for the agent.

返回:

The combined notes from the active tool groups.

返回类型:

str

reset\_equipped\_tools(*\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.reset_equipped_tools)[¶](#agentscope.tool.Toolkit.reset_equipped_tools "Link to this definition")

Choose appropriate tools to equip yourself with, so that you can finish your task. Each argument in this function represents a group of related tools, and the value indicates whether to activate the group or not. Besides, the tool response of this function will contain the precaution notes for using them, which you **MUST pay attention to and follow**. You can also reuse this function to check the notes of the tool groups.

Note this function will reset the tools, so that the original tools will be removed first.

参数:

**kwargs** (*Any*)

返回类型:

[*ToolResponse*](#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

clear()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.clear)[¶](#agentscope.tool.Toolkit.clear "Link to this definition")

Clear the toolkit, removing all tool functions and groups.

返回类型:

None

*class* ToolResponse[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_response.html#ToolResponse)[¶](#agentscope.tool.ToolResponse "Link to this definition")

基类：`object`

The result chunk of a tool call.

content*: List\[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") | [ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") | [AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")\]*[¶](#agentscope.tool.ToolResponse.content "Link to this definition")

The execution output of the tool function.

metadata*: dict | None* *\= None*[¶](#agentscope.tool.ToolResponse.metadata "Link to this definition")

The metadata to be accessed within the agent, so that we don't need to parse the tool result block.

stream*: bool* *\= False*[¶](#agentscope.tool.ToolResponse.stream "Link to this definition")

Whether the tool output is streamed.

\_\_init\_\_(*content*, *metadata=None*, *stream=False*, *is\_last=True*, *is\_interrupted=False*, *id=<factory>*)[¶](#agentscope.tool.ToolResponse.__init__ "Link to this definition")

参数:

-   **content** (*List**\[*[*TextBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock") *|* [*ImageBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock") *|* [*AudioBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")*\]*)
    
-   **metadata** (*dict* *|* *None*)
    
-   **stream** (*bool*)
    
-   **is\_last** (*bool*)
    
-   **is\_interrupted** (*bool*)
    
-   **id** (*str*)
    

返回类型:

None

is\_last*: bool* *\= True*[¶](#agentscope.tool.ToolResponse.is_last "Link to this definition")

Whether this is the last response in a stream tool execution.

is\_interrupted*: bool* *\= False*[¶](#agentscope.tool.ToolResponse.is_interrupted "Link to this definition")

Whether the tool execution is interrupted.

id*: str*[¶](#agentscope.tool.ToolResponse.id "Link to this definition")

The identity of the tool response.

*async* execute\_python\_code(*code*, *timeout\=300*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_coding/_python.html#execute_python_code)[¶](#agentscope.tool.execute_python_code "Link to this definition")

Execute the given python code in a temp file and capture the return code, standard output and error. Note you must print the output to get the result, and the tmp file will be removed right after the execution.

参数:

-   **code** (str) -- The Python code to be executed.
    
-   **timeout** (float, defaults to 300) -- The maximum time (in seconds) allowed for the code to run.
    
-   **kwargs** (*Any*)
    

返回:

The response containing the return code, standard output, and standard error of the executed code.

返回类型:

ToolResponse

*async* execute\_shell\_command(*command*, *timeout\=300*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_coding/_shell.html#execute_shell_command)[¶](#agentscope.tool.execute_shell_command "Link to this definition")

Execute given command and return the return code, standard output and error within <returncode></returncode>, <stdout></stdout> and <stderr></stderr> tags.

参数:

-   **command** (str) -- The shell command to execute.
    
-   **timeout** (float, defaults to 300) -- The maximum time (in seconds) allowed for the command to run.
    
-   **kwargs** (*Any*)
    

返回:

The tool response containing the return code, standard output, and standard error of the executed command.

返回类型:

ToolResponse

*async* view\_text\_file(*file\_path*, *ranges\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_view_text_file.html#view_text_file)[¶](#agentscope.tool.view_text_file "Link to this definition")

View the file content in the specified range with line numbers. If ranges is not provided, the entire file will be returned.

参数:

-   **file\_path** (str) -- The target file path.
    
-   **ranges** (*list**\[**int**\]* *|* *None*) -- The range of lines to be viewed (e.g. lines 1 to 100: \[1, 100\]), inclusive. If not provided, the entire file will be returned. To view the last 100 lines, use \[-100, -1\].
    

返回:

The tool response containing the file content or an error message.

返回类型:

ToolResponse

*async* write\_text\_file(*file\_path*, *content*, *ranges\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_write_text_file.html#write_text_file)[¶](#agentscope.tool.write_text_file "Link to this definition")

Create/Replace/Overwrite content in a text file. When ranges is provided, the content will be replaced in the specified range. Otherwise, the entire file (if exists) will be overwritten.

参数:

-   **file\_path** (str) -- The target file path.
    
-   **content** (str) -- The content to be written.
    
-   **ranges** (list\[int\] | None, defaults to None) -- The range of lines to be replaced. If None, the entire file will be overwritten.
    

返回:

The tool response containing the result of the writing operation.

返回类型:

ToolResponse

*async* insert\_text\_file(*file\_path*, *content*, *line\_number*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_write_text_file.html#insert_text_file)[¶](#agentscope.tool.insert_text_file "Link to this definition")

Insert the content at the specified line number in a text file.

参数:

-   **file\_path** (str) -- The target file path.
    
-   **content** (str) -- The content to be inserted.
    
-   **line\_number** (int) -- The line number at which the content should be inserted, starting from 1. If exceeds the number of lines in the file, it will be appended to the end of the file.
    

返回:

The tool response containing the result of the insertion operation.

返回类型:

ToolResponse

dashscope\_text\_to\_image(*prompt*, *api\_key*, *n\=1*, *size\='1024\*1024'*, *model\='wanx-v1'*, *use\_base64\=False*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_text_to_image)[¶](#agentscope.tool.dashscope_text_to_image "Link to this definition")

Generate image(s) based on the given prompt, and return image url(s) or base64 data.

参数:

-   **prompt** (str) -- The text prompt to generate image.
    
-   **api\_key** (str) -- The api key for the dashscope api.
    
-   **n** (int, defaults to 1) -- The number of images to generate.
    
-   **size** (Literal\["1024\*1024", "720\*1280", "1280\*720"\], defaults to "1024\*1024") -- Size of the image.
    
-   **model** (str, defaults to '"wanx-v1"') -- The model to use, such as "wanx-v1", "qwen-image", "wan2.2-t2i-flash", etc.
    
-   **use\_base64** (bool, defaults to 'False') -- Whether to use base64 data for images.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

dashscope\_text\_to\_audio(*text*, *api\_key*, *model\='sambert-zhichu-v1'*, *sample\_rate\=48000*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_text_to_audio)[¶](#agentscope.tool.dashscope_text_to_audio "Link to this definition")

Convert the given text to audio.

参数:

-   **text** (str) -- The text to be converted into audio.
    
-   **api\_key** (str) -- The api key for the dashscope API.
    
-   **model** (str, defaults to 'sambert-zhichu-v1') -- The model to use. Full model list can be found in the [official document](https://help.aliyun.com/zh/model-studio/sambert-python-sdk).
    
-   **sample\_rate** (int, defaults to 48000) -- Sample rate of the audio.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

dashscope\_image\_to\_text(*image\_urls*, *api\_key*, *prompt\='Describe the image'*, *model\='qwen-vl-plus'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_image_to_text)[¶](#agentscope.tool.dashscope_image_to_text "Link to this definition")

Generate text based on the given images.

参数:

-   **image\_urls** (str | Sequence\[str\]) -- The url of single or multiple images.
    
-   **api\_key** (str) -- The api key for the dashscope api.
    
-   **prompt** (str, defaults to 'Describe the image') -- The text prompt.
    
-   **model** (str, defaults to 'qwen-vl-plus') -- The model to use in DashScope MultiModal API.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_text\_to\_image(*prompt*, *api\_key*, *n\=1*, *model\='dall-e-2'*, *size\='256x256'*, *quality\='auto'*, *style\='vivid'*, *response\_format\='url'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_text_to_image)[¶](#agentscope.tool.openai_text_to_image "Link to this definition")

Generate image(s) based on the given prompt, and return image URL(s) or base64 data.

参数:

-   **prompt** (str) -- The text prompt to generate images.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **n** (int, defaults to 1) -- The number of images to generate.
    
-   **model** (Literal\["dall-e-2", "dall-e-3"\], defaults to "dall-e-2") -- The model to use for image generation.
    
-   **size** (Literal\["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"\], defaults to "256x256") -- The size of the generated images. Must be one of 1024x1024, 1536x1024 (landscape), 1024x1536 ( portrait), or auto (default value) for gpt-image-1, one of 256x256, 512x512, or 1024x1024 for dall-e-2, and one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3.
    
-   **quality** (Literal\["auto", "standard", "hd", "high", "medium", "low"\], defaults to "auto") --
    
    The quality of the image that will be generated.
    
    -   auto (default value) will automatically select the best quality for the given model.
        
    -   high, medium and low are supported for gpt-image-1.
        
    -   hd and standard are supported for dall-e-3.
        
    -   standard is the only option for dall-e-2.
        
-   **style** (Literal\["vivid", "natural"\], defaults to "vivid") --
    
    The style of the generated images. This parameter is only supported for dall-e-3. Must be one of vivid or natural.
    
    -   Vivid causes the model to lean towards generating hyper-real and dramatic images.
        
    -   Natural causes the model to produce more natural, less hyper-real looking images.
        
-   **response\_format** (Literal\["url", "b64\_json"\], defaults to "url") --
    
    The format in which generated images with dall-e-2 and dall-e-3 are returned.
    
    -   Must be one of "url" or "b64\_json".
        
    -   URLs are only valid for 60 minutes after the image has been generated.
        
    -   This parameter isn't supported for gpt-image-1 which will always return base64-encoded images.
        

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_text\_to\_audio(*text*, *api\_key*, *model\='tts-1'*, *voice\='alloy'*, *speed\=1.0*, *res\_format\='mp3'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_text_to_audio)[¶](#agentscope.tool.openai_text_to_audio "Link to this definition")

Convert text to an audio file using a specified model and voice.

参数:

-   **text** (str) -- The text to convert to audio.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **model** (Literal\["tts-1", "tts-1-hd"\], defaults to "tts-1") -- The model to use for text-to-speech conversion.
    
-   **voice** (Literal\["alloy", "echo", "fable", "onyx", "nova", "shimmer"\], defaults to "alloy") -- The voice to use for the audio output.
    
-   **speed** (float, defaults to 1.0) -- The speed of the audio playback. A value of 1.0 is normal speed.
    
-   **res\_format** (Literal\["mp3", "wav", "opus", "aac", "flac", "wav", "pcm"\], defaults to "mp3") -- The format of the audio file.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_edit\_image(*image\_url*, *prompt*, *api\_key*, *model\='dall-e-2'*, *mask\_url\=None*, *n\=1*, *size\='256x256'*, *response\_format\='url'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_edit_image)[¶](#agentscope.tool.openai_edit_image "Link to this definition")

Edit an image based on the provided mask and prompt, and return the edited image URL(s) or base64 data.

参数:

-   **image\_url** (str) -- The file path or URL to the image that needs editing.
    
-   **prompt** (str) -- The text prompt describing the edits to be made to the image.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **model** (Literal\["dall-e-2", "gpt-image-1"\], defaults to "dall-e-2") -- The model to use for image generation.
    
-   **mask\_url** (str | None, defaults to None) -- The file path or URL to the mask image that specifies the regions to be edited.
    
-   **n** (int, defaults to 1) -- The number of edited images to generate.
    
-   **size** (Literal\["256x256", "512x512", "1024x1024"\], defaults to "256x256") -- The size of the edited images.
    
-   **response\_format** (Literal\["url", "b64\_json"\], defaults to "url") --
    
    The format in which generated images are returned.
    
    -   Must be one of "url" or "b64\_json".
        
    -   URLs are only valid for 60 minutes after generation.
        
    -   This parameter isn't supported for gpt-image-1 which will always return base64-encoded images.
        

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_create\_image\_variation(*image\_url*, *api\_key*, *n\=1*, *model\='dall-e-2'*, *size\='256x256'*, *response\_format\='url'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_create_image_variation)[¶](#agentscope.tool.openai_create_image_variation "Link to this definition")

Create variations of an image and return the image URL(s) or base64 data.

参数:

-   **image\_url** (str) -- The file path or URL to the image from which variations will be generated.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **n** (int, defaults to 1) -- The number of image variations to generate.
    
-   **model** (\` Literal\["dall-e-2"\]\`, default to dall-e-2) -- The model to use for image variation.
    
-   **size** (Literal\["256x256", "512x512", "1024x1024"\], defaults to "256x256") -- The size of the generated image variations.
    
-   **response\_format** (Literal\["url", "b64\_json"\], defaults to "url") --
    
    The format in which generated images are returned.
    
    -   Must be one of url or b64\_json.
        
    -   URLs are only valid for 60 minutes after the image has been generated.
        

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_image\_to\_text(*image\_urls*, *api\_key*, *prompt\='Describe the image'*, *model\='gpt-4o'*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_image_to_text)[¶](#agentscope.tool.openai_image_to_text "Link to this definition")

Generate descriptive text for given image(s) using a specified model, and return the generated text.

参数:

-   **image\_urls** (str | list\[str\]) -- The URL or list of URLs pointing to the images that need to be described.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **prompt** (str, defaults to "Describe the image") -- The prompt that instructs the model on how to describe the image(s).
    
-   **model** (str, defaults to "gpt-4o") -- The model to use for generating the text descriptions.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse

openai\_audio\_to\_text(*audio\_file\_url*, *api\_key*, *language\='en'*, *temperature\=0.2*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_audio_to_text)[¶](#agentscope.tool.openai_audio_to_text "Link to this definition")

Convert an audio file to text using OpenAI's transcription service.

参数:

-   **audio\_file\_url** (str) -- The file path or URL to the audio file that needs to be transcribed.
    
-   **api\_key** (str) -- The API key for the OpenAI API.
    
-   **language** (str, defaults to "en") -- The language of the input audio in [ISO-639-1 format](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g., "en", "zh", "fr"). Improves accuracy and latency.
    
-   **temperature** (float, defaults to 0.2) -- The temperature for the transcription, which affects the randomness of the output.
    

返回:

A ToolResponse containing the generated content (ImageBlock/TextBlock/AudioBlock) or error information if the operation failed.

返回类型:

ToolResponse