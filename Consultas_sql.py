#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:51:05 2021

@author: sergio
"""

import psycopg2
import pandas as pd

"""
*******************************
        CONEXIÓN DATABASE
*******************************
"""
database = 'acp'
user = 'sergio'
password = 'sergio'
host = '192.168.1.66'
port = '5432'

connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
cursor = connection.cursor()

# CSP TEST
host_test = '192.168.1.166'

connection_test = psycopg2.connect(database=database, user=user, password=password, host=host_test, port=port)
cursor_test = connection_test.cursor()

"""
*******************************
         CONSULTAS SQL
*******************************
"""

# Inspecciones
def psql_inspecciones(contrato = 'CDADSVERPI', fecha_creacion = '2021-01-01'):
    query = '''SELECT *
           FROM "public"."inspecciones" 
           WHERE contrato = %s AND fecha_inspeccion >= %s
           ORDER BY fecha_inspeccion ASC''' #cod_prov = %s AND 

    #cod_prov, orden_produccion, referencia, estado, contrato

    cursor.execute(query, [contrato, fecha_creacion]) #'CBC' SOPINDOFT, 
    colnames = [desc[0] for desc in cursor.description]
    data_psql= cursor.fetchall()
    
    df = pd.DataFrame(data_psql, columns=colnames)
    
    return (df)

# Defectos
def psql_defectos(contrato = 'CDADSVERPI', fecha_creacion = '2021-01-01'):
    query = '''SELECT *
               FROM "public"."defectos" 
               WHERE contrato = %s AND created_at >= %s
               ORDER BY created_at ASC'''
               
    cursor.execute(query, [contrato, fecha_creacion]) #'CBC', 
    colnames = [desc[0] for desc in cursor.description]
    data_psql= cursor.fetchall()
    
    df = pd.DataFrame(data_psql, columns=colnames)
    
    return(df)


# Pilatus QTY-NC
def psql_pilatusqtync(contrato = 'GQPILQIIN'):
    query = '''SELECT a.id, a.codigo, caa.campo_adicional, caa.id as ca_id, rcaa.contenido as contenido
               FROM auditorias a
               LEFT JOIN registro_campos_adicionales_auditoria rcaa ON a.id = rcaa.idauditoria::bigint
               LEFT JOIN campos_adicionales_auditoria caa ON caa.id = rcaa.idcampo::bigint
               WHERE a.contrato = %s AND a.estado != 'CANCELADO'
               ORDER BY a.codigo'''
    
    cursor.execute(query, [contrato]) #'CBC', 
    colnames = [desc[0] for desc in cursor.description]
    data_psql= cursor.fetchall()
    
    df = pd.DataFrame(data_psql, columns=colnames)
    
    return(df)

# Pilatus NO CONFORMIDADES
def psql_pilatusnc(contrato = 'GQPILQIIN'):
    query = '''SELECT a.id, a.codigo, caa.campo_adicional, caa.id as ca_id, rcaa.contenido as contenido
               FROM auditorias a
               LEFT JOIN registro_campos_adicionales_auditoria rcaa ON a.id = rcaa.idauditoria::bigint
               LEFT JOIN campos_adicionales_auditoria caa ON caa.id = rcaa.idcampo::bigint
               WHERE a.contrato = %s AND a.estado != 'CANCELADO'
               ORDER BY a.codigo'''
    
    cursor.execute(query, [contrato]) #'CBC', 
    colnames = [desc[0] for desc in cursor.description]
    data_psql= cursor.fetchall()
    
    df = pd.DataFrame(data_psql, columns=colnames)
    
    return(df)

"""
*******************************
      CONSULTAS SQL - TEST
*******************************
"""

# Inspecciones
def psql_inspecciones_test(contrato = 'SOPINDOFT', fecha_creacion = '2021-01-01'):
    query = '''SELECT *
           FROM "public"."inspecciones" 
           WHERE contrato = %s AND fecha_inspeccion >= %s
           ORDER BY fecha_inspeccion ASC''' #cod_prov = %s AND 

    #cod_prov, orden_produccion, referencia, estado, contrato

    cursor.execute(query, [contrato, fecha_creacion]) #'CBC' SOPINDOFT, 
    colnames = [desc[0] for desc in cursor.description]
    data_psql= cursor.fetchall()
    
    df = pd.DataFrame(data_psql, columns=colnames)
    
    return (df)
