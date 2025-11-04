'''
Данная программа позволяет проводить 2д симуляцию газа, у которого молекул взаимодействуют абсолютно упруго. управление производится клавишами:
# esc для завершения
# "c" (англ) для начала уменьшения объема области с газом(аддиабатическое сжатие)
# "e" (англ) для начала увеличения объема области с газом(аддиабатическое расширение)
# "shift" для начала Увеличения суммарной кинетической энергии частиц(подогрев)
# "alt" для начала уменьшения суммарной кинетической энергии частиц(охлаждение)
# "ctrl" для завершения сжатия/расширения
Во время работы отображается движение частиц в предоставленом объеме и гистрограмма распределения их скоростей.
С помощью клавиш, описанных выше возможно изменять термодинамические параметры системы. Изменение внутренней энергии системы возможно только путем запуска соответствующих функций. Теплопотери не предусмотрены.
'''
import pygame
from math import *
from random import *
from statistics import mean
import matplotlib.pyplot as plt
ax = plt.subplots()[1]
import numpy as np
import keyboard

NOW_TIME=0


pygame.init()
pygame.display.set_caption("GAS simulation")
# задание размеров области с газом
L=1000
width0=L
height0=L
width=width0
height=height0

win = pygame.display.set_mode((width0*1.5, height0))

# Инициализация цвета
color = (255, 255, 255)
r1=5
# Рисование прямоугольника
pygame.draw.rect(win, color, pygame.Rect(-r1+2*r1, -r1+2*r1, width, height))



# количество частиц
nn=500
print("Number of molecules: "+str(nn))


time_check=0.01
time_sleep=0.001
timer=0
timer_heat=0
time_heat=0.1


delta_px_left=0.0
delta_px_right=0.0
delta_py_up=0.0
delta_py_down=0.0

r=[]
m=[]
m1=1
r1=5
x=[]
y=[]
a=[]
v=[]
v_start=5
c=[]
# v.append(v_start)
for i in range (nn):
    x.append(randrange(r1,width-r1))
    y.append(randrange(r1,height-r1))
    a.append(i*pi/6)
    v.append(v_start)
    # v.append(0.001)
    c.append(0)
    c[i]=(255,0,0)
c[0]=(0,255,0)


Energy=m1*(v_start**2)*nn/2
Energy_check=0
Temperature=[]
Average_pressure=0
Pressure=[]
Volume=[]
Time_meas=[]

counter=0

running=True

Mode="OFF"
def Heat():
    global Mode
    Mode="heat"
def Freeze():
    global Mode
    Mode="freeze"
def OFF():
    global Mode
    Mode="OFF"
def STOP():
    global running
    running=False
def Expansion():
    global Mode
    Mode="expansion"
def Compression():
    global Mode
    Mode="compression"   

# задаем горячие клавиши управления симуляцией
keyboard.add_hotkey("esc", STOP)        #esc для завершения
keyboard.add_hotkey("c", Compression)   # "c" (англ) для начала уменьшения объема области с газом(аддиабатическое сжатие)
keyboard.add_hotkey("e", Expansion)     # "e" (англ) для начала увеличения объема области с газом(аддиабатическое расширение)
keyboard.add_hotkey("shift", Heat)      # "shift" для начала Увеличения суммарной кинетической энергии частиц(подогрев)
keyboard.add_hotkey("alt", Freeze)      # "alt" для начала уменьшения суммарной кинетической энергии частиц(охлаждение)
keyboard.add_hotkey("ctrl", OFF)        # "ctrl" для завершения сжатия/расшире

