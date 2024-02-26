#Con funcionalidad igual que el otro código. Únicamente creado para realizar las pruebas de 6 instrucciones. 
import random
import simpy
import statistics as stats
RandomSeed = 77
env = simpy.Environment()

random.seed(RandomSeed)
QTY_Procesos = 200   #Sujeto a cambios durante cada intento
RawInterval = 10    #Sujeto a cambos durante cada intento
RAM = simpy.Container(env, init=100,capacity=100)
CPU = simpy.Resource(env,capacity=1)    
duracionTotal = []      

def source(env,qty,counter,ram):
    
    asignado= {}
    for i in range(qty):
        needed_ram = random.randint(1,10)
        instructions = random.randint(1,10)
        p = execute(env,'Proceso%02d' %i, counter,ram,needed_ram,instructions,asignado)
        env.process(p)
        Interval_Procesos = random.expovariate(1.0/RawInterval)
        t = Interval_Procesos
        yield env.timeout(t)


def execute(env,ID,counter,ram,needed_ram,instructions,asignado):
    duracion = 0
    arrive = env.now
    print('%7.4f %s: Nuevo proceso' %(arrive,ID))
    print("Instrucciones: ", instructions, "RAM: ", needed_ram)
    asignado[ID] = False
    while instructions > 0:
        print("RAM DISPONIBLE:", ram.level)
        if ram.level < needed_ram:
            print('%7.4f %s: Esperando RAM...' % (env.now, ID))
            yield ram.get(needed_ram)  # Esperar llegada de ram. 
            print('%7.4f %s: Obtenida RAM' % (env.now, ID))
            asignado[ID] = True  
        else:
            ram.get(needed_ram)
            print('%7.4f %s: Obtenida RAM' % (env.now, ID))
            asignado[ID] = True

        with counter.request() as req:
            yield req
            print('%7.4f %s: desde que llegó a CPU han pasado %6.3f' % (env.now, ID, env.now - arrive))
            while instructions > 0:
                if instructions >= 6:   #Resto del código, modificado para 6:
                    yield env.timeout(6)
                    instructions -= 6
                    print("CPU Realizó 6 instrucciones con", ID)
                    decide = random.randint(1,2)
                    if decide == 1:
                        tiempoIO = random.expovariate(1/random.randint(1,3))    #La guía no especificaba explícitamente cómo manejar la I/O, entonces consideré que un pequeño random era lo más ideal.
                        yield env.timeout(tiempoIO)
                        print("Fue a I/O y recibió una señal después de",tiempoIO)
                    elif decide == 2:
                        print(ID,"regresó a ready at ", env.now)

                elif instructions == 5:
                    yield env.timeout(5)
                    instructions -= 5
                    print("CPU Realizó 5 instrucciones con", ID)
                elif instructions == 4:
                    yield env.timeout(4)
                    instructions -= 4
                    print("CPU Realizó 4 instrucciones con", ID)
                elif instructions == 3:
                    yield env.timeout(3)
                    instructions -= 3
                    print("CPU Realizó 3 instrucciones con", ID)
            
                elif instructions == 2:
                    yield env.timeout(2)
                    instructions -= 2
                    print("CPU Realizó 2 instrucciones con", ID)
                elif instructions == 1:
                    yield env.timeout(1)
                    instructions -= 1
                    print("CPU Realizó 1 instrucción con", ID)
                if instructions == 0:
                    print('%7.4f %s: Terminó el proceso' % (env.now, ID))
                    ram.put(needed_ram)  
                    print(asignado)
                    duracion = env.now-arrive
                    print("Tiempo de vida del proceso: ", duracion)
                    global duracionTotal
                    duracionTotal.append(duracion)



print("Analizador de procesos Simpy: \n")
env.process(source(env,QTY_Procesos,CPU,RAM))
env.run()
print("\n")
print("Duración de todos los procesos: ",sum(duracionTotal))
print("Media de todos los procesos: ", stats.mean(duracionTotal))
print("Desviacion estándar de todos los procesos: ", stats.stdev(duracionTotal))