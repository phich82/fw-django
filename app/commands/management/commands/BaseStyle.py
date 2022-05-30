class BaseStyle:

    def error(self, message):
        self.stdout.write(self.style.ERROR(message))

    def notice(self, message):
        self.stdout.write(self.style.NOTICE(message))

    def success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def warning(self, message):
        self.stdout.write(self.style.WARNING(message))

    def info(self, message):
        self.stdout.write(self.style.HTTP_INFO(message))

    def info_column(self, message):
        self.stdout.write(self.style.SQL_FIELD(message))

    def info_column_type(self, message):
        self.stdout.write(self.style.SQL_COLTYPE(message))

    def info_keyword(self, message):
        self.stdout.write(self.style.SQL_KEYWORD(message))

    def info_table(self, message):
        self.stdout.write(self.style.SQL_TABLE(message))

    def info1x(self, message):
        self.stdout.write(self.style.HTTP_INFO(message))

    def success2x(self, message):
        self.stdout.write(self.style.HTTP_SUCCESS(message))

    def error304(self, message):
        self.stdout.write(self.style.HTTP_NOT_MODIFIED(message))

    def error3x(self, message):
        self.stdout.write(self.style.HTTP_REDIRECT(message))

    def error404(self, message):
        self.stdout.write(self.style.HTTP_NOT_FOUND(message))

    def error400(self, message):
        self.stdout.write(self.style.HTTP_BAD_REQUEST(message))

    def error5x(self, message):
        self.stdout.write(self.style.HTTP_SERVER_ERROR(message))

    def info_heading(self, message):
        self.stdout.write(self.style.MIGRATE_HEADING(message))

    def info_label(self, message):
        self.stdout.write(self.style.MIGRATE_LABEL(message))
