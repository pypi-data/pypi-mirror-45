class NumberValidator:
    def has_min(self, val, min, message):
        if val < min:
            self.notifications = message

    def has_max(self, val, max, message):
        if val > max:
            self.notifications = message

    def is_between(self, val, min, max, message):
        if val < min or val > max:
            self.notifications = message
