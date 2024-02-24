import random
import simpy
RandomSeed = 77
env = simpy.Environment()

random.seed(RandomSeed)
QTY_Procesos = 5   #Sujeto a cambios durante cada intento
RawInterval = 10    #Sujeto a cambos durante cada intento
#RAM = simpy.Container(env, init=5,capacity=5)
RAM = simpy.Container(env, init=100,capacity=100)
CPU = simpy.Resource(env,capacity=1)    #Sujeto a cambios durante cada intento

def source(env,qty,counter,ram):
    for i in range(qty):
        needed_ram = random.randint(1,10)
        instructions = random.randint(1,10)
        p = execute(env,'Proceso%02d' %i, counter,ram,needed_ram,instructions)
        env.process(p)
        Interval_Procesos = random.expovariate(1.0/RawInterval)
        t = Interval_Procesos
        yield env.timeout(t)


def execute(env,ID,counter,ram,needed_ram,instructions):
    arrive = env.now
    print('%7.4f %s: Nuevo proceso' %(arrive,ID))
    print(instructions)
    
    if ram.capacity > needed_ram:
        ram.get(needed_ram)
        while instructions >0:
            with counter.request() as req:
                yield req
                if req.triggered:
                    print('%7.4f %s: desde que llegó a CPU han pasado %6.3f' %(env.now,ID, env.now-arrive))
                    if instructions >= 3:
                        instructions = instructions-3
                        yield env.timeout(3)
                        decide = random.randint(1,2)
                        print("CPU Realizó 3 instrucciones con ",ID)
                        if decide == 1:
                            tiempoIO = random.expovariate(1/random.randint(1,3))
                            yield env.timeout(tiempoIO)
                            print("Fue a I/O y recibió una señal después de",tiempoIO)
                        elif decide == 2:
                            print(ID,"regresó a ready at ", env.now)
                    elif instructions == 2:
                        yield env.timeout(2)
                        instructions = instructions-2
                        print("CPU Realizó 2 instrucciones", ID)
                    elif instructions == 1:
                        yield env.timeout(1)
                        instructions = instructions-1
                        print("CPU Realizó 1 instruccion",ID)
            if instructions == 0:
                print('%7.4f %s: Terminó el proceso' %(env.now,ID))
                ram.put(needed_ram)


print("Analizador de procesos Simpy: \n")
env.process(source(env,QTY_Procesos,CPU,RAM))
env.run()


                

