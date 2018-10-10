class Student(object):

    @property
    def score(self):
        print 'property get'
        return self._score

    @score.setter
    def score(self, value):
        print 'property set'
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

s = Student()
s.score=60
print s.score
if __name__=="__main__":
    print("main")
