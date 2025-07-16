from django.apps import AppConfig


class DjSkillswapAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_skillswap_app'


    def ready(self):
            import dj_skillswap_app.signals
