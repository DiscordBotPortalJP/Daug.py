from Daug.functions import embeds  # noqa: F401
from functools import wraps
import traceback


def excepter(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            orig_error = getattr(e, 'original', e)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            appinfo = await self.bot.application_info()
            await appinfo.owner.send(f'```python\n{error_msg}\n```')
    return wrapped
