import random


class random_plus():
    def __init__(self):
        self.A = 'qwertyuiopasdfghjklzxcvbnm'
        self.B = '0123456789'
        self.C = '/?.>,<;:|{}[]~!@#$%^&*()'
        self.D = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        self.E = []
        self.G = ''
        self.default_number = 8
        self.F = {'En': self.A, 'Num': self.B, 'Mark': self.C, 'EN': self.D}

    def _for(self, *A):
        D = []
        for i in range(int(A[0])):
            D = D+random.sample(A[1], 1)
        return D

    def random_plus(self, **N):
        if N:
            if 'Many' in N:
                self.default_number = N['Many']
            for x in self.F:
                for i in N:
                    if x in i and x != 'Many':
                        self.G = self.G + self.F[x]
            if self.G:
                self.E = self._for(self.default_number, self.G)
            else:
                self.E = self._for(self.default_number,
                                    self.A+self.B+self.C+self.D)
        else:
            self.E = self._for(self.default_number,
                               self.A+self.B+self.C+self.D)
        return "".join(str(x) for x in self.E)


