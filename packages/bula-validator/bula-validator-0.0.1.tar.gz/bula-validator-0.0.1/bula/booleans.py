class BooleanValidator:
    def is_true(self, val, message):
        if not val:
            self.notifications = message

    def is_false(self, val, message):
        if val:
            self.notifications = message
