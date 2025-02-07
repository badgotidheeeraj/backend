# from django.apps import AppConfig

# class BlogApiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'blog_api'
#     # def ready(self):
#     #     from .cron import start_scheduler
#     #     start_scheduler()


# # from django.apps import AppConfig

# # class SchedulerConfig(AppConfig):
# #     name = 'scheduler'

# #     def ready(self):
# #         from .scheduler import start_scheduler
# #         start_scheduler()


from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_api'

    def ready(self):
        import blog_api.signals  # Ensure signals are connected
