"""apps"""
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class AppLocalConfig(AppConfig):
    """AppLocalConfig subclass of AppConfig"""
    name = 'app'
