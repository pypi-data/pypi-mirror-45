from django.apps import AppConfig

from .errors import BAD_CONFIG_ERROR


def webpack_cfg_check(*args, **kwargs):
    '''Test if config is compatible or not'''
    from django.conf import settings

    check_failed = False
    user_config = getattr(settings, 'WEBPACK_LOADER', {})
    try:
        user_config = [dict({}, **cfg) for cfg in user_config.values()]
    except TypeError:
        check_failed = True

    errors = []
    if check_failed:
        errors.append(BAD_CONFIG_ERROR)
    return errors


class WebpackLoaderRemoteConfig(AppConfig):
    name = 'webpack_loader_remote'
    verbose_name = "Webpack Loader Remote"

    def ready(self):
        from django.core.checks import register, Tags
        register(Tags.compatibility)(webpack_cfg_check)
