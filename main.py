from pyscript import document
from sympy import symbols, Eq, solve
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt
import random

body = document.querySelector(".body")
def valores_restricciones():
    input_text = document.querySelector("#variables")
    input_res = document.querySelector("#restricciones")
    variables = input_text.value
    restricciones = input_res.value
    if(restricciones == ""): 
        restricciones = "0"
    var = convertir_Aentero(variables)
    res = convertir_Aentero(restricciones)
    return var , res

def crear_elemento(tipo):
    return document.createElement(tipo)

def agregar_elemento(padre,hijo):
    padre.append(hijo)

def agregar_atributos(elemento,tipo,valor):
    elemento.setAttribute(tipo,valor)

def convertir_Aentero(texto):
    return int(texto)

def convertir_Atexto(entero):
    return str(entero)
    
def generate_variables(value):
    output_var = document.querySelector("#funcion_objetiva")
    h2 = crear_elemento("h2")
    h2.innerText="Función Objetivo"
    div = crear_elemento("div")
    agregar_atributos(div,"class","container_fo")
    agregar_elemento(output_var,h2)
    agregar_elemento(output_var,div)


    for i in range(value):
        index = convertir_Atexto(i)
        input = crear_elemento("input",)
        agregar_atributos(input,"type","text")
        agregar_atributos(input,"id","input_"+index)
        agregar_atributos(input,"class","input_fo")
        agregar_elemento(div,input)
        
        span = crear_elemento("span")
        sub = crear_elemento("sub")
        sub.innerText = convertir_Atexto(i+1)
        span.innerText = "X"
        agregar_elemento(span,sub)
        agregar_elemento(div,span)

        if(i < value-1):
          span.innerText += "+"  
     
def generate_restricciones(variables,rest,banderas):
    output_res = document.querySelector("#funcion_res")
    h2 = crear_elemento("h2")
    h2.innerText="Restricciones"
    divRes = crear_elemento("div")
    agregar_atributos(divRes,"class","container_res")
    agregar_elemento(output_res,h2)
    agregar_elemento(output_res,divRes)

    for i in range(rest):
        index_i = convertir_Atexto(i)
        div = crear_elemento("div")
        agregar_atributos(div,"class","div_res_"+index_i)

        for j in range(variables+1):
            index_j = convertir_Atexto(j) 
            input = crear_elemento("input")
            agregar_atributos(input,"type","text")
            agregar_atributos(input,"id","input_res_"+index_j)
            agregar_atributos(input,"class","input_res_"+index_i)
            agregar_elemento(div,input)
            
            span = crear_elemento("span")
            sub = crear_elemento("sub")
            if(j < variables):
                sub.innerText = convertir_Atexto(j+1)
                span.innerText = "X"
                agregar_elemento(span,sub)
                agregar_elemento(div,span)

            if(j < variables - 1):  
                span.innerText += "+"  

            if(j == variables-1):
                span = crear_elemento("span")
                span.innerText = banderas[i]
                agregar_elemento(div,span)

        agregar_elemento(divRes,div)
    ultima_restriccion(variables,divRes)



def ultima_restriccion(variable,divRes):
    span = crear_elemento("span")
    valores = []
    for i in range(int(variable)):
        valores.append("X"+str(i+1))
    valores.append("\u2265 0")
    texto = ', '.join(valores)
    span.innerText = texto
    agregar_elemento(divRes,span)
    


def mostar_solucion(event):
    var,res = valores_restricciones()
    values_restricciones = []
    values_objetivos = []

    for i in range(var):
        index_i = convertir_Atexto(i)
        input_ob_value = document.querySelector('.container_fo #input_'+index_i)
        values_objetivos.append(input_ob_value.value)

    for i in range(res):
        index_i = convertir_Atexto(i)
        input_res_index_i=[]
        for j in range(var+1):
            index_j = convertir_Atexto(j)
            input_res_cont = document.querySelector('.div_res_'+index_i+' #input_res_'+index_j)
            input_res_index_i.append(input_res_cont.value)
        values_restricciones.append(input_res_index_i)

    x_opt,y_opt,result,c = valor_optimo(values_restricciones,values_objetivos)
    soluciones_x1_0,soluciones_x2_0 =hallar_puntos(values_restricciones)
    intersecciones = puntos_interseccion(values_restricciones)  # Define intersecciones
    script = crear_elemento("py-script")
    agregar_atributos(script,"output","lineplot")
    agregar_atributos(script,"id","script_grafica")
    script.textContent = f'{graficar(soluciones_x1_0,soluciones_x2_0,x_opt,y_opt, values_restricciones)}'
    agregar_elemento(body,script)
    generar_tabla_intersecciones_factibles(values_restricciones)
    valor_optimo_dom(x_opt,y_opt,result,c)

