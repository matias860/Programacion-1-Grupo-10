import random
from validaciones import *
def crearArchivoUsuarios():
    #crea usuarios en el caso que no haya ninguno cargado
    
        correos = [
            "matiabeledo@gmail.com",
            "joseperez@gmail.com",
            "ricardothompson@gmail.com",
            "kevin@gmail.com",
            "franco@gmail.com"
        ]
        se=verificarexistencia(correos)
        if se==1:
            print()
        else:
        
            cadena = "abcdefghijklmnopqrstuvwxyz0123456789"
            contras = []
            for _ in range(5):
                contra = ""
                cadena = "abcdefghijklmnopqrstuvwxyz0123456789"
                contra = "".join([cadena[random.randint(0, len(cadena) - 1)] for _ in range(6)])
                contras.append(contra)

            try:
                arch = open("usuarios.csv", "at")
            except IOError:
                print("Error al crear el archivo de usuarios.")
            else:
                for i in range(5):
                    arch.write(correos[i] + ";" + contras[i] + "\n")
                arch.close()
                
def verificarexistencia(correos):
    #verifica si existe al menos un usuario, de lo contrario crear usuarios crea 5 predeterminados
    sig = 0
    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("No se encontró el archivo de usuarios")
    else:
        
        for linea in arch:
            correo_archivo = linea.strip().split(";")[0]
            for correo in correos:
                if correo == correo_archivo:
                    sig = 1  
        arch.close()
    
    
    return sig

def validar(mail, password, archivo="usuarios.csv"):
    #se llama desde main para validar el ingreso al sistema
    valido = False
    try:
        with open(archivo, "rt") as arch:
            for linea in arch:
                partes = linea.strip().split(";")
                if len(partes) == 2:
                    usuario, contra = partes
                    if usuario == mail and contra == password:
                        valido = True
                
    except FileNotFoundError:
        print("No se encontró el archivo de usuarios.")
    except IOError:
        print("Error al abrir el archivo.")

    return valido

def gestiondeusuarios():
    #menu de gestionar usuarios
    claveUS="CLINICA2025"
    dominios= {1: "@gmail.com", 2: "@hotmail.com", 3: "@outlook.com"}
    intentos=3
    opci=validarentradanumerica(1,4,"1- Dar de alta un usuario\n2- Modificar un usuario\n3- Dar de baja un usuario\n4- Volver a inicio")
    if opci == 1:
            Altausuario(claveUS, dominios)
    elif opci == 2:
        modificarusuario(claveUS, dominios)
    elif opci == 3:
        bajausuario(claveUS, dominios)
    else:
        print("Volviendo al menú principal...")
        menuPrincipal() 

def Altausuario(clave, dominios):
    #funcion que da de alta los usuarios
    exito = "no"
    dominio = validarentradanumerica(1, 3, "Ingrese la opción que corresponde a su dominio:\n1- @gmail.com\n2- @hotmail.com\n3- @outlook.com: ")
    altamail = validacion_text("Ingrese su mail sin el dominio: ")
    alcontra = validar_alfadigit("Ingrese una contraseña (debe contener letras y números):")

    while True:
        valclave = input("Ingrese la clave del sistema para dar de alta su usuario (deje vacío para cancelar): ").strip()
        if valclave == "":
            print("Operación cancelada por el usuario.")
            break
        if valclave == clave:
            mailfinal = altamail + dominios[dominio]
            existe = False
            try:
                arch = open("usuarios.csv", "rt")
            except IOError:
                print("No se pudo abrir el archivo")
            else:
                for linea in arch:
                    partes = linea.strip().split(";")
                    if len(partes) > 0 and partes[0] == mailfinal:
                        existe = True
                arch.close()
            
                

            if existe:
                print("Ya existe un usuario con ese mail. No se pudo dar de alta.")
            else:
                try:
                    arch = open("usuarios.csv", "at")
                except IOError:
                    print("No se pudo dar de alta al usuario por un problema del archivo.")
                else:
                    arch.write(mailfinal + ";" + alcontra + "\n")
                    arch.close()
                    print("Usuario generado con éxito:", mailfinal)
                    exito = "si"
                
            break
        else:
            print("Clave incorrecta. Intente nuevamente.")

    if exito == "no":
        print("No se generó ningún usuario.")


