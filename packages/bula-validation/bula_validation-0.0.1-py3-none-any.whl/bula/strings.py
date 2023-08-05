class StringValidator:
    def is_notnull_or_notempty(self, val, message):
        if val is None or val == '':
            self.notifications = message

    def is_null_or_empty(self, val, message):
        if val is not None or val != '':
            self.notifications = message

    def is_equal(self, val1, val2, message):
        if val1 != val2:
            self.notifications = message

    def is_not_equal(self, val1, val2, message):
        if val1 == val2:
            self.notifications = message
