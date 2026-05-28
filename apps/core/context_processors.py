from .utils.constants import SYSTEM_NAME, SYSTEM_SHORT_NAME


def app_settings(request):
    return {
        'system_name': SYSTEM_NAME,
        'system_short_name': SYSTEM_SHORT_NAME,
    }
