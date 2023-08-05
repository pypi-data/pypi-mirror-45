class GradCafeTracking(object):
    def __init__(self,colleges, course, last_updated):
        self.colleges = colleges
        self.course = course
        self.last_updated = last_updated

    def to_json(self):
        return {
            'colleges': self.colleges,
            'course': self.course,
            'last_updated': self.last_updated
        }

    def clear(self):
        self.colleges = []
        self.course = ""
        self.last_updated = ""