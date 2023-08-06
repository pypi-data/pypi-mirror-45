from speaklater import is_lazy_string, make_lazy_string
from aiohttp.web import middleware
from aiohttp_babel import locale
from babel.core import UnknownLocaleError
from threading import local

_thread_locals = local()


def make_lazy_gettext(lookup_func):
    def lazy_gettext(string, *args, **kwargs):
        if is_lazy_string(string):
            return string
        return make_lazy_string(lookup_func(), string, *args, **kwargs)
    return lazy_gettext

_ = make_lazy_gettext(lambda: _thread_locals.locale.translate)


@middleware
async def babel_middleware(request, handler):
    # get locale from cookie
    _code = locale.detect_locale(request)
    _thread_locals.locale = locale.get(_code)
    return await handler(request)


def get_current_locale():
    return getattr(_thread_locals, 'locale', None)