print("Volume "+"  Sys. energy(temp)  "+"  av. Pressure  "+"  av. Velocity"+"  Time"+"      Mode")

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False#если надо прекратить симуляцию

    win.fill((0,0,0))

    for i in  range(0, nn):
        x[i]+=v[i]*cos(a[i])#симуляция движения частиц
        y[i]+=v[i]*sin(a[i])
        pygame.draw.circle(win, c[i], (x[i], y[i]), r1)

    pygame.draw.rect(win, (0,0,255), pygame.Rect(-r1, -r1, width0+2*r1, height0+2*r1), 5)
    pygame.draw.rect(win, color, pygame.Rect(-r1, -r1,  width+2*r1, height+2*r1), 5)
    pygame.display.update()
    pygame.time.delay(10)

    #проверка столкновения  со стенами
    for i in  range(0, nn):
        #левая
        if (x[i] <= r1 and(a[i]>pi/2 or a[i]<-pi/2)):
            a[i] = pi-a[i]
            # c[i]=(0, 0, 255) #окраска при столкновении со стенками раскоментировать, если нужно оценить количество частиц ударившихся об стенки
            delta_px_left+=abs(2*m1*v[i]*cos(a[i]))
            
        #правая
        if (x[i]+1 >= width-r1 and(a[i]>-pi/2 and a[i]<pi/2)):
            a[i] = pi-a[i]
            # c[i]=(0, 0, 255) #окраска при столкновении со стенками
            delta_px_right+=abs(2*m1*v[i]*cos(a[i]))
            
        #верхняя
        if (y[i] <= r1 and(a[i]<0 and a[i]>-pi)):
            a[i] = -a[i]
            # c[i]=(0, 0, 255) #окраска при столкновении со стенками
            delta_py_up+=abs(2*m1*v[i]*sin(a[i]))
            
        #нижняя
        if (y[i] >= height-r1 and(a[i]>0 and a[i]<pi)):
            a[i] =-a[i]
            # c[i]=(0, 0, 255) #окраска при столкновении со стенками
            delta_py_down+=abs(2*m1*v[i]*sin(a[i]))

        while a[i]>pi: a[i]-=2*pi
        while a[i]<-pi: a[i]+=2*pi

    Energy_check=0#проверка энергии всей системы (вспомогательная перменная для проверки адекватности симуляции. Эксперименты показали, что энергия не утекает со временем)
    for i in range(nn):
        Energy_check+=m1*(v[i]**2)/2

    #проверка столкновений молекул
    for i in range(0, nn):
        for j in range(i, nn):
            if abs(x[i]-x[j])<=2.5*r1 and abs(y[i]-y[j])<=2.5*r1: # проверяем столкновения шаров только у шаров, стоящих близко друг к другу(для оптимизации)
                dist = sqrt((x[i]-x[j])**2+(y[i]-y[j])**2) # рассчет дистанции между шарами
                
                if dist <= r1*2+0.1:
                    # если дистанция меньше, чем 2 радиуса, то рассчитываем координаты, которые будут у шаров при дальнейшем движении
                    x1_new = x[i] + v[i]*cos(a[i])*0.01
                    y1_new = y[i] + v[i]*sin(a[i])*0.01
                    x2_new = x[j] + v[j]*cos(a[j])*0.01
                    y2_new = y[j] + v[j]*sin(a[j])*0.01
                    dist_new = sqrt((x1_new-x2_new)**2+(y1_new-y2_new)**2)
                    if dist > dist_new: # если шары сближаются, то будет столкновение
                        # расчет новых скоростей из закона сохранения импульса
                        collision_angle = atan((y[j]-y[i])/(x[j]-x[i]+0.001))
                        if (x[j]-x[i]) < 0:
                            collision_angle += pi
                            while collision_angle > pi/2: collision_angle -= 2*pi
                            while collision_angle < -pi/2: collision_angle += 2*pi
                        
                        # Скорости в системе координат столкновения
                        velocity_angle1 = a[i] - collision_angle
                        velocity_angle2 = a[j] - collision_angle
                        # Компоненты скоростей вдоль линии столкновения (нормальные) и перпендикулярно (тангенциальные)
                        normal_velocity1 = v[i]*cos(velocity_angle1)
                        normal_velocity2 = v[j]*cos(velocity_angle2)
                        
                        tangential_velocity1 = v[i]*sin(velocity_angle1)
                        tangential_velocity2 = v[j]*sin(velocity_angle2)
                        # Обмен нормальными компонентами скоростей (упрощенная модель)
                        normal_velocity1_new = (2*m1*v[j]*cos(velocity_angle2))/(2*m1)
                        normal_velocity2_new = (2*m1*v[i]*cos(velocity_angle1))/(2*m1)
                        # Новые полные скорости
                        v[i] = sqrt(normal_velocity1_new**2 + tangential_velocity1**2)
                        v[j] = sqrt(normal_velocity2_new**2 + tangential_velocity2**2)
                        # Новые углы движения
                        new_angle1 = atan(tangential_velocity1/normal_velocity1_new)
                        if normal_velocity1_new < 0: new_angle1 += pi
                        new_angle2 = atan(tangential_velocity2/normal_velocity2_new)
                        if normal_velocity2_new < 0: new_angle2 += pi
                        a[i] = collision_angle + new_angle1
                        while a[i] > pi: a[i] -= 2*pi
                        while a[i] < -pi: a[i] += 2*pi
                        a[j] = collision_angle + new_angle2
                        while a[j] > pi: a[j] -= 2*pi
                        while a[j] < -pi: a[j] += 2*pi

    #блок изменения объема
    if Mode=="expansion":
        delta_len=0.1
        width+=delta_len

    if Mode=="compression":
        delta_len=0.1
        width-=delta_len

    # блок изменеия кинетической энергии системы    
    if Mode=="heat":
        delta_v=0.05#при нагреве/охлаждении скорость всех частиц увеличивается/уменьшается на delta_v
        for i in  range(0, nn):
            v[i]+=delta_v

    if Mode=="freeze" and counter>=50:
        delta_v=0.05
        for i in  range(0, nn):
            if v[i]-delta_v>0:
                v[i]-=delta_v


    

    plt.hist(v, range=(0, 20), color = 'blue', edgecolor = 'black', bins=30)
    # plt.axvline(x=mean(v), ymin=0, ymax=1, color='r', linestyle='', label=nn)
    LABEL="kinetic energy= "+str(int(Energy_check))
    plt.scatter([],[],label=LABEL)
    LABEL="Number of molecules= "+str(nn)
    plt.scatter([],[],label=LABEL)

    #этот кусок кода необходим для вывода ожидаемого распределения максвелла при параметрах симуляции nn=500 m1=1 L=500
    # f_array=[]
    # xx_array=[]
    # for i in range(0,300):
    #     xx=i/10
    #     f=pow(15*m1/(Energy_check*0.01), 3/2)*np.exp(-(m1*xx*xx)/(2*Energy_check*0.0015))*xx*xx
    #     f_array.append(f*100)
    #     xx_array.append(xx)
    # plt.scatter(xx_array, f_array, color='red',label=f'MaxMaxwell Distribution')



    plt.ylim(0, 100)
    plt.title('Speed distribution')
    plt.ylabel('Molecules')
    plt.xlabel('Speed')
    plt.legend()
    plt.draw()
    plt.pause(time_sleep)
    plt.clf()

    # эта часть кода необходима для вывода графиков в координатах PT, PV и графиков P(t), V(t), T(t) во время симуляции. Эти же графики выведутся в конце симуляции

    # plt.subplot(2, 3, 1)
    # plt.scatter(Temperature,Pressure,  label=f'Температура')
    # plt.xlabel('"Температура"*100')
    # plt.ylabel('Давление')
    # plt.title('P от Ek_sum')
    # plt.legend()
    # plt.grid(True)

    # plt.subplot(2, 3, 2)
    # plt.scatter(Volume,Pressure,  label=f'Давление')
    # plt.xlabel('Объем*1000')
    # plt.ylabel('Давление')
    # plt.legend()
    # plt.grid(True)

    # plt.subplot(2, 3, 3)
    # plt.scatter(Time_meas,Volume,  label=f'Объем')
    # plt.ylabel('Объем*1000')
    # plt.xlabel('Время')
    # plt.legend()
    # plt.grid(True)

    # plt.subplot(2, 3, 4)
    # plt.scatter(Time_meas,Pressure,  label=f'Давление')
    # plt.xlabel('Время')
    # plt.ylabel('Давление')
    # plt.legend()
    # plt.grid(True)

    # plt.subplot(2, 3, 5)
    # plt.scatter(Time_meas,Temperature,  label=f'Температура')
    # plt.ylabel('Температура')
    # plt.xlabel('Время')
    # plt.legend()
    # plt.grid(True)
    # plt.scatter(Temperature,Pressure,  label=f'asd')
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.xlabel('"Температура"*100')
    # plt.ylabel('Давление')
    # plt.title('P от Ek_sum')
    # plt.grid(which='both')
    # plt.legend()
    # plt.pause(time_sleep)
    # plt.draw()
    # plt.clf()        

    NOW_TIME+=time_sleep
    
    #print("Time ", round(NOW_TIME, 3))
    counter+=1


    if time_check<=-timer+NOW_TIME:

        # эта часть позволяет посмотреть давления на отдельные стенки
        '''
        print("Pressure right:  ", delta_px_left/(time_sleep*50*height))
        print("Pressure left:  ", delta_px_right/(time_sleep*50*height))
        print("Pressure up:  ", delta_py_up/(time_sleep*50*width))
        print("Pressure down:  ", delta_py_down/(time_sleep*50*width))
        '''
        Average_pressure=((delta_px_left+delta_px_right)/(time_check*height)+(delta_py_up+delta_py_down)/(time_check*width))/4 #среднее давление в сосуде рассчитывается как среднее давление на каждую стенку через изменение импульса за определенный промежуток времени
        '''nn*pi*(r1**2)   4*r1*r1'''
        print(str(round(float(height*width)-nn*pi*(r1**2),1))+"       "
              +str(round(Energy_check,3))+"         "
              +str(round(Average_pressure, 3))+"         "
              +str(round(mean(v),3))+"        "
              +str(round(NOW_TIME, 3))+"     "
              +Mode
            )
        # на данном этапе происходит сбор данных для дальнейшего отображения графиков
        Pressure.append(Average_pressure)
        Temperature.append(Energy_check/100)
        Volume.append((width*height-nn*pi*(r1**2))/1000)
        Time_meas.append(NOW_TIME)


        delta_px_left=0
        delta_px_right=0
        delta_py_up=0
        delta_py_down=0
        
        timer=NOW_TIME


# вывод конечных графиков
plt.tight_layout()
plt.show()
pygame.quit()

plt.subplot(2, 3, 1)
plt.scatter(Temperature,Pressure,  label=f'Температура')
plt.xlabel('"Температура"*100')
plt.ylabel('Давление')
plt.title('P от Ek_sum')
plt.legend()
plt.grid(True)

plt.subplot(2, 3, 2)
plt.scatter(Volume,Pressure,  label=f'Давление')
plt.xlabel('Объем*1000')
plt.ylabel('Давление')
plt.legend()
plt.grid(True)

plt.subplot(2, 3, 3)
plt.scatter(Time_meas,Volume,  label=f'Объем')
plt.ylabel('Объем*1000')
plt.xlabel('Время')
plt.legend()
plt.grid(True)

plt.subplot(2, 3, 4)
plt.scatter(Time_meas,Pressure,  label=f'Давление')
plt.xlabel('Время')
plt.ylabel('Давление')
plt.legend()
plt.grid(True)

plt.subplot(2, 3, 5)
plt.scatter(Time_meas,Temperature,  label=f'Температура')
plt.ylabel('Температура')
plt.xlabel('Время')
plt.legend()
plt.grid(True)

plt.show()
