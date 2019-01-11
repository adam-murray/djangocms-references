from functools import lru_cache

from django.apps import apps
from django.contrib.contenttypes.models import ContentType


@lru_cache(maxsize=1)
def supported_models():
    try:
        app_config = apps.get_app_config("djangocms_navigation")
    except LookupError:
        return []
    else:
        extension = app_config.cms_extension
        return extension.navigation_apps_models


@lru_cache(maxsize=1)
def supported_content_type_pks():
    app_config = apps.get_app_config("djangocms_navigation")
    models = app_config.cms_extension.navigation_apps_models
    content_type_dict = ContentType.objects.get_for_models(*models)
    return [ct.pk for ct in content_type_dict.values()]