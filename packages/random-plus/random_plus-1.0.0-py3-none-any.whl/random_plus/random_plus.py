import random


class ramdon_plus():
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

    def aa(self, **N):
        if N:
            if 'Many' in N:
                self.default_number = N['Many']
                for x in self.F:
                    # print(x)
                    for i in N:
                        # print(i)
                        if x in i and x != 'Many':
                            # print(x)
                            # print(self.F[x])
                            self.G = self.G + self.F[x]
                if self.G:
                    self.E = self._for(self.default_number, self.G)
                else:
                    self.E = self._for(self.default_number,
                                       self.A+self.B+self.C+self.D)
                # print(self.E)
        else:
            self.E = self._for(self.default_number,
                               self.A+self.B+self.C+self.D)
        return "".join(str(x) for x in self.E)


'''
    def ramdon_plus(self, **N):
        if N:
            if 'Many' in N:
                self.default_number = N['Many']
            if 'Num' in N and 'Mark'in N:
                self.E = self._for(self.default_number, self.B+self.C)
            elif 'En' in N and 'Mark'in N:
                self.E = self._for(self.default_number, self.A+self.C)
            elif 'En' in N and 'Num'in N:
                self.E = self._for(self.default_number, self.A+self.B)
            elif 'EN' in N and 'Mark'in N:
                self.E = self._for(self.default_number, self.A+self.C)
            elif 'EN' in N and 'En'in N:
                self.E = self._for(self.default_number, self.A+self.D)
            elif 'EN' in N and'Num'in N:
                self.E = self._for(self.default_number, self.A+self.E)
            elif 'En' in N:
                self.E = self._for(self.default_number, self.A)
            elif 'Mark' in N:
                self.E = self._for(self.default_number, self.C)
            elif 'Num' in N:
                self.E = self._for(self.default_number, self.B)
            elif 'EN' in N:
                self.E = self._for(self.default_number, self.D)
            else:
                self.E = self._for(self.default_number, self.A+self.B+self.C)
        else:
            self.E = self._for(self.default_number, self.A+self.B+self.C)
        return "".join(str(x) for x in self.E)


a = ramdon_plus().aa(EN='t', En='t', Many=100)
print(a)
'''