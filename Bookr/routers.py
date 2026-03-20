class BookOnlineRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'bookOnline':
            return 'mysql'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'bookOnline':
            return 'mysql'
        return 'default'

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'bookOnline':
            return db == 'mysql'
        return db == 'default'