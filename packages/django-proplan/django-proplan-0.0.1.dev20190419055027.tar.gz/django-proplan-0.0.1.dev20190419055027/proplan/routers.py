"""
Router for application.
"""


class ProplanRouter:
    """
    A router to control all database operations on models in this
    application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read proplan models go to proplan database.
        """
        if model._meta.app_label == 'proplan':
            return 'proplan'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write proplan models go to proplan database.
        """
        if model._meta.app_label == 'proplan':
            return 'proplan'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the proplan app is involved.
        """
        if obj1._meta.app_label == 'proplan' or \
           obj2._meta.app_label == 'proplan':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the proplan app only appears in the 'proplan'
        database.
        """
        if app_label == 'proplan':
            return db == 'proplan'
        return None
