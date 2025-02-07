def secantMethod(func, x0, x1):

    def f(x):
        return eval(func)

    toleranceReached = False

    for i in range (1,10):

        if(f(x0)-f(x1) == 0):
            x0 = x0 - 0.001

        xi = x0 - f(x0) / (f(x0)-f(x1)) * (x0-x1)

        x0 = x1
        x1 = xi

        if(abs((x1-x0)/x1) <= 1e-9):
            toleranceReached = True
            break

    print(f"A raiz da funcao e aproximadamente {x1}", end = "")

    if(not toleranceReached):
        print(" mas este valor nao e muito preciso", end = "")

    print("")



def newtonsMethod(func, x0):

    def f(x):
        return eval(func)

    def df(x):
        return (f(x + 1e-6) - f(x)) / 1e-6

    toleranceReached = False

    for i in range(1,10):

        if(df(x0) == 0):
            x0 = x0 - 0.001

        oldx0 = x0
        x0 = x0 - (f(x0) / df(x0))

        if(abs((x0-oldx0)/x0) <= 1e-9):
            toleranceReached = True
            break

    print(f"A raiz da funcao e aproximadamente {x0}", end = "")

    if(not toleranceReached):
        print(" mas este valor nao e muito preciso", end = "")

    print("")



def bissetrizMethod(func, x0, x1):
    
    def f(x):
        return eval(func)

    toleranceReached = False

    for i in range (1,20):

        xi = (x0+x1) / 2.0

        if(f(x0) * f(xi) > 0):
            x0 = xi
            lastUsed = 0
            if(x0 == 0):
                x0 = 0.001
        else:
            x1 = xi
            lastUsed = 1
            if(x1 == 0):
                x1 = 0.001

        if(abs((x0-x1) / (x0 if lastUsed == 0 else x1)) <= 1e-6):
            toleranceReached = True
            break


    print(f"A raiz da funcao e aproximadamente {x0}", end = "")

    if(not toleranceReached):
        print(" mas este valor nao e muito preciso", end = "")

    print("")



def main():

    method = 3

    while(method < 0 or method > 2):

        method = int(input("""Insira o metodo que deseja utilizar.
0 -> metodo da bisseçao
1 -> metodo de newton
2 -> metodo da secante
"""))

    func = input("insira a expressão que deseja avaliar. Exemplo: x**3 + 5*x**2 -x - 4\n")

    if(method == 1):
        val1 = float(input("insira o valor inicial.\n"))
    else:
        val1 = float(input("insira um extremo do intervalo\n"))
        val2 = float(input("insira o outro extremo\n"))

    if(method == 0):
        bissetrizMethod(func, val1, val2)
    elif(method == 1):
        newtonsMethod(func, val1)
    else:
        secantMethod(func, val1, val2)

main()