def modificarusuario(clave, dominios):
    #funcion para modificar usuarios
    exito = "no"

    while True:
        try:
            mail_a_buscar = input("Ingrese el mail completo del usuario a modificar: ").strip()
            if mail_a_buscar == "":
                raise ValueError("Operación cancelada por el usuario.")
            break
        except ValueError as o:
            print("ERROR:", o)

    try:
        arch = open("usuarios.csv", "rt")
        lineas = [l.strip() for l in arch]
        arch.close()
    except IOError:
        print("No se pudo abrir el archivo de usuarios.")
        lineas = []

    indice_encontrado = None
    for i in range(len(lineas)):
        partes = lineas[i].split(";")
        if len(partes) > 0 and partes[0] == mail_a_buscar:
            indice_encontrado = i

    if indice_encontrado is None:
        print("No se encontró el usuario con ese mail.")
    else:
        autorizado = False
        while True:
            valclave = input("Ingrese la clave del sistema (deje vacío para cancelar): ").strip()
            if valclave == "":
                print("Operación cancelada por el usuario.")
                break
            if valclave == clave:
                autorizado = True
                break
            else:
                print("Clave incorrecta. Intente nuevamente.")

        if autorizado:
            print("Usuario encontrado:", lineas[indice_encontrado])
            opcion = validarentradanumerica(1, 3, "Qué desea modificar?\n1- Cambiar mail\n2- Cambiar contraseña\n3- Cancelar")

            if opcion == 1:
                nueva_parte = validacion_text("Ingrese el nuevo mail sin el dominio: ")
                dominio_opc = validarentradanumerica(1, 3, "Seleccione el dominio:\n1- @gmail.com\n2- @hotmail.com\n3- @outlook.com: ")
                nuevo_mail = nueva_parte + dominios[dominio_opc]

                existe = False
                for l in lineas:
                    partes = l.split(";")
                    if len(partes) > 0 and partes[0] == nuevo_mail:
                        existe = True

                if existe:
                    print("Ya existe un usuario con ese mail. No se realizó la modificación.")
                else:
                    partes = lineas[indice_encontrado].split(";", 1)
                    passwd = partes[1] if len(partes) == 2 else ""
                    lineas[indice_encontrado] = nuevo_mail + ";" + passwd
                    try:
                        arch = open("usuarios.csv", "w")
                        for l in lineas:
                            arch.write(l + "\n")
                        arch.close()
                        print("Mail modificado con éxito a:", nuevo_mail)
                        exito = "si"
                    except IOError:
                        print("Error al guardar el archivo.")

            elif opcion == 2:
                nueva_pass = validar_alfadigit("Ingrese la nueva contraseña: ")
                mail_actual = lineas[indice_encontrado].split(";", 1)[0]
                lineas[indice_encontrado] = mail_actual + ";" + nueva_pass
                try:
                    arch = open("usuarios.csv", "w")
                    for l in lineas:
                        arch.write(l + "\n")
                    arch.close()
                    print("Contraseña modificada con éxito para:", mail_actual)
                    exito = "si"
                except IOError:
                    print("Error al guardar el archivo.")
            else:
                print("Operación cancelada.")

    if exito == "no":
        print("No se realizaron cambios.")


def bajausuario(clave, dominios):
    #funcion para dar de baja a los usuarios
    exito = "no"
    while True:
        mail_a_borrar = input("Ingrese el mail completo del usuario a dar de baja: ").strip()
        if mail_a_borrar == "":
            print("Operación cancelada por el usuario.")
            break
        else:
            break

    try:
        arch = open("usuarios.csv", "rt")
        lineas = [l.strip() for l in arch]
        arch.close()
    except IOError:
        print("No se pudo abrir el archivo de usuarios.")
        lineas = []

    indice_encontrado = None
    for i in range(len(lineas)):
        partes = lineas[i].split(";")
        if len(partes) > 0 and partes[0] == mail_a_borrar:
            indice_encontrado = i

    if indice_encontrado is None:
        print("No se encontró el usuario con ese mail.")
    else:
        autorizado = False
        while True:
            valclave = input("Ingrese la clave del sistema para dar de baja el usuario (deje vacío para cancelar): ").strip()
            if valclave == "":
                print("Operación cancelada por el usuario.")
                break
            if valclave == clave:
                autorizado = True
                break
            else:
                print("Clave incorrecta. Intente nuevamente.")

        if autorizado:
            usuario_borrado = lineas[indice_encontrado]
            lineas.pop(indice_encontrado)
            try:
                arch = open("usuarios.csv", "w")
                for l in lineas:
                    arch.write(l + "\n")
                arch.close()
                print("Usuario dado de baja correctamente:", usuario_borrado.split(";")[0])
                exito = "si"
            except IOError:
                print("Error al escribir el archivo.")

    if exito == "no":
        print("No se realizaron cambios.")