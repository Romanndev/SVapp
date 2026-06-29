import math

eps = 100
g = 5
y = 10
bvps = 10

# фнкция расчитывает варианты формулы Грэма по заданным параметрам(в год публикации)
def value(eps,g,y,bvps) :
    GRAHAM_1962 = eps*(8.5 + 2*g)
    print('Graham 1962 formula:',GRAHAM_1962)

    GRAHAM_1974 =((eps*(8.5 + 2*g))*4.4)/y
    print('Graham 1974 formula:',GRAHAM_1974)

    GRAHAM_1949 = math.sqrt(22.5*eps*bvps)
    print('Graham 1974 formula:',GRAHAM_1949)

value(eps,g,y,bvps)