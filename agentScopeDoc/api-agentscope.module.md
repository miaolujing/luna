Toggle table of contents sidebar

The module in agentscope.

*class* StateModule[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/module/_state_module.html#StateModule)[¶](#agentscope.module.StateModule "Link to this definition")

基类：`object`

The state module class in agentscope to support nested state serialization and deserialization.

\_\_init\_\_()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/module/_state_module.html#StateModule.__init__)[¶](#agentscope.module.StateModule.__init__ "Link to this definition")

Initialize the state module.

返回类型:

None

state\_dict()[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/module/_state_module.html#StateModule.state_dict)[¶](#agentscope.module.StateModule.state_dict "Link to this definition")

Get the state dictionary of the module, including the nested state modules and registered attributes.

返回:

A dictionary that keys are attribute names and values are the state of the attribute.

返回类型:

dict

load\_state\_dict(*state\_dict*, *strict\=True*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/module/_state_module.html#StateModule.load_state_dict)[¶](#agentscope.module.StateModule.load_state_dict "Link to this definition")

Load the state dictionary into the module.

参数:

-   **state\_dict** (dict) -- The state dictionary to load.
    
-   **strict** (bool, defaults to True) -- If True, raises an error if any key in the module is not found in the state\_dict. If False, skips missing keys.
    

返回类型:

None

register\_state(*attr\_name*, *custom\_to\_json\=None*, *custom\_from\_json\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/module/_state_module.html#StateModule.register_state)[¶](#agentscope.module.StateModule.register_state "Link to this definition")

Register an attribute to be tracked as a state variable.

参数:

-   **attr\_name** (str) -- The name of the attribute to register.
    
-   **custom\_to\_json** (Callable\[\[Any\], JSONSerializableObject\] | None, optional) -- A custom function to convert the attribute to a JSON-serializable format. If not provided, json.dumps will be used.
    
-   **custom\_from\_json** (Callable\[\[JSONSerializableObject\], Any\] | None , defaults to None) -- A custom function to convert the JSON dictionary back to the original attribute format.
    

返回类型:

None