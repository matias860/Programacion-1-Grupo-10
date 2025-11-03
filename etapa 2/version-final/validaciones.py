def validacion_texto(text):
    #validacion de texto
    while True:
            try:
                texto= input(text).strip()
                if texto == "":
                    break
                if not texto.isalpha():
                    raise ValueError("El ingreso solo puede contener letras.")
                break
            except ValueError as e:
                print("ERROR:",e)
    return texto    

def validarnumerolen(largo_min,largo_max,msj):
    #valiida numero con un len maximo y un len minimo
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

def validarentradanumerica(desde,hasta,mensaje):
    #valida un numero con rango
    while True:
        try:
            entrada=input(mensaje).strip()
            if entrada=="":
                raise ValueError("No se permiten entradas vacias")
            if not entrada.isdigit():
                raise ValueError("El ingreso debe ser numerico")
            entrada=int(entrada)
            if entrada<desde or entrada>hasta:
                raise ValueError("el ingreso esta fuera del rango permitido")
            break
        except ValueError as e:
            print("ERROR:",e)
    return entrada

def validar_alfadigit(mensj_us):
    #valida una entrada que puede ser alfanumerica(usado para contras)
    while True:
        try:
            aldigi=input(mensj_us).strip()
            if aldigi=="":
                raise ValueError("La entrada no puede ser vacia")
            if not aldigi.isalnum():
                raise ValueError("La entrada solo debe contener numero y letras")
            break
        except ValueError as o:
            print("ERROR:",o)
    return aldigi

def validacion_text(mensaj):
    #valida ingreso sin @ ni "" (para mails)
    while True:
        try:
            txt = input(mensaj).strip()
            if txt == "":
                raise ValueError("La entrada no puede ser vacÃ­a.")
            if "@" in txt or " " in txt:
                raise ValueError("No incluya '@' ni espacios.")
            break
        except ValueError as o:
            print("ERROR:",o)
    return txt
