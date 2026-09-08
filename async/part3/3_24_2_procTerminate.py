import asyncio
import sys


async def sub_proc(code: str, timeout: int | float) -> str:
    process = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    try:
        data_output, data_error = await asyncio.wait_for(process.communicate(), timeout)
        if data_error:
            return "Exception"
        return data_output.decode().rstrip()

    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return "TimeoutError"
    except Exception:
        if process.returncode is None:
            process.terminate()
            await process.wait()
        return "Exception"
