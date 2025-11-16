"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import re
import pandas as pd


def pregunta_01():
    """
    Lee el archivo 'files/input/clusters_report.txt' y construye un
    dataframe de Pandas con el contenido organizado.

    Requisitos implementados:

    - La estructura del dataframe replica la tabla del archivo fuente.
    - Los encabezados de las columnas están en minúsculas y usan
      guiones bajos en lugar de espacios.
    - Las frases de palabras clave se unifican en una sola cadena,
      separadas por coma y un espacio entre término y término.
    """

    # Abrimos el archivo de texto y descartamos las primeras 4 líneas de cabecera
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as archivo:
        lineas_archivo = archivo.readlines()[4:]

    # Expresión regular para identificar el inicio de cada fila de la tabla
    patron_cluster = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.+)$")

    registros = []
    registro_actual = None

    for linea in lineas_archivo:
        coincidencia = patron_cluster.match(linea)

        if coincidencia:
            # Si ya veníamos acumulando un registro, lo completamos y guardamos
            if registro_actual is not None:
                registro_actual["principales_palabras_clave"] = limpiar_palabras_clave(
                    registro_actual["palabras_crudas"]
                )
                registro_actual["porcentaje_de_palabras_clave"] = convertir_porcentaje(
                    registro_actual["porcentaje_de_palabras_clave"]
                )
                # Eliminamos el campo auxiliar que solo se usa durante el armado
                del registro_actual["palabras_crudas"]
                registros.append(registro_actual)

            # Empezamos un nuevo registro a partir de la línea actual
            registro_actual = {
                "cluster": int(coincidencia.group(1)),
                "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                "porcentaje_de_palabras_clave": coincidencia.group(3).strip(),
                # Guardamos las palabras clave en bruto para unirlas más adelante
                "palabras_crudas": [coincidencia.group(4).strip()],
            }

        elif linea.strip() and registro_actual is not None:
            # Si la línea no está vacía, es una continuación de las palabras clave
            registro_actual["palabras_crudas"].append(linea.strip())

    # Procesamos el último registro acumulado, si existe
    if registro_actual is not None:
        registro_actual["principales_palabras_clave"] = limpiar_palabras_clave(
            registro_actual["palabras_crudas"]
        )
        registro_actual["porcentaje_de_palabras_clave"] = convertir_porcentaje(
            registro_actual["porcentaje_de_palabras_clave"]
        )
        del registro_actual["palabras_crudas"]
        registros.append(registro_actual)

    # Convertimos la lista de diccionarios en un dataframe de Pandas
    return pd.DataFrame(registros)


def limpiar_palabras_clave(lista_palabras):
    """
    Une las líneas de palabras clave, corrige espacios y formato
    de comas y devuelve un solo texto limpio.
    """
    texto = " ".join(lista_palabras)
    # Reemplaza repeticiones de espacios por un único espacio
    texto = re.sub(r"\s+", " ", texto)
    # Asegura que haya exactamente un espacio después de cada coma
    texto = re.sub(r"\s*,\s*", ", ", texto)
    # Remueve espacios sobrantes y signos de puntuación al final
    return texto.strip().rstrip(".,")


def convertir_porcentaje(cadena_porcentaje):
    """
    Recibe un porcentaje como texto (ej. '12,34 %') y retorna
    su valor numérico en tipo float.
    """
    valor_limpio = (
        cadena_porcentaje.replace(",", ".")
        .replace("%", "")
        .strip()
    )
    return float(valor_limpio)
