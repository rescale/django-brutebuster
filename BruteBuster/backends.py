from django.contrib.auth.backends import ModelBackend
from BruteBuster.models import FailedAttempt
from BruteBuster.middleware import get_request
from django.core.exceptions import ValidationError


class BrutebusterBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        request = get_request()
        if request:
            # try to get the remote address from thread locals
            IP_ADDR = request.META.get('REMOTE_ADDR', None)
        else:
            IP_ADDR = None

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

        user = super(BrutebusterBackend, self).authenticate(username, password)
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
