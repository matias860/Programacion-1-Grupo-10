from modulos import *

def main():
    turnos, dias, pacientes = inicializarDatos()

    print("Bienvenido a la clinica Hoggins.")
    opcion = int(input("1- Asignar turno\n2- Ver turnos asignados\n3- Resumen del dia\n4- Salir: "))

    while opcion != 4:
        while opcion < 1 or opcion > 4:
            opcion = int(input("ERROR. Ingrese una opcion correcta (1-4): "))

        if opcion == 1:
            cargaTurnos(turnos, pacientes)
        elif opcion == 2:
            mostrarTurnos(turnos, dias)
        elif opcion == 3:
            resumen(turnos, dias, pacientes)

        opcion = int(input("1- Asignar turno\n2- Ver turnos asignados\n3- Resumen del dia\n4- Salir: "))
        
    print("Hasta mañana!")

if __name__ == "__main__":
    main()