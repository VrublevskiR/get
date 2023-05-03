import RPi.GPIO as GPIO
import time
from matplotlib import pyplot



    #ОБЪЯВЛЕНИЕ ГЛОБАЛЬНЫХ ПЕРЕМЕННЫХ

DAC = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(DAC)
levels = 2**bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4
weight = [128, 64, 32, 16, 8, 4, 2, 1]
LEDS = [24, 25, 8, 7, 12, 16, 20, 21]
LEDS1 = [21, 20, 16, 12, 7, 8, 25, 24]

    #ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКО GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)
GPIO.setup(LEDS, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(LEDS1, GPIO.OUT, initial = GPIO.LOW)
#GPIO.output(troykaModule, 1)
    #ПРЕВОД ИЗ ДЕСЯТИЧНОЙ В ДВОИЧНУЮ

def decimal2binary(value, n):
    return [int(element) for element in bin(value)[2:].zfill(n)]

    #ФНКЦИЯ РАБОТЫ С АЦП

def adc():
    summary = 0
    for value in range(8):
        signal = decimal2binary(summary + weight[value],8)
        GPIO.output(DAC, signal)
        time.sleep(0.01)
        if(GPIO.input(comparator) == 1):
            summary += weight[value]
        signal = decimal2binary(summary,8)
        for value in range(8):
            if (value < (summary / (levels - 1) * bits)):
                GPIO.output(LEDS[value], 1)
            else:
                GPIO.output(LEDS[value], 0)
        #voltage = summary / levels * maxVoltage
        
    return summary

try:

    #ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ И СПИСКОВ

    voltage=0
    result_of_experement=[]
    time_of_start=time.time()
    counter=0

    #ЗАРЯДКА КОНДЕНСАТОРА И ЗАПИСЬ ПОКАЗАНИЙ В ОПЕРАТИВНУЮ ПАМЯТЬ
        
    print('\n начало зарядки конденсатора\n')
    while voltage < 3.2:
        summary = adc()
        voltage = summary / levels * maxVoltage
        print('voltage = {}'.format(voltage))
        result_of_experement.append(voltage)
        time.sleep(0)
        counter+=1
        for value in range(8):
            if (value < (summary / (levels - 1) * bits)):
                GPIO.output(LEDS[value], 1)
            else:
                GPIO.output(LEDS[value], 0)

    GPIO.setup(troykaModule,GPIO.OUT, initial=GPIO.LOW)

    #ЗАРЯДКА КОНДЕНСАТОРА И ЗАПИСЬ ПОКАЗАНИЙ В ОПЕРАТИВНУЮ ПАМЯТЬ

    print('\n начало разрядки конденсатора\n')
    while voltage > 0.1:
        summary = adc()
        print('voltage = {}'.format(voltage))
        voltage = summary / levels * maxVoltage
        result_of_experement.append(voltage)
        time.sleep(0)
        counter+=1

        for value in range(8):
            if (value < (summary / (levels - 1) * bits)):
                GPIO.output(LEDS[value], 1)
            else:
                GPIO.output(LEDS[value], 0)

    time_of_experiment=time.time()-time_of_start

    #ЗАПИСЬ ДАННЫХ В ФАЙЛ

    print('\n запись данных в файл\n')
    with open('data.txt', 'w') as f:
        for i in result_of_experement:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write(str(1/time_of_experiment/counter) + '\n')
        f.write('0.01289')
    
    print('\n Общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации {} \n'.format(time_of_experiment, time_of_experiment/counter, 1/time_of_experiment/counter))

    #ПОСТРОЕНИЕ ГРАФИКА ЗАВИСИМОСТИ НАПРЯЖЕНИЯ НА КОНДЕНСАТОРЕ ОТ ВРЕМЕНИ V(t)

    print('\n построение графика\n')
    y=[i for i in result_of_experement]
    x=[i*time_of_experiment/counter for i in range(len(result_of_experement))]
    pyplot.figure (figsize = (8, 6), dpi = 200)
    pyplot.plot(x, y)
    pyplot.xlabel('time')
    pyplot.ylabel('Voltage')
    pyplot.savefig ("plt.png")
    pyplot.show()

finally:
    GPIO.output(LEDS, 0)
    GPIO.output(DAC, 0)
    GPIO.cleanup()
