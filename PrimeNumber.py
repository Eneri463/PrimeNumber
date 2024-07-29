import random
import math
from datetime import datetime
import PySimpleGUI as sg

# массив простых чисел до 2000
simple_numbers = []

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# функция Эйлера
def eylerFunc(n):
    
    res = 0
    
    # ищем числа, взаимно простые к n
    # их количество - значение функции Эйлера
    for num in range (0, n):
        
        if math.gcd(num, n) == 1:
            res = res + 1
    
    return res

#------------------------------------------------------------------------------
# имеет ли число первообразные корни
# m - число, l - упорядоченные простые множители m
def isRoot(m, l):
    
    # первообразные корни могут существовать только у m вида
    # m = 2, 4, p^a, 2*p^a
    # где p>2 - простое число
    # a>=1 - натуральное число
    
    l1 = list(set(l)) # простые множители без повторений
    
    if m == 2 or m == 4:
        return True
    
    # если m представимо степенью одного простого числа
    if len(l1) == 1:
        
        # если это степень двойки
        if l1[0] == 2:
            return False
        # если это степень другого простого числа
        else:
            return True
    
    # если m представимо степенью двух простых чисел
    if len(l1) == 2:
        
        # если представимо степенью двух чисел, но одно из них не двойка
        # т.е. это m не представимо в виде 2*p^a
        if l1[0] != 2:
            return False
        
        # если m = 2^n*p^a, где n больше 1
        if l[1] == 2:
            return False
        else:
            return True
    
    if len(l1) > 2:
        return False


#------------------------------------------------------------------------------
# факторизация числа (разложение на простые множители)
def prime_factors(num): 
    
    res = []
    
    while num % 2 == 0:
        res.append(2)
        num = num / 2 
 
    for i in range(3, int(math.sqrt(num)) + 1, 2): 
 
        while num % i == 0: 
            res.append(i)
            num = num / i 
            
    if num > 1: 
        res.append(num)
    
    res.sort()
    
    return res

#------------------------------------------------------------------------------
# поиск первообразных корней по модулю modulo
def primitive_root(modulo, kolvo):
    
    start_time = datetime.now()

    corni = []
    
    # единица не имеет первообразных корней
    if modulo == 1:
        return corni, datetime.now() - start_time
    # у двойки один первообразный корень - единица
    elif modulo == 2:
        return [1], datetime.now() - start_time 
    
    n = eylerFunc(eylerFunc(modulo)) # максимальное количество первообразных корней
    phiM = eylerFunc(modulo)
    k = 0 # число найденных первообразных корней
    g = 1 # потенциальный первообразный корень
    
    
    q = list(set(prime_factors(phiM))) # простые делители phiM
    q1 = prime_factors(modulo) # простые делители modulo
    
    # проверяем, может ли m вообще иметь первообразные корни
    if isRoot(modulo, q1) == False:
        return corni, datetime.now() - start_time
    
    # ищем первообразные корни
    while k < kolvo and k < n:
        
        g += 1
        
        # проверяем, является ли число взаимно простым с modulo
        # если нет, то это не первообразный корень
        if math.gcd(g, modulo) != 1:
            continue
        
        flag = True
        
        # проверяем по свойству 5
        for i in range(len(q)):
            if pow(g, int(phiM/q[i]), modulo) == 1:
                flag = False
                break
        
        if flag == False:
            continue
        
        corni.append(g)
        k += 1        
    
    return corni, datetime.now() - start_time

#------------------------------------------------------------------------------
# тест Рабина-Миллера (проверка на простоту)

def test_RM_help(p, b, m):
    
    a = 0 # случайное число меньше p
    j = 0
    z = 0
    flag = 0
    
    if(p <= 1001):
        a = random.randint(1, p-1)
    else:
        a = random.randint(1, 1000)
    
    
    while(flag == 0):
    
        try:
            
            z = pow(a,int(m),p)
            flag = 1
            
        except OverflowError:
            
            if(p <= 1001):
                a = random.randint(1, p-1)
            else:
                a = random.randint(1, 1000)
    
    
    if z == 1 or z == p-1:
        return True
    
    flag = 0
    
    while flag == 0:
        
        if j>0 and z==1:
            return False
        
        j = j+1
        
        if j<b and z<p-1:
            z = pow(z,2,p)
        else:
            flag = 1
            if z == p-1:
                return True
    
    if j == b and z != p-1:
        return False
    
    return True

