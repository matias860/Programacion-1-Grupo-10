from modulos import *
import datetime

def main():
    crearArchivoUsuarios()
    try:
        arch = open("usuarios.csv", "rt")
        log = open("log.csv","at")
    except FileNotFoundError:
        print("No se encontró el archivo de usuarios.")
        return
    except IOError:
        print("Error al abrir el archivo")
    else:
        print("Log cargado")
        usuarios = {}
        for linea in arch:
            partes = linea.strip().split(";")
            if len(partes) == 2:
                usuarios[partes[0]] = partes[1]
        arch.close()

        print("=== LOGIN DE USUARIO ===")
        while True:
            mail = input("Ingrese su mail: ").strip()
            password = input("Ingrese su contraseña: ").strip()

            if mail in usuarios and usuarios[mail] == password:
                print("Acceso concedido.\n")
                accion = ";".join([mail, str(datetime.datetime.now()), "Ingreso al sistema"])
                log.write(accion + "\n")
                menuPrincipal(log, mail)
                break
            else:
                print("Usuario o contraseña incorrectos. Intente de nuevo.\n")
        arch.close()
        log.close()

if __name__=="__main__":
    main()
