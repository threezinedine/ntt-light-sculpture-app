# This data is used for storing the typedef, struct, using which cannot be parsed by the parser
SELF_DEFINED_TYPE: dict[str, str] = {
    "LogCallback": 'Callable[["EngineLogRecord"], None]',
}
