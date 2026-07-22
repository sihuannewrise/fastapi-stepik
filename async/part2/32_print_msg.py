async def print_msg():
    a = ctx.get(ctx_msg, "failure")
    b = ctx.get(ctx_fileno, "failure")
    c = ctx.get(ctx_permission, "guest")
    print(f"{a}, fileno={b}, {c}")
