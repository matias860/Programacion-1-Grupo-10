from modulos import menuPrincipal
from modulologin import crearArchivoUsuarios, validar
import datetime

def main():
    #inicio de programa
    crearArchivoUsuarios() 

    try:
        log = open("log.csv", "at")
    except IOError:
        print("No se pudo abrir el archivo de log.")

    else: 
        acceso = False
        while not acceso:
            print("=== LOGIN DE USUARIO ===")
            mail = input("Ingrese su mail: ").strip()
            contr = input("Ingrese su contraseña: ").strip()

            if validar(mail, contr):
                print("Acceso concedido.\n")
                if log:
                    accion = ";".join([mail, str(datetime.datetime.now()), "Ingreso al sistema"])
                    log.write(accion + "\n")
                menuPrincipal(log, mail)
                acceso = True
            else:
                print("Usuario o contraseña incorrectos. Intente de nuevo.\n")


        log.close()


if name=="main":
    main()