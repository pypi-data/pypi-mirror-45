import re
import logging

from hawkei.store import Store
from hawkei.utils import url_obfuscate, uuid
from hawkei.config import config

_COOKIE_NAME = '_hawkei_stid'

class HawkeiMiddleware:
    logger = logging.getLogger('hawkei')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (config.active()):
            Store.init()
            try:
                Store.add({'session_tracker_id': self.get_session_tracker_id(request)})
                Store.add({'request': self.get_request_data(request)})
                Store.add({'software': request.META.get('SERVER_SOFTWARE')})
            except Exception as e:
                self.logger.exception("Exception while storing middleware data: %r", e)

        response = self.get_response(request)

        if (config.active()):
            self.write_session_tracker_id(response)
            Store.delete()

        return response

    @classmethod
    def get_session_tracker_id(cls, request):
        return request.COOKIES.get(_COOKIE_NAME) or uuid()

    @classmethod
    def write_session_tracker_id(cls, response):
        try:
            response.set_cookie(
                _COOKIE_NAME,
                value=Store.get().get('session_tracker_id'),
                max_age=(10 * 365 * 24 * 60 * 60),
                path='/',
                httponly=False,
                domain=config.data.get('domain'),
            )
        except Exception as e:
            cls.logger.exception("Exception while setting cookie: %r", e)

    @classmethod
    def get_request_data(cls, request):
        return ({
            'url': url_obfuscate(request.build_absolute_uri(), config.data['obfuscated_fields']),
            'get_params': dict(request.GET.items()),
            'post_params': dict(request.POST.items()),
            'ssl': request.scheme == 'https',
            'host': request.get_host(),
            'path': request.path,
            'referrer': url_obfuscate(request.META.get('HTTP_REFERER'), config.data['obfuscated_fields']),
            'method': request.method,
            'xhr': request.META.get('HTTP_X_REQUESTED_WITH') is not None,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'ip': request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR'),
            'headers': cls.get_headers(request.META),
        })

    @classmethod
    def get_headers(cls, meta):
        pattern = re.compile("^HTTP_|^CONTENT_TYPE$|^CONTENT_LENGTH$")
        skip_headers=['HTTP_COOKIE']
        headers = {}

        for key in meta:
            if isinstance(key, str) and pattern.match(key) and not key in skip_headers:
                formated_key = '-'.join([value.title() for value in key.split('_')])
                headers[formated_key] = meta.get(key)

        return headers
