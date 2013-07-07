from django.contrib.auth.backends import ModelBackend
from BruteBuster.models import FailedAttempt
from BruteBuster.middleware import get_request
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class RateLimitingBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        request = get_request()
        if request:
            # try to get the remote address from thread locals
            # First check if the heroku header with the original client IP
            logger.info('request.META: %s', request.META)
            ip_list = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
            IP_ADDR = ip_list[0].strip()
            if not IP_ADDR:
                # Otherwise, use the basic REMOTE_ADDR header.
                IP_ADDR = request.META.get('REMOTE_ADDR', None)
        else:
            IP_ADDR = None

        logger.info('IP_ADDR: %s', IP_ADDR)
        try:
            fa = FailedAttempt.objects.filter(username=username, IP=IP_ADDR)[0]
            if fa.recent_failure():
                if fa.too_many_failures():
                    # we block the authentication attempt because
                    # of too many recent failures
                    fa.failures += 1
                    fa.save()
                    # Raise validation error
                    raise ValidationError('Your account is temporarily '
                                          'locked out. Please try again later '
                                          'or contact support for assistance.')
            else:
                # the block interval is over, so let's start
                # with a clean sheet
                fa.failures = 0
                fa.save()
        except IndexError:
            # No previous failed attempts
            fa = None

        user = super(RateLimitingBackend, self).authenticate(username,
                                                             password)
        if user:
            # the authentication was successful - we do nothing
            # special
            return user

        # the authentication was kaput, we should record this
        fa = fa or FailedAttempt(username=username, IP=IP_ADDR, failures=0)
        fa.failures += 1
        fa.save()
        # return with unsuccessful auth
        return None
