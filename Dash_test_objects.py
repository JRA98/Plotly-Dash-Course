#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:07:15 2021

@author: sergio
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import pandas as pd

import Consultas_sql as sql

df_pilatus = sql.psql_pilatusqtync()

"""
--------------------------------
    KPI 3 - PILATUS - QTY/NC
--------------------------------
"""
def kpi_4(tipo = 'Todos'):
    df_kpi_4 = df_pilatus[["codigo", "campo_adicional", "contenido"]]
    
    #print("Inicio función:", tipo)
    
    if tipo == 'Todos' or tipo == None  or tipo == 'None':
        #print("Seguimos")
        a = "a"
    else:
        #print("Dentro función:", tipo)
        mask = (df_kpi_4["campo_adicional"] == tipo)
        df_kpi_4 = df_pilatus.loc[mask, :]
    
    df_kpi_4["contenido"] = df_kpi_4["contenido"].apply(pd.to_numeric, errors='coerce')
    
    kpi_4 = df_kpi_4.groupby(["codigo"])["contenido"].agg('sum').reset_index().rename(columns={"codigo":"MSN", "contenido":"Defectos"})
    
    y_range = kpi_4["Defectos"].max() + 100
    
    fig_1 = px.line(kpi_4, x="MSN", y="Defectos", hover_name="MSN", title="QTY NC/MSN", text="Defectos")#, log_x=True)
    fig_1.add_hline(y=200, line=dict(color="red", dash="dashdot"))
    fig_1.add_hline(y=50, line=dict(color="yellow", dash="dashdot"))
    fig_1.layout.plot_bgcolor = "#fff"
    fig_1.layout.paper_bgcolor = "#fff"
    fig_1.layout.showlegend = True
    fig_1.update_traces(line=dict(color="rgb(0,73,131)"), marker=dict(color="rgb(168,200,85)"), marker_line=dict(color="rgb(0,73,131)", width=2), textposition="top center", textfont=dict(color="#656565"))
    #fig.layout.title(text="QTY NC/MSN")
    fig_1.update_xaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1, tickcolor="red", tickangle=315)
    fig_1.update_yaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1, tickcolor="#656565", range=[0,y_range])

    return fig_1

"""------------------"""

"""
------------------------------------------
    KPI 2 - PILATUS - NO CONFORMIDADES
------------------------------------------
"""
def kpi_5(tipo = '-'):
    #df_pilatus = sql.psql_pilatusqtync()
    df_kpi_5 = df_pilatus[["campo_adicional", "contenido"]]
    df_kpi_5["contenido"] = df_kpi_5["contenido"].apply(pd.to_numeric, errors='coerce')
        
    kpi_5 = df_kpi_5.groupby(["campo_adicional"]).agg({'contenido':'sum'}).reset_index().rename(columns={"campo_adicional":"Tipo", "contenido":"Defectos"})
    kpi_5.sort_values(by=["Defectos"], ascending= False, inplace=True)
    #Calcular el porcentaje sobre el total en una columna, se puede con groupby
    kpi_5["Cumsum %"] = round(kpi_5["Defectos"].cumsum() / kpi_5["Defectos"].sum(), 2)
    
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2.add_trace(go.Bar(x=kpi_5["Tipo"], y=kpi_5["Defectos"], hovertext=kpi_5["Tipo"], name="TYPE", text=kpi_5["Defectos"], marker_color="rgb(0,73,131)"), secondary_y = False)#, log_x=True)
    fig_2.add_trace(go.Line(x=kpi_5["Tipo"], y=kpi_5["Cumsum %"], marker_color="red", name="%"), secondary_y = True)
    
    # Styling
    fig_2.update_traces(textfont=dict(color="#fff")) #, textposition="inside"
    fig_2.layout.plot_bgcolor = "#fff"
    fig_2.layout.paper_bgcolor = "#fff"
    fig_2.update_xaxes(title="Defectos", showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1, tickcolor="red", tickangle=315, tickfont=dict(size=7))
    fig_2.update_yaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1, tickcolor="#656565", secondary_y = False, showticklabels=True)
    fig_2.update_yaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=False, gridcolor="#E4E6E8", gridwidth=1, tickcolor="#656565", secondary_y = True, range=[0,1.1], overlaying='y')
    
    return fig_2