#------------------------------------------------------------------------------
# тест Рабина-Миллера
def test_RM(p, t):
    
    b = 0   # искомое b
    m = p-1
    
    # ищем, сколько раз делится p-1 на 2
    while m%2 == 0:
        b = b+1
        m = m/2
    
    m = (p-1)/pow(2,b)
    
    # начинаем цикл проверок
    
    for i in range(t):
        
        flag = test_RM_help(p, b, m)
        
        if flag == False:
            return False
    
    return True

#------------------------------------------------------------------------------
# поиск простых чисел на диапазоне
def simple_search(a, b):
    
    sn = []
    
    start_time = datetime.now()
    
    if a <= 2:
        sn.append(2)
        a = 3
        
    for i in range(a, b+1):
      if i%2 != 0 and test_RM(i,5):
          sn.append(i)
    
    return sn, datetime.now() - start_time
        

# -----------------------------------------------------------------------------
# генерация n-битного нечётного числа
def getNbitNumber(n):

    p = bin(random.getrandbits(n))[2:]

    while len(p) < n-1:
        
        if random.randint(0,1) == 1:
            p = p + "1"
        else:
            p = p + "0"
            
    p = p[:n-1] + "1"

    return int(p, 2)


#------------------------------------------------------------------------------
# генерация простого числа
def simple_generation(n,t):
    
    start_time = datetime.now()
    
    itera = 0
    
    while(True):
        
        itera +=1
        
        # случайное N-битное число
        p = getNbitNumber(n)
        
        # проверяем делимость на простые числа
        
        delimost = 0
        
        for i in range(len(simple_numbers)):
            
            # это НЕ простое число, если оно делится на другое простое число
            # не учитываем ситуацию, когда число делится само на себя
            if p%simple_numbers[i] == 0 and p!=simple_numbers[i]:
                delimost = 1
                break
        
        # применяем тест Рабина-Миллера
        if delimost != 1:
            
            if test_RM(p, t):
                return p, datetime.now() - start_time, itera
    
#------------------------------------------------------------------------------
# алгоритм Диффи-Хеллмана
def DiffiHellman(n = 0, xa = 0, xb = 0, typeOfWork = 1):
     
    if typeOfWork == 1:
        
        # генерируем простое число с количеством бит, равным 20
        n,_,_ = simple_generation(20, 5)
        xa = random.randint(1, n-1)
        xb = random.randint(1, n-1)
    
    g, _ = primitive_root(n, 1)
    g = g[0]

    # ключ абонента А
    ya = pow(g, xa, n)
    
    # ключ абонента B
    yb = pow(g, xb, n)
    
    # секретный ключ
    ka = pow(yb, xa, n)
    kb = pow(ya, xb, n) 
    
    return n, g, xa, xb, ka, kb

