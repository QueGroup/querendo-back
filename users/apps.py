from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # noinspection PyUnresolvedReferences
    def ready(self) -> None:
        """
        This method is called when the `users` application is ready.

        It registers signals that should be processed when the User model is saved.

        :return: None
        """
        from users import signals
