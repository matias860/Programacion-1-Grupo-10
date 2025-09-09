import random

def inicializarDatos():
    #inicia las listas y la matriz
    
    dias = ["Lunes(Nutricion)", "Martes(Cardiologia)", "Miercoles(Pediatria)",
            "Jueves(Neurologia)", "Viernes(oftalmologia)"]
    pacientes = []
    turnos = [[0]*8 for _ in range(5)]
    return turnos, dias, pacientes

def cargaTurnos(turnos, pacientes):
    #elegimos la especialidad y cargamos el turno
    print()
    consul = int(input("Indique la especialidad en la que desea reservar un turno\n1- Nutricion (Lunes) \n2- Cardiologia (Martes) \n3- Pediatria (Miercoles) \n4- Neurologia (Jueves) \n5- Oftalmología (Viernes) \nSeleccione: "))
    while consul<1 or consul>5:
        consul = int(input("Consultorio invalido, Indique la especialidad en la que desea reservar un turno\n1- Nutricion (Lunes) \n2- Cardiologia (Martes) \n3- Pediatria (Miercoles) \n4- Neurologia (Jueves) \n5- Oftalmología (Viernes) \nSeleccione: "))    
    
    mostrarDisponibilidad(turnos, consul)
    
    hora = int(input("Ingrese hora (8-15): "))
    while hora < 8 or hora > 15 or turnos[consul-1][hora-8] != 0:
        hora= int(input("ERROR. Ingrese una hora valida (8-15) y/o LIBRE: "))
    paciente_id = random.randint(1, 100)
    while paciente_id in pacientes:
        paciente_id = random.randint(1, 100)
        
    pacientes.append(paciente_id)
        

    if asignarTurnos(turnos, consul, hora, paciente_id):
        print("Turno asignado correctamente.")
    else:
        print("Ese turno ya está ocupado.")
        
def mostrarDisponibilidad(turnos, consul):
    #mostramos la disponibilidad de los turnos

    print(f"\nhorarios disponibles para el consultorio {consul}")
    for h in range(8):
        if turnos [consul-1][h] == 0:
            print(f"  - {h+8}hs")

def asignarTurnos(turnos, consul, hora, paciente_id):
    #funcion que asigna los turnos
    
    c, h = consul - 1, hora - 8
    if turnos[c][h] == 0:
        turnos[c][h] = paciente_id
        return True
    return False

def mostrarTurnos(turnos, dias):
    #funcion para mostrar los turnos
    for c in range(5):
        print("Consultorio ", c+1)
        for h in range(8):
            if turnos[c][h] != 0:
                print("   Dia ", dias[c], "Hora ", h+8, ", numero de paciente:", turnos[c][h])

                
def resumen(turnos,dias, pacientes):
    #funcion que llama otras funciones correspondientes al resumen
    print()
    sinreservas(turnos,dias)
    print()
    mayorPacientes(turnos, dias)
    print()
    menorpacientes(turnos, dias)
    print()
    promediototal(turnos, dias)
    print()
    pacientes_conturno(pacientes,turnos)
    print()
    turnos_pordia(turnos,dias)

def sinreservas(turnos, dias):
    #buscamos las especialidades que no tengan reserva
    
    print("Especialedades sin reservas")
    noreservadas=[]
    for i in range(len(turnos)):
        cont=0
        for hora in turnos[i]:
            if hora == 0:
                cont+=1
        if cont==8:
            noreservadas.append(dias[i])
    print(noreservadas)

def mayorPacientes(turnos, dias):
    #muestra el consultorio con la mayor cantidad de pacientes
    
    ocupados = [sum(1 for x in fila if x != 0) for fila in turnos]
    max_turnos = max(ocupados)
    inicio= 0
    for i in range(len(ocupados[1:])):
        indice= i + 1                   
        if ocupados[indice] == max_turnos:
            inicio= indice

    print("El consultorio con más pacientes es:", dias[inicio],
          "con", max_turnos, "pacientes")

    
    
def promediototal(turnos, dias):
    #calcula el promedio total de todos los turnos
    suma=0
    for i in range(len(turnos)):
        for hora in turnos[i]:
            if hora != 0:
                suma=suma+1
    totaldeturnos=(len(turnos))*(len(turnos[0]))
    prom=suma/totaldeturnos
    print("el promedio de el total de los turnos es",prom * 100,"%")
                
def pacientes_conturno(pacientes,turnos):
    #muestra una lista ordenada por numero de id de los pacientes con turno
    pacientes.sort()
    print("Pacientes ordenados por numero de id",pacientes)
        
def turnos_pordia(turnos, dias):
    #muestra los turnos por dia
    for i in range(len(turnos)):
        print(f"\n{dias[i]}:")
        cant=0
        for h in range(len(turnos[i])):
            if turnos[i][h] !=0:
                cant+=1
        if cant!=0:
            print("cantidad de turnos es",cant)
        else:
            print("no tuvo turnos")
                
def menorpacientes(turnos, dias):
    #muestra el consultorio con menor numero de pacientes
    
    tur_ocupados = lambda fila: sum(1 for x in fila if x != 0)
    menor = tur_ocupados(turnos[0])
    indice = 0
    for i in range(1, len(turnos)):
        if tur_ocupados(turnos[i]) < menor:
            menor = tur_ocupados(turnos[i])
            indice = i
    print("El consultorio con menos pacientes es:", dias[indice],
          "con", menor, "pacientes")