"""------------------"""

"""
------------------------------------------
    KPI 3 - INSPECCIONES - TEST
------------------------------------------
"""
def kpi_6(tipo = '-'):
    df = sql.psql_inspecciones_test()
    df_kpi = df[["id", "fecha_inspeccion"]]
    df_kpi["fecha_inspeccion"] = pd.to_datetime(df_kpi["fecha_inspeccion"])
    df_kpi["Año-mes"] = df_kpi["fecha_inspecicon"].dt.year.astype(str) + "-" + df_kpi["fecha_inspeccion"].dt.strftime('%m')
        
    kpi = pd.crosstab(df_kpi["Año-mes"], columns="count").reset_index().rename(columns={"Año-mes": "Año-mes", "count":"#"})
    
    fig = px.Bar(kpi, x = kpi["Año-mes"], y = ["#"], title="# Inspections")
    #fig_1 = px.line(kpi_4, x="MSN", y="Defectos", hover_name="MSN", title="QTY NC/MSN", text="Defectos")#, log_x=True)
    #fig.add_trace(go.Bar(x=kpi_5["Tipo"], y=kpi_5["Defectos"], hovertext=kpi_5["Tipo"], name="TYPE", text=kpi_5["Defectos"], marker_color="rgb(0,73,131)"), secondary_y = False)#, log_x=True)
    #fig_2.add_trace(go.Line(x=kpi_5["Tipo"], y=kpi_5["Cumsum %"], marker_color="red", name="%"), secondary_y = True)
    
    # Styling
    fig.update_traces(textfont=dict(color="#fff")) #, textposition="inside"
    fig.layout.plot_bgcolor = "#fff"
    fig.layout.paper_bgcolor = "#fff"
    fig.update_xaxes(title="Month", showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1)#, tickcolor="red", tickangle=315, tickfont=dict(size=7))
    fig.update_yaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=True, gridcolor="#E4E6E8", gridwidth=1, tickcolor="#656565", showticklabels=True)
    #fig.update_yaxes(showline=True, linewidth=1, linecolor="#656565", showgrid=False, gridcolor="#E4E6E8", gridwidth=1, tickcolor="#656565", secondary_y = True, range=[0,1.1], overlaying='y')
    
    return fig

"""------------------"""

fig_1 = kpi_4()
fig_2 = kpi_5()

app = dash.Dash(
      __name__,
    external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])

app.layout = html.Div(
    children = [
        html.H1(children="DASHBOARD CSP",),
        html.H3(
            children = "AUDITORÍAS - PILATUS",
            className='center',
        ),
        html.Div([
            html.Div([], className = "one columns"),
            
            html.Div([
                dcc.Dropdown(
                    id = 'tipo',
                    options = [{'label': i, 'value': i} for i in df_pilatus["campo_adicional"].sort_values(ascending=True).unique()],
                    value='Todos'
                ),
            ], className = "three columns")  
        ], className="row"),
        html.Div([
            html.Div([
                dcc.Graph(
                    id = "g0",
                    figure=fig_1,
                ),
                dcc.Interval(
                    id = 'interval-component',
                    interval = 60*1000,
                    n_intervals = 0
                ),
            ], className = "six columns"),

            html.Div([
                dcc.Graph(
                    id = "g1",
                    figure=fig_2,
                ),
            ], className = "six columns"),
        ], className="row"),
    ]
)


@app.callback(
    Output(component_id = 'g0', component_property = 'figure'),
    [
         Input(component_id = 'tipo', component_property = 'value'),
         Input('interval-component', 'n_intervals'),
    ],)
def update_graph_g0(value, n):
    return kpi_4(value)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')