Toggle table of contents sidebar

The agentscope serialization module

init(*project\=None*, *name\=None*, *logging\_path\=None*, *logging\_level\='INFO'*, *studio\_url\=None*, *tracing\_url\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope.html#init)[¶](#agentscope.init "Link to this definition")

Initialize the agentscope library.

参数:

-   **project** (str | None, optional) -- The project name.
    
-   **name** (str | None, optional) -- The name of the run.
    
-   **logging\_path** (str | None, optional) -- The path to saving the log file. If not provided, logs will not be saved.
    
-   **logging\_level** (str | None, optional) -- The logging level. Defaults to "INFO".
    
-   **studio\_url** (str | None, optional) -- The URL of the AgentScope Studio to connect to.
    
-   **tracing\_url** (str | None, optional) -- The URL of the tracing endpoint, which can connect to third-party OpenTelemetry tracing platforms like Arize-Phoenix and Langfuse. If not provided and studio\_url is provided, it will send traces to the AgentScope Studio's tracing endpoint.
    

返回类型:

None

setup\_logger(*level*, *filepath\=None*)[\[源代码\]](https://doc.agentscope.io/zh_CN/_modules/agentscope/_logging.html#setup_logger)[¶](#agentscope.setup_logger "Link to this definition")

Set up the agentscope logger.

参数:

-   **level** (str) -- The logging level, chosen from "INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL".
    
-   **filepath** (str | None, optional) -- The filepath to save the logging output.
    

返回类型:

None