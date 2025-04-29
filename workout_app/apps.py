from django.apps import AppConfig


class WorkoutAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workout_app'

    def ready(self):
        import workout_app.signals.d_program_asign_signal
