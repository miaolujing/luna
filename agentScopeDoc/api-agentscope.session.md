[Back to top](#)

Toggle table of contents sidebar

The session module in agentscope.

*class* SessionBase[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_session_base.html#SessionBase)[¶](#agentscope.session.SessionBase "Link to this definition")

基类：`object`

The base class for session in agentscope.

\_\_init\_\_(*session\_id*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_session_base.html#SessionBase.__init__)[¶](#agentscope.session.SessionBase.__init__ "Link to this definition")

Initialize the session base class

参数:

**session\_id** (*str*)

返回类型:

None

session\_id*: str*[¶](#agentscope.session.SessionBase.session_id "Link to this definition")

The session id

*abstract async* save\_session\_state(*\*\*state\_modules\_mapping*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_session_base.html#SessionBase.save_session_state)[¶](#agentscope.session.SessionBase.save_session_state "Link to this definition")

Save the session state

参数:

**state\_modules\_mapping** ([*StateModule*](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule"))

返回类型:

None

*abstract async* load\_session\_state(*\*args*, *\*\*kwargs*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_session_base.html#SessionBase.load_session_state)[¶](#agentscope.session.SessionBase.load_session_state "Link to this definition")

Load the session state

参数:

-   **args** (*Any*)
    
-   **kwargs** (*Any*)
    

返回类型:

None

*class* JSONSession[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_json_session.html#JSONSession)[¶](#agentscope.session.JSONSession "Link to this definition")

基类：[`SessionBase`](#agentscope.session.SessionBase "agentscope.session._session_base.SessionBase")

The JSON session class.

\_\_init\_\_(*session\_id*, *save\_dir*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_json_session.html#JSONSession.__init__)[¶](#agentscope.session.JSONSession.__init__ "Link to this definition")

Initialize the JSON session class.

参数:

-   **session\_id** (str) -- The session id.
    
-   **save\_dir** (str) -- The directory to save the session state.
    

返回类型:

None

*property* save\_path*: str*[¶](#agentscope.session.JSONSession.save_path "Link to this definition")

The path to save the session state.

*async* save\_session\_state(*\*\*state\_modules\_mapping*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_json_session.html#JSONSession.save_session_state)[¶](#agentscope.session.JSONSession.save_session_state "Link to this definition")

Load the state dictionary from a JSON file.

参数:

**\*\*state\_modules\_mapping** (dict\[str, StateModule\]) -- A dictionary mapping of state module names to their instances.

返回类型:

None

*async* load\_session\_state(*\*\*state\_modules\_mapping*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/session/_json_session.html#JSONSession.load_session_state)[¶](#agentscope.session.JSONSession.load_session_state "Link to this definition")

Get the state dictionary to be saved to a JSON file.

参数:

**state\_modules\_mapping** (list\[StateModule\]) -- The list of state modules to be loaded.

返回类型:

None