def es_factible(punto, values_restricciones):
    """Determina si un punto está en la región factible definida por las restricciones."""
    x, y = punto
    for restriccion in values_restricciones:
        a = float(restriccion[0])
        b = float(restriccion[1])
        c = float(restriccion[2])
        a, b, c = [float(val) for val in restriccion]  # Convertir a flotante
        if a * x + b * y > c:
            return False
    return True

import string

def generar_tabla_intersecciones_factibles(values_restricciones):
    # 1. Obtener puntos donde las restricciones intersectan los ejes
    soluciones_x1_0, soluciones_x2_0 = hallar_puntos(values_restricciones)
    puntos = soluciones_x1_0 + soluciones_x2_0
    
    # 2. Obtener puntos de intersección entre las restricciones
    intersecciones = puntos_interseccion(values_restricciones)
    puntos.extend(intersecciones)
    
    # 3. Agregar el origen a la lista de puntos
    puntos.append((0,0))
    
    # 4. Filtrar puntos para quedarse solo con los factibles
    puntos_factibles = [punto for punto in puntos if es_factible(punto, values_restricciones)]
    
    # Generar tabla
    tabla = crear_elemento("table")
    agregar_atributos(tabla, "class", "styled-table")
    thead = crear_elemento("thead")
    tr_head = crear_elemento("tr")
    th_nombre = crear_elemento("th")
    th_nombre.innerText = "Punto"
    th_x = crear_elemento("th")
    th_x.innerText = "X"
    th_y = crear_elemento("th")
    th_y.innerText = "Y"
    agregar_elemento(tr_head, th_nombre)
    agregar_elemento(tr_head, th_x)
    agregar_elemento(tr_head, th_y)
    agregar_elemento(thead, tr_head)
    agregar_elemento(tabla, thead)
    
    tbody = crear_elemento("tbody")
    for idx, punto in enumerate(puntos_factibles):
        tr = crear_elemento("tr")
        td_nombre = crear_elemento("td")
        td_nombre.innerText = string.ascii_lowercase[idx]  # Nombrar el punto
        td_x = crear_elemento("td")
        td_x.innerText = str(punto[0])
        td_y = crear_elemento("td")
        td_y.innerText = str(punto[1])
        agregar_elemento(tr, td_nombre)
        agregar_elemento(tr, td_x)
        agregar_elemento(tr, td_y)
        agregar_elemento(tbody, tr)
    agregar_elemento(tabla, tbody)
    agregar_elemento(body, tabla)

def valor_optimo(values_restricciones,values_objetivos):
    c = [int(valor) for valor in values_objetivos]
    res_izq_valores_x= [int(sublista[0]) for sublista in values_restricciones]
    res_izq_valores_y = [int(sublista[1]) for sublista in values_restricciones]
    res_der_valores = [int(sublista[-1]) for sublista in values_restricciones]

    A = np.array([res_izq_valores_x, res_izq_valores_y]).T      
    b = np.array(res_der_valores)
    result = linprog(c, A_ub=-A, b_ub=-b)
    x_opt, y_opt = result.x
    return x_opt,y_opt,result,c
    

def valor_optimo_dom(x_opt,y_opt,result,c):
    div = crear_elemento("div")
    agregar_atributos(div,"class","valor_optimo")
    span_punto = crear_elemento("span")
    agregar_atributos(span_punto,"class","span_punto")
    span_fo = crear_elemento("span")
    agregar_atributos(span_fo,"class","span_fo")
    
    span_punto.innerText = f"({x_opt},{y_opt})"
    span_fo.innerText = f"{c[0]}({x_opt})+{c[1]}({y_opt}) = {result.fun}"
    agregar_elemento(div,span_punto)
    agregar_elemento(div,span_fo)
    agregar_elemento(body,div)

def hallar_puntos(values_restricciones):
    var,res= valores_restricciones()
    variables = {}
    for i in range(1, var+1):
        variables[f'x{i}'] = symbols(f'x{i}')

    ecuaciones = []
    for a,b,c in values_restricciones:
        ecuacion = Eq(int(a) * variables['x1'] + int(b) * variables['x2'], int(c))
        ecuaciones.append(ecuacion)

    ecuaciones_x1=[]
    for i in range(len(ecuaciones)):
        ecuacion_con_valores = ecuaciones[i].subs({variables['x1']: 0})
        ecuaciones_x1.append(ecuacion_con_valores)

    ecuaciones_x2=[]
    for i in range(len(ecuaciones)):
        ecuacion_con_valores = ecuaciones[i].subs({variables['x2']: 0})
        ecuaciones_x2.append(ecuacion_con_valores)

    soluciones_x1_0 = []
    soluciones_x2_0 = []
    for i in range(len(ecuaciones)):
        punto_x = solve(ecuaciones_x1[i])
        puntos_x1_0 = [0,int(punto_x[0])]
        soluciones_x1_0.append(puntos_x1_0)
        punto_y = solve(ecuaciones_x2[i])
        puntos_x2_0 = [int(punto_y[0]),0]
        soluciones_x2_0.append(puntos_x2_0)
    
    return soluciones_x1_0,soluciones_x2_0
    