#------------------------------------------------------------------------------
def main1():
 
    sg.theme('DefaultNoMoreNagging')


    simple_one = [
                    [sg.Text('_______________________________________________________________________________________')],
                    [sg.Text('Количество бит (n): ')],
                    [sg.Input(size=(87, 1),key='bit1')],
                    [sg.Text('Количество проверок в тесте (t): ')],
                    [sg.Input(size=(87, 1),key='test1')],
                    [sg.Text('Результат: ')],
                    [sg.Output(size=(85, 5),key='result1')],
                    [sg.Text('_______________________________________________________________________________________')],
                    [sg.Button('ОК', key ='ok1')]
                ]

    simple_many = [
                    [sg.Text('_______________________________________________________________________________________')],
                    [sg.Text('Начало диапазона (a): ')],
                    [sg.Input(size=(87, 1),key='a2')],
                    [sg.Text('Конец диапазона (b): ')],
                    [sg.Input(size=(87, 1),key='b2')],
                    [sg.Text('Результат: ')],
                    [sg.Output(size=(85, 5),key='result2')],
                    [sg.Text('_______________________________________________________________________________________')],
                    [sg.Button('ОК', key ='ok2')]
                    
                ]

    root_gen = [ 
                     [sg.Text('_______________________________________________________________________________________')],
                     [sg.Text('Число: ')],
                     [sg.Input(size=(87, 1),key='number3')],
                     [sg.Text('Первообразные корни числа (первые 100): ')],
                     [sg.Output(size=(85, 5),key='result3')],
                     [sg.Text('_______________________________________________________________________________________')],
                     [sg.Button('ОК', key ='ok3')]
                ]

    difi = [         [sg.Text('_______________________________________________________________________________________')],
                     [sg.Text('Простое число n: ')],
                     [sg.Input(size=(87, 1),key='bit4')],
                     [sg.Text('Xa: ')],
                     [sg.Input(size=(87, 1),key='bit5')],
                     [sg.Text('Xb: ')],
                     [sg.Input(size=(87, 1),key='bit6')],
                     [sg.Text('Способ получения n, Xa, Xb:'), sg.Radio("Генерируются программой", "type7", key='genN'), sg.Radio("Задаются пользователем", "type7", key='vvodN', default=True)],
                     [sg.Text('Результат: ')],
                     [sg.Output(size=(85, 6),key='result4')],
                     [sg.Button('Сгенерировать', key ='ok4')]
                ]

    tab_group_layout = [[sg.TabGroup([[sg.Tab('Генерация простого числа', simple_one, key='-TAB1-'), sg.Tab('Простые числа из диапазона', simple_many, key='-TAB2-'),sg.Tab('Первообразные корни', root_gen, key='-TAB3-'), sg.Tab('Диффи-Хеллман', difi, key='-TAB4-')]])]]

    window = sg.Window('Лабораторная 5', tab_group_layout)

    while True:
        event, values = window.read()
        
        if event in (None, 'Exit'):
            break
        
        # ---------------------------------------------------------------------
        # генерация простого числа
        
        elif event == 'ok1':
            
            if values['bit1'] == "" or values['test1'] == "":
                sg.popup_ok("Необходимо заполнить поля")
            
            n = int(values['bit1'])
            t = int(values['test1'])
            
            p, work_time, itera = simple_generation(n,t)
            
            window['result1'].update("Сгенерировано число: " + str(p) + "\nЧисло итераций: " + str(itera) + "\nВремя выполнения: " + str(work_time))
            
                            
        
        # ---------------------------------------------------------------------
        # простые числа из диапазона
        
        elif event == 'ok2':
            
            if values['a2'] == "" or values['b2'] == "":
                sg.popup_ok("Необходимо заполнить поля")
            
            a = int(values['a2'])
            b = int(values['b2'])
            
            p, work_time = simple_search(a, b)
            
            window['result2'].update("Простые числа из диапазона:\n" + str(p) + "\nВремя выполнения: " + str(work_time))
            
                    
        
        # ---------------------------------------------------------------------
        # первообразные корни числа
        
        elif event == 'ok3':
            
            if values['number3'] == "":
                sg.popup_ok("Необходимо заполнить поля")
            
            n = int(values['number3'])
            
            p, work_time = primitive_root(n, 100)
            
            window['result3'].update("Первообразные корни:\n" + str(p) + "\nВремя выполнения: " + str(work_time))
            
                           
        # ---------------------------------------------------------------------
        # схема Диффи-Хеллмана
        
        elif event == 'ok4':
            
            if values['genN'] == True:
                
                n, q, xa, xb, ka, kb = DiffiHellman()
                window['result4'].update("n: " + str(n) + "\ng: " + str(q) +"\nxa: " + str(xa) + "\nxb: " + str(xb) + "\nka: " + str(ka) + "\nkb: " + str(kb))
                
            else:
                
                if values['bit4'] == "" or values['bit5'] == "" or values['bit6'] == "":
                    sg.popup_ok("Необходимо заполнить поля")
                else:
                
                    n = int(values['bit4'])
                    
                    if n%2 == 0 or not test_RM(n,5):
                        sg.popup_ok("В поле n должно быть простое число")
                    else:
                        
                        xa = int(values['bit5'])
                        xb = int(values['bit6'])
                        
                        if xa >= n or xb >= n:
                            sg.popup_ok("Xa и Xb должны быть меньше n")
                        
                        else:
                            
                            n, q, xa, xb, ka, kb = DiffiHellman(n, xa, xb, 2)
                        
                            window['result4'].update("n: " + str(n) + "\ng: " + str(q) +"\nxa: " + str(xa) + "\nxb: " + str(xb) + "\nka: " + str(ka) + "\nkb: " + str(kb))
                               
            
        
            
    window.close()

simple_numbers, _ = simple_search(1, 2000)
main1()

