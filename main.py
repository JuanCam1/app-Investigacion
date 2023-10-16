from pyscript import document
from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt
import random

body = document.querySelector(".body")
def valores_restricciones():
    input_text = document.querySelector("#variables")
    input_res = document.querySelector("#restricciones")
    variables = input_text.value
    restricciones = input_res.value
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
            
            if(j < variables):
                span = crear_elemento("span")
                sub = crear_elemento("sub")
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
    
    soluciones_x1_0,soluciones_x2_0 =hallar_puntos(values_restricciones)
    script = crear_elemento("py-script")
    agregar_atributos(script,"output","lineplot")
    script.textContent = f'{graficar(soluciones_x1_0,soluciones_x2_0)}'
    agregar_elemento(body,script)
    

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
    

def graficar(soluciones_x1_0,soluciones_x2_0):
    fig, ax = plt.subplots()
    maximo_punto = max(soluciones_x1_0)
    maximo_punto_2 = max(soluciones_x2_0)
    plt.xlim(0, max(maximo_punto_2[0]+5, 10))
    plt.ylim(0, max(maximo_punto[1]+5, 5))

    for punto in soluciones_x1_0:
        ax.plot(punto[0], punto[1], marker='.')

    for punto in soluciones_x2_0:
        ax.plot(punto[0], punto[1], marker='.')

    colores = ['red','blue','yellow','black','green']
    for punto1, punto2 in zip(soluciones_x1_0, soluciones_x2_0):
        x_values = [punto1[0], punto2[0]]
        y_values = [punto1[1], punto2[1]]
        color_aleatorio = random.choice(colores)
        ax.plot(x_values, y_values, linestyle='-', color=color_aleatorio)

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')

    ax.legend(["Método Grafico"], fontsize=8)
    plt.show()
    fig

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

    generate_variables(var)    
    generate_restricciones(var,res,banderas)
    button = crear_elemento("button")
    button.innerText = "Solución"
    agregar_atributos(button,"py-click","mostar_solucion")
    agregar_atributos(button,"class","button_solucion")
    agregar_elemento(body,button)