def puntos_interseccion(values_restricciones):
    var, res = valores_restricciones()
    variables = {}
    for i in range(1, var+1):
        variables[f'x{i}'] = symbols(f'x{i}')
    
    ecuaciones = []
    for a, b, c in values_restricciones:
        ecuacion = Eq(int(a) * variables['x1'] + int(b) * variables['x2'], int(c))
        ecuaciones.append(ecuacion)
    
    puntos = []
    for i in range(len(ecuaciones)):
        for j in range(i+1, len(ecuaciones)):
            sol = solve((ecuaciones[i], ecuaciones[j]), (variables['x1'], variables['x2']))
            if sol:  # si hay solución
                puntos.append((float(sol[variables['x1']]), float(sol[variables['x2']])))
    
    return puntos
    
def graficar(soluciones_x1_0,soluciones_x2_0,x_opt,y_opt,values_restricciones):
    fig, ax = plt.subplots()
    plt.rcParams['toolbar'] = 'None'
    maximo_punto = max(soluciones_x1_0)
    maximo_punto_2 = max(soluciones_x2_0)
    plt.xlim(0, max(maximo_punto_2[0]+5, 10))
    plt.ylim(0, max(maximo_punto[1]+5, 5))
    
    # Sombrear la región factible 
    x = np.linspace(0, max(maximo_punto_2[0]+5, 10), 400)
    y_lists = []
    
    for punto1, punto2 in zip(soluciones_x1_0, soluciones_x2_0):
        y_list = (punto2[1] - punto1[1])/(punto2[0] - punto1[0]) * (x - punto1[0]) + punto1[1]
        y_lists.append(y_list)
    y_min = np.min(y_lists, axis=0)
    ax.fill_between(x, 0, y_min, where=(y_min>=0), color='lightgray', alpha=0.5)
    
    #graficar las restricciones
    colores = ['red','blue','yellow','black','green',"gray","blueViolet","brown","darkSlateBlue"]
    for punto1, punto2 in zip(soluciones_x1_0, soluciones_x2_0):
        color_aleatorio = random.choice(colores)
        ax.scatter(punto1[0], punto1[1], s=50, color=color_aleatorio)
        ax.annotate(f"({punto1[0]},{punto1[1]})", (punto1[0], punto1[1]), fontsize=8, xytext=(5,-10), textcoords='offset points')
        ax.scatter(punto2[0], punto2[1], s=50, color=color_aleatorio)
        ax.annotate(f"({punto2[0]},{punto2[1]})", (punto2[0], punto2[1]), fontsize=8, xytext=(5,-10), textcoords='offset points')
        
        x_values = [punto1[0], punto2[0]]
        y_values = [punto1[1], punto2[1]]
        ax.plot(x_values, y_values, linestyle='-', color=color_aleatorio)

    # Puntos de intersección
    intersecciones = puntos_interseccion(values_restricciones)
    for x, y in intersecciones:
        if 0 <= x <= max(maximo_punto_2[0]+5, 10) and 0 <= y <= max(maximo_punto[1]+5, 5):
            ax.scatter(x, y, color='purple', marker='o', s=50)
            ax.annotate(f"({x:.2f},{y:.2f})", (x, y), fontsize=8, xytext=(5,10), textcoords='offset points')
    
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')

    ax.legend(["Método Grafico"], fontsize=8)
    plt.show()

def capturar_valores(event):
    input_max = document.querySelector("#opcion")
    var,res = valores_restricciones()
    banderas = []

    if(input_max.value.lower() == 'maximizar'):
        for i in range(res):
            banderas.append('\u2264')
    else:
        for i in range(res):
            banderas.append('\u2265')

    h2 = crear_elemento("h2")
    agregar_atributos(h2,"class","alert_style")
    agregar_atributos(h2,"id","error")
    h2.innerText="Restricciones > 1."
    agregar_elemento(body,h2)
    
    if (res <= 1):
        h2.style.display = 'block'
        print('hi')
    else:
        h2.style.display = 'none'
        generate_variables(var)    
        generate_restricciones(var,res,banderas)
        button = crear_elemento("button")
        button.innerText = "Solución"
        agregar_atributos(button,"py-click","mostar_solucion")
        agregar_atributos(button,"class","button_solucion")
        agregar_elemento(body,button)