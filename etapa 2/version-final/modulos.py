import random
import datetime
from validaciones import *
from modulologin import *

def inicializarDatos():
    # Estructura de turnos con doctores y horarios
    turnos = {
        "Nutricion": {
            "Dr. Pérez": {hora: 0 for hora in range(8, 12)},
            "Dra. Gómez": {hora: 0 for hora in range(12, 16)}
        },
        "Cardiologia": {
            "Dr. López": {hora: 0 for hora in range(8, 12)},
            "Dra. Torres": {hora: 0 for hora in range(12, 16)}
        },
        "Pediatria": {
            "Dr. Castro": {hora: 0 for hora in range(8, 12)},
            "Dra. Sosa": {hora: 0 for hora in range(12, 16)}
        },
        "Neurologia": {
            "Dr. Díaz": {hora: 0 for hora in range(8, 12)},
            "Dra. Morales": {hora: 0 for hora in range(12, 16)}
        },
        "Oftalmologia": {
            "Dr. Ruiz": {hora: 0 for hora in range(8, 12)},
            "Dra. Vega": {hora: 0 for hora in range(12, 16)}
        }
    }

    dias = list(turnos.keys())
    pacientes = {}
    nombres = set()
    docs = set()
    recaudos={}
    obras = {
        "Osde": 0.40,
        "Obsba": 0.35,
        "Medife": 0.30,
        "Pami": 0.25,
        "Particular": 0.00
    }

    return turnos, dias, pacientes, nombres, docs, obras , recaudos



def menuPrincipal(log, mail, turnos=None, dias=None, pacientes=None, nombres=None, docs=None, obras=None, recaudos=None):
    if turnos is None:
        turnos, dias, pacientes, nombres, docs, obras, recaudos = inicializarDatos()
    

    print("Bienvenido a la clínica Hoggins.")
        
    while True:
        try:
            opcion = input("1- Asignar turno\n2- Ver turnos\n3- Cargar pacientes\n4- Generar estadisticas\n5- Gestionar usuarios\n6- Salir: ").strip()

            if opcion == "":
                raise ValueError("No se permiten entradas vacías.")
            if not opcion.isdigit():
                raise ValueError("Ingrese un valor numérico.")
            opcion = int(opcion)
            if opcion < 1 or opcion > 6:
                raise ValueError("Opción fuera de rango (1-5).")
            break
        except ValueError as e:
                print("Error:", e)

    if opcion == 1:
        cargaTurnos(turnos, pacientes, nombres, docs, obras,recaudos)
        log.write(";".join([mail, str(datetime.datetime.now()), "Cargo un turno"]) + "\n")
        return menuPrincipal(log, mail, turnos, dias, pacientes, nombres, docs, obras, recaudos)
    elif opcion == 2:
        mostrarTurnos(turnos)
        log.write(";".join([mail, str(datetime.datetime.now()), "Imprimio los turnos"]) + "\n")
        return menuPrincipal(log, mail, turnos, dias, pacientes, nombres, docs, obras, recaudos)
    elif opcion == 3:
        cargarPacientes("historiaclinica.csv", pacientes, obras)
        log.write(";".join([mail, str(datetime.datetime.now()), "Cargo un paciente"]) + "\n")
        return menuPrincipal(log, mail, turnos, dias, pacientes, nombres, docs, obras, recaudos)
    elif opcion ==4:
        generarestadisticas(turnos, pacientes, nombres, docs, obras,recaudos)
        log.write(";".join([mail, str(datetime.datetime.now()), "Genero las estadisticas"]) + "\n")
        return menuPrincipal(log, mail, turnos, dias, pacientes, nombres, docs, obras, recaudos)
    elif opcion ==5:
        gestiondeusuarios()
        log.write(";".join([mail, str(datetime.datetime.now()), "Abrio gestion de usuarios"]) + "\n")
        return menuPrincipal(log, mail, turnos, dias, pacientes, nombres, docs, obras, recaudos)
    elif opcion == 6:
        print("Hasta mañana.")
        log.write(";".join([mail, str(datetime.datetime.now()), "Cerro sesion"]) + "\n")
        return

    
