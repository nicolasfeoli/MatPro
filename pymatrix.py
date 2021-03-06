class Matrix():

    def __init__(self, argumentos):
        """
        Metodo de inicializacion de la matriz.
        Recibe una lista que representa la matriz.
        """
        self.listaValores = list()
        x = 0
        for fila in argumentos:
          if len(fila) > x:
                x = len(fila)
        for fila in argumentos:
            while len(fila) < x:
                fila.append(0)
        for fila in argumentos:
            if type(fila) == list:
                self.listaValores.append(fila)
        self.dimensiones = len(self.listaValores)*len(self.listaValores[0])

    def __repr__(self):
        """
        Metodo que define lo que se va a imprimir cuando se haga print matriz
        """
        mayor = 0
        final = ""
        for i in self.listaValores:
            for j in i:
                if len('{} '.format(int(j))) > mayor:
                    mayor = len('{} '.format(int(j)))
        for fila in self.listaValores:
            s = ''
            for i in fila:
                t = '{} '.format(int(i))
                while len(t) < mayor:
                    t = ' ' + t
                s += t
            s = s[:-1]
            final += s+"\n"
            print(s)
        return final
        
       

    def __add__(self, otraMatriz):
        """
        Metodo que define la suma de matrices.
        """
        if type(otraMatriz) != Matrix or \
            self.dimensiones != otraMatriz.dimensiones or\
            len(self.listaValores) != len(otraMatriz.listaValores):
            raise ArithmeticError
        x = list()
        for i in range(0, len(self.listaValores)):
            fila = []
            for j in range(0, len(self.listaValores[0])):
                fila.append(float(self.listaValores[i][j] + otraMatriz.listaValores[i][j]))
            x.append(fila)
        return Matrix(x)

    def __mul__(self, otraMatriz):
        """
        Metodo que define la multiplicacion de matrices
        """
        if type(otraMatriz) == int or type(otraMatriz) == float:
            return otraMatriz * self
        if type(otraMatriz) != Matrix:
            raise ArithmeticError
        if len(otraMatriz.listaValores) == 1:
            otraMatriz = otraMatriz.transcribir()
        if len(self.listaValores[0]) != len(otraMatriz.listaValores):
            raise ArithmeticError
        r = []
        for i in range(0, len(self.listaValores)):
            x = []
            for j in range(0,len(otraMatriz.listaValores[0])):
                a = 0
                for k in range(0, len(self.listaValores[0])):
                    a += self.listaValores[i][k] * otraMatriz.listaValores[k][j]
                x.append(a)
            r.append(x)
        return Matrix(r)

    def __rmul__(self, otraMatriz):
        """
        Metodo que define la multiplicacion de matrices cuando se multiplican por un entero.
        """
        a = float(otraMatriz)
        x = []
        for i in range(0, len(self.listaValores)):
            r = []
            for j in range(0, len(self.listaValores[0])):
                r.append(a * self.listaValores[i][j])
            x.append(r)
        return Matrix(x)


    def __pow__(self, exp):
        """
        Metodo que define la potenciacion de matrices.
        Numero debe ser un entero.
        """
        a = exp
        t = False
        if a < 0:
            a *= -1
            t = True
        b = 1
        x = self
        while b < a:
            x *= self
            b += 1
        if t:
            pass
        return x

    def __sub__(self, b):
        """
        Metodo que define la resta de matrices.
        """
        return self + -1*b

    def transcribir(self):
        """
        Metodo que define la transcripcion de funciones.
        Es necesitado por el metodo de multiplicacion.
        """
        r = []
        for j in range(0,len(self.listaValores[0])):
            x = []
            for i in range(0,len(self.listaValores)):
                a = self.listaValores[i][j]
                x.append(a)
            r.append(x)
        return Matrix(r)
        
    def determinant(self):
        if len(self.listaValores) == len(self.listaValores[0]):
            if self.dimensiones == 4:
                return (self.listaValores[0][0]*self.listaValores[1][1] - self.listaValores[1][0]*self.listaValores[0][1])
            elif self.dimensiones == 1:
                return self.listaValores[0][0]
            else:
                x = 0
                if (type(self.listaValores[0][0]) == Matrix):
                    x = Matrix([[0]]*self.listaValores[0][0].dimensiones)
                for j in range(0, len(self.listaValores[0])):
                    x += self.listaValores[0][j] * (self.subMatrix(1, j+1).determinant()) * ((-1) ** (2+j))
                return x
        else:
            raise ArithmeticError
            
    def magnitude(self):
        if len(self.listaValores) == 1 or len(self.listaValores[0]) == 1:
            x = 0
            for i in self.listaValores:
                for j in i:
                    x += j**2
            return (x)**(1/2)
               
    def subMatrix(self, a, b):
        if a < 1 or b < 1:
            raise ArithmeticError
        a = int(a) - 1
        b = int(b) - 1
        x = []
        for i in range(0, len(self.listaValores)):
            if i  != a:
                r = []
                for j in range(0, len(self.listaValores[0])):
                    if j != b:
                        r. append(self.listaValores[i][j])
                x.append(r)
        return Matrix(x)
        
    def crossProduct(self, v):
        i = Matrix([[1],[0],[0]])
        j = Matrix([[0],[1],[0]])
        k = Matrix([[0],[0],[1]])
        if type(v) != Matrix :
            raise ArithmeticError
        if self.dimensiones == 3 and v.dimensiones == 3:
            a = self
            b = v
            if len(self.listaValores[0]) == 1:
                a = self.transcribir()
            if len(v.listaValores[0]) == 1:
                b = v.transcribir()
            c = Matrix([[i,j,k],a.listaValores[0],b.listaValores[0]])
            return c.determinant()
            
    def inverse(self):
        if len(self.listaValores) == len(self.listaValores[0]) or self.determinant != 0:
            x = []
            for i in range(0, len(self.listaValores)):
                r = []
                for j in range(0, len(self.listaValores[0])):
                    r.append(self.subMatrix(i+1,j+1).determinant()*((-1)**(j+i+2)))
                x.append(r)
            return (Matrix(x).transcribir()*(1/self.determinant()))
        else:
            raise ArithmeticError
            
    def solutionForVector(self, v):
        if type(v) == Matrix and len(v.listaValores[0]) == 1 and len(v.listaValores) == len(self.listaValores[0]):
            x = self.inverse()*v
            return x

    def asignarMatriz(self, v):
        """
        setMatriz
        """
        return

    def obtenerMatriz(self):
        """
        getMatriz
        """
        return self

    def sumaMatriz(self, matriz2):
       return self + matriz2

    def restaMatriz(self, matriz2):
        return self - matriz2

    def multiplicaMatriz(self, matriz2):
        return self * matriz2

    def exponenciacionMatriz(self, exponente):
        return self ** exponente
