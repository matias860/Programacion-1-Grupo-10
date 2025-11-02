import random
import datetime

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
    obras = {
        "Osde": 0.40,
        "Swiss Medical": 0.35,
        "Medife": 0.30,
        "Pami": 0.25,
        "Particular": 0.00
    }

    return turnos, dias, pacientes, nombres, docs, obras

def crearArchivoUsuarios():
    correos = ["matiabeledo@gmail.com", "joseperez@gmail.com", "ricardothompson@gmail.com", "kevin@gmail.com", "franco@gmail.com"]
    contras = []

    for _ in range(5):
        contra = ""
        for i in range(6):
            cadena = "abcdefghijklmnopqrstuvwxyz0123456789"
            contra += cadena[random.randint(0, len(cadena) - 1)]
        contras.append(contra)
        
    try:
        arch = open("usuarios.csv", "wt")
    except IOError:
        print("Error al crear el archivo de usuarios.")
        return -1
    else:
        for i in range(5):
            arch.write(correos[i] + ";" + contras[i] + "\n")
        arch.close()
        

def menuPrincipal(log, mail):
    turnos, dias, pacientes, nombres, docs, obras = inicializarDatos()
    print("Bienvenido a la clínica Hoggins.")
        
    while True:
        try:
            opcion = input("1- Asignar turno\n2- Ver turnos\n3- Cargar pacientes\n4- Salir: ").strip()

            if opcion == "":
                raise ValueError("No se permiten entradas vacías.")
            if not opcion.isdigit():
                raise ValueError("Ingrese un valor numérico.")
            opcion = int(opcion)
            if opcion < 1 or opcion > 4:
                raise ValueError("Opción fuera de rango (1-4).")

            if opcion == 1:
                cargaTurnos(turnos, pacientes, nombres, docs, obras)
                log.write(";".join([mail, str(datetime.datetime.now()), "Cargo un turno"]) + "\n")
            elif opcion == 2:
                    mostrarTurnos(turnos)
                    log.write(";".join([mail, str(datetime.datetime.now()), "Imprimio los turnos"]) + "\n")
            elif opcion == 3:
                cargarPacientes("historiaclinica.csv", pacientes, obras)
                log.write(";".join([mail, str(datetime.datetime.now()), "Cargo un paciente"]) + "\n")
            elif opcion == 4:
                print("Hasta mañana.")
                log.write(";".join([mail, str(datetime.datetime.now()), "Cerro sesion"]) + "\n")
                break

        except ValueError as e:
                print("Error:", e)
                
                
def validacion_texto(text):
    while True:
            try:
                texto= input(text).strip()
                if texto == "":
                    break
                if not all(c.isalpha() or c.isspace() for c in texto):
                    raise ValueError("El ingreso solo puede contener letras.")
                break
            except ValueError as e:
                print("ERROR:",e)
    return texto    

def validarnumero(largo_min,largo_max,msj):
    while True:
        try:
            num= input(msj).strip()
            if num== "":
                raise ValueError("la entrada no puede ser vacio")
            if not num.isdigit():
                raise ValueError("El ingreso debe ser numerico.")
            if len(num)<largo_min or len(num)>largo_max:
                raise ValueError("fuera de el rango especificado")
            break
        except ValueError as e:
            print("ERROR:",e)
    return num

def cargarPacientes(dato, pacientes, obras):
    try:
        arch = open(dato, 'at')
    except IOError:
        print("Error al abrir el archivo.")
    else:
        while True:
            try:
                nombre = validacion_texto("Ingrese su nombre completo vacio para finalizar): ")
                if nombre=="":
                    break

                else:
                    dni = validarnumero(7,8,"ingrese su dni, porfavor de 7 a 8 digitos")
                    
                    paciente_id = str(random.randint(1, 100))
                    while paciente_id in pacientes:
                        paciente_id = str(random.randint(1, 100))
                    pacientes["id"]=paciente_id
                    
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

            except ValueError as e:
                print("Error:", e)
                
        arch.close()
        


def cargaTurnos(turnos, pacientes, nombres, docs, obras):
    while True:
        try:
            idpac = input("Ingrese el ID del paciente (ENTER para salir): ").strip()
            if idpac == "":
                break
            if not idpac.isdigit():
                raise ValueError("El ID debe ser numérico.")

           
            paciente =buscarpaciente(idpac, pacientes)
            if paciente==':(':
                break
            else:
                especialidad = seleccionar_especialidad(turnos)
                doctor = seleccionar_doctor(turnos, especialidad)
                hora = seleccionar_hora(turnos, especialidad, doctor)

                asignar_turno(turnos, especialidad, doctor, hora, idpac, pacientes, obras)

        except ValueError as e:
            print("Error:", e)

def buscarpaciente(idpac, pacientes):
    if idpac in pacientes:
        estado=pacientes[idpac]  
    else:
        print("Paciente no encontrado.")
        estado=':('
    return estado
        
        
    
        
    

    
    
def seleccionar_especialidad(turnos):
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

def asignar_turno(turnos, especialidad, doctor, hora, idpac, pacientes, obras):

    turnos[especialidad][doctor][hora] = idpac
    obra = pacientes[idpac]["obra"]
    descuento = obras.get(obra, 0)
    monto_base = 1000
    monto_final = monto_base - (monto_base * descuento)

    print(f"\n Turno asignado correctamente:")
    print(f"  Especialidad: {especialidad}")
    print(f"  Doctor: {doctor}")
    print(f"  Hora: {hora}hs")
    print(f"  Paciente: {pacientes[idpac]['nombre']}")
    print(f"  Monto a pagar: ${monto_final:.2f} ({obra})")

 





def mostrarTurnos(turnos):
    for esp in turnos:
        print(f"\nEspecialidad: {esp}")
        for doc in turnos[esp]:
            print(f"  Doctor: {doc}")
            for hora in sorted(turnos[esp][doc]):
                paciente = turnos[esp][doc][hora]
                estado = paciente if paciente != 0 else "Libre"
                print(f"    {hora}hs -> {estado}")