def cargarPacientes(dato, pacientes, obras):
    #carga pacientes al archivo historia clinica
    try:
        arch = open(dato, 'at')
    except IOError:
        print("Error al abrir el archivo.")
    else:
        while True:
            try:
                nombre = validacion_texto("Ingrese solo su apellido (ENTER para finalizar): ")
                if nombre == "":
                    break

                dni = validarnumerolen(7, 8, "Ingrese su DNI (7 a 8 dígitos): ")

                paciente_id = str(random.randint(1, 100))
                while paciente_id in pacientes:
                    paciente_id = str(random.randint(1, 100))

                while True:
                    try:
                        obra = input(f"Ingrese su obra social ({', '.join(obras.keys())}): ").strip().capitalize()
                        if obra not in obras:
                            raise ValueError("Obra social no válida. Intente nuevamente.")
                        break
                    except ValueError as e:
                        print("Error:", e)

                pacientes[paciente_id] = {"nombre": nombre, "dni": dni, "obra": obra}

                linea = ";".join([nombre, dni, paciente_id, obra])
                arch.write(linea + '\n')
                print(f"Paciente {nombre} cargado con ID {paciente_id}.\n")

            except ValueError as e:
                print("Error:", e)

        arch.close()                
                

def cargaTurnos(turnos, pacientes, nombres, docs, obras, recaudos):
    #pide el id y llama a otras funciones
    while True:
        try:
            idpac = input("Ingrese el ID del paciente (ENTER para salir): ").strip()
            if idpac == "":
                break
            if not idpac.isdigit():
                raise ValueError("El ID debe ser numérico.")

            paciente = buscarpaciente(idpac)
            if paciente is None:
                print("Paciente no encontrado.\n")
                continue

            especialidad = seleccionar_especialidad(turnos)
            doctor = seleccionar_doctor(turnos, especialidad)
            hora = seleccionar_hora(turnos, especialidad, doctor)

            asignar_turno(turnos, especialidad, doctor, hora, idpac, {idpac: paciente}, obras, recaudos)

        except ValueError as e:
            print("Error:", e)



def buscarpaciente(idpac, archivo="historiaclinica.csv"):
    #comprueba la existencia de el id en historia clinica
    paciente_encontrado = None
    try:
        with open(archivo, "rt") as arch:
            for linea in arch:
                partes = linea.strip().split(";")
                if len(partes) == 4:
                    nombre, dni, pid, obra = partes
                    if pid == idpac:
                        paciente_encontrado = {"nombre": nombre, "dni": dni, "obra": obra}
                        
    except FileNotFoundError:
        print("Archivo de pacientes no encontrado.")
    except IOError:
        print("Error al leer el archivo de pacientes.")

    return paciente_encontrado


        
    

    
    
def seleccionar_especialidad(turnos):
    #permite elegir la especialidad
    print("\nEspecialidades disponibles:")
    for espec in turnos.keys():
        print("-", espec)
    while True:
        try:
            especialidad = input("Ingrese la especialidad del turno: ").strip().capitalize()
            if especialidad.isdigit():
                raise ValueError("la entrada no puede ser numerica")
            if especialidad not in turnos:
                raise ValueError("Especialidad no válida.")
            break
        except ValueError as e:
            print("ERROR:",e)
    return especialidad

def seleccionar_doctor(turnos, especialidad):
    #permite elegir el doctor

    doc1, doc2 = turnos[especialidad].keys()

    print(f"\nDoctores disponibles en {especialidad}:")
    print(f"1- {doc1}")
    print(f"2- {doc2}")
    while True:
        try:
            indice = input("Seleccione el doctor (1 o 2): ").strip()
            if indice=="":
                raise ValueError("el ingreso no puede estar vacio")
            if not indice.isdigit():
                raise ValueError("el valor debe ser numerico")
            indice=int(indice)
            if indice<1 or indice>2:
                raise ValueError("El valor solo puede ser 1 o 2")
            break
        except ValueError as e:
            print("Error:",e)
    if indice==1:
        doc=doc1
    else:
        doc=doc2
    return doc



def seleccionar_hora(turnos, especialidad, doctor):
    #permite selecionar la hora
    while True:
        try:
            print(f"\nHoras disponibles con {doctor}:")
            for hora, estado in turnos[especialidad][doctor].items():
                if estado==0:
                    print(f"{hora}hs - libre")
                else:
                    print(f"{hora}hs - ocupado")
             
            hora = input("Ingrese la hora del turno: ").strip()
            if not hora.isdigit():
                raise ValueError("La hora debe ser numérica.")
            
            hora = int(hora)
            if hora not in turnos[especialidad][doctor]:
                raise ValueError("Hora no válida.")
                
            if turnos[especialidad][doctor][hora] != 0:
                raise ValueError("Horario ocupado. Intente otro.")
            break
        except ValueError as e:
            print("EEROR:",e)
            
    return hora

