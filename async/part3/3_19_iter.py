import inspect

entities = []

functions = []
func_coro = []
func_gen = []
async_func_gen = []
ob_coro = []
ob_gen = []
ob_async_gen = []


for entity in entities:
    if inspect.iscoroutine(entity):
        ob_coro.append(entity)
    elif inspect.isgenerator(entity):
        ob_gen.append(entity)
    elif inspect.isasyncgen(entity):
        ob_async_gen.append(entity)
    elif inspect.isroutine(entity):
        if inspect.isgeneratorfunction(entity):
            func_gen.append(entity)
        elif inspect.iscoroutinefunction(entity):
            func_coro.append(entity)
        elif inspect.isasyncgenfunction(entity):
            async_func_gen.append(entity)
        else:
            functions.append(entity)
