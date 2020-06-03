import datetime


def escribir_al_log(excepcion, texto):
    fecha = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    with open('error.log', 'a+') as archivo_log:
        archivo_log.write(f'-------------------------{fecha}-------------------------\n')
        archivo_log.write(str(excepcion))
        archivo_log.write(texto)
        archivo_log.write('----------------------------------------------------------------\n')