def asignar_turno(turnos, especialidad, doctor, hora, idpac, pacientes, obras, recaudos):
    # asigna el turno y cuenta los recaudos para tesoreria
    turnos[especialidad][doctor][hora] = idpac
    obra = pacientes[idpac]["obra"]
    descuento = obras.get(obra, 0)
    monto_base = 1000.0
    monto_final = monto_base - (monto_base * descuento)

    if especialidad not in recaudos:
        recaudos[especialidad] = monto_final
    else:
        recaudos[especialidad] += monto_final

    print(f"\n Turno asignado correctamente:")
    print(f"  Especialidad: {especialidad}")
    print(f"  Doctor: {doctor}")
    print(f"  Hora: {hora}hs")
    print(f"  Paciente: {pacientes[idpac]['nombre']}")
    print(f"  Monto a pagar: ${monto_final:.2f} ({obra})")

    





def mostrarTurnos(turnos):
    #muestra los turnos y sus estados
    for esp in turnos:
        print(f"\nEspecialidad: {esp}")
        for doc in turnos[esp]:
            print(f"  Doctor: {doc}")
            for hora in sorted(turnos[esp][doc]):
                paciente = turnos[esp][doc][hora]
                estado = paciente if paciente != 0 else "Libre"
                print(f"    {hora}hs -> {estado}")
                
                
def generarestadisticas(turnos, pacientes, nombres, docs, obras,recaudos):
    #llama a las funciones que escriben algunos archivos 
    generarPorcentajeMedico(turnos)
    cargarTesoreria(recaudos)
    estadisticaobras(turnos)
    

def generarPorcentajeMedico(turnos):
    contdoctores = {}
    total_turnos = 0

    for especialidad in turnos:
        for doctor in turnos[especialidad]:
            for hora, paciente in turnos[especialidad][doctor].items():
                if paciente != 0:
                    contdoctores[doctor] = contdoctores.get(doctor, 0) + 1
                    total_turnos += 1

    if total_turnos == 0:
        print("No hay turnos registrados para generar el reporte.")
    else:  

    
        porcentajes = {doctor: (cantidad / total_turnos) * 100 for doctor, cantidad in contdoctores.items()}

    
        lista_doctores = sorted(contdoctores.items(), key=lambda x: x[1], reverse=True)

        try:
            with open("porcentajes.csv", "wt") as porc:
                porc.write("Doctor;Cantidad de Turnos;Porcentaje\n")
                for doctor, cantidad in lista_doctores:
                    porc.write(f"{doctor};{cantidad};{porcentajes[doctor]:.2f}\n")
            print("Archivo de porcentajes generado correctamente.\n")
        except IOError:
            print("Error al escribir el archivo de porcentajes.")

        



def cargarTesoreria(recaudos):
    try:
        with open("tesoreria.csv", "wt") as arch:
            arch.write("Especialidad;Monto Recaudado\n")
            for especialidad, monto in recaudos.items():
                arch.write(f"{especialidad};{monto:.2f}\n")
        print("Archivo de tesorería generado correctamente.")
    except IOError:
        print("No se pudo abrir o escribir el archivo de tesorería.")


            
def estadisticaobras(turnos):
    conteo = {}
    total = 0

    try:
        with open("historiaclinica.csv", "rt") as arch:
            for linea in arch:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(";")
                if len(partes) < 4:
                    continue
                obra = partes[3].strip()
                conteo[obra] = conteo.get(obra, 0) + 1
                total += 1
    except IOError:
        print("No se puede abrir el archivo 'historiaclinica.csv'.")
        return

    if total == 0:
        print("El archivo está vacío o no contiene registros válidos de obra social.")
        return

    lista = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    try:
        with open("obras_sociales.csv", "wt") as arch:
            arch.write("Obra Social;Cantidad;Porcentaje\n")
            for obra_key, cantidad in lista:
                pct = (cantidad / total) * 100
                arch.write(f"{obra_key};{cantidad};{pct:.2f}\n")
        print("\nArchivo 'obras_sociales.csv' generado correctamente.")
    except IOError:
        print("No se pudo crear/escribir 'obras_sociales.csv'.")
