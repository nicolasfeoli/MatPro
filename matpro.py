from tkinter import *
from pymatrix import Matrix
import os
import webbrowser


root = Tk()
root.title("MatPro V-1.0 @Nicolas Feoli")
root.geometry("717x450+250+80")
root.resizable(width=FALSE, height=FALSE)

Label(root, bg="black", height=5, width=100).place(x=0, y=400)



#Label(root, text="MatPro",font="Verdana 20").pack(side=TOP)

frameMedio = Frame(root, bd=0, relief=FLAT)
frameMedio.place(x=0,y=0)

xscrollbar = Scrollbar(root, orient=HORIZONTAL)#, width=16)
xscrollbar.pack(side=BOTTOM, fill=X)
#xscrollbar.place(x=0,y=437)

yscrollbar = Scrollbar(frameMedio)
yscrollbar.pack(side=RIGHT, fill=Y)

text = Text(frameMedio, wrap=NONE, bd=0,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set,
            highlightbackground="black",
            height=27,
            width=100,
            bg="black",
            fg="white")
text.insert(INSERT, """

 __  __       _   _____
|  \/  |     | | |  __ \
| \  / | __ _| |_| |__) | __ ___                           +-+-+-+-+-+-+  +-+-+
| |\/| |/ _` | __|  ___/ '__/ _ \                  _       |A|y|u|d|a|:| | F1  |
| |  | | (_| | |_| |   | | | (_) |        \  / /| / \      +-+-+-+-+-+-+  +-+-+
|_|  |_|\__,_|\__|_|   |_|  \___/          \/   |o\_/ \n
MatPro v1.0 es una calculadora de matrices con interfaz de
linea de comando que permite hacer una serie de operaciones
con matrices de manera sencilla y rapida.\n
Para un listado de las funciones escriba el comando AYUDA o presione F1.\n\n\n\n\n\n\n\n\n\n
""")


text.config(state=DISABLED)

text.pack(fill=X)

xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)

text.tag_add("here", "1.0", "1.4")
text.tag_add("start", "1.8", "1.13")
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="black", foreground="white")

Label(root, text="MATPRO:~$", bg="black", fg="white").place(x=0, y=415)

comando = StringVar()
E = Entry(root, relief=FLAT,
          highlightbackground="black",
          textvariable=comando,width=79,
          bd = 0, bg="black", fg="white",
          insertbackground="white",)
E.place(x=75,y=415)



matrices = {"a":Matrix([[3,2,1],[1,1,3],[0,2,1]]),
            "b":Matrix([[2,1],[1,0],[3,2]])}
state = "idle"
contMat = 2
nombreActual = ""
matrizActual = []

def insertarTexto(texto, start="\n"):
    global text
    text.config(state=NORMAL)
    text.insert(END, "{0}{1}".format(start, texto))
    text.see(END)
    text.config(state=DISABLED)

def getTextComando(quitarComas=False):
    global comando
    com = comando.get()
    if quitarComas:
        arreglarString(com)
    else:
        com = com.split(" ")
    comando.set("")
    return com

def pegarLista(lista, conEspacios=False):
    final = ""
    if conEspacios:
        for i in lista:
            final += i
            final += " "
    else:
        for i in lista:
            final += i
    return final

def arreglarString(fila):
    "recibe un string retorna una lista con solo numeros"
    final = []
    temp = ""
    for i in fila:
            if i == "," and i == " ":
                final.append(temp)
                temp = ""
            else:
                temp += i
            final.append(temp)
    return final

def guardarFila(fila):
    global nombreActual, matrizActual
    matrizActual += fila.split(" ")

def instanMatriz():
    global matrices, matrizActual, nombreActual
    #print(matrizActual)
    print(matrizActual)
    matriz = Matrix(matrizActual)
    #print(matriz)
    matrices[nombreActual] = matriz

def desplegarAcercaDe():
    insertarTexto("MatPro version 1.0\nHecho por Nicolas Feoli\nCreado el 1/06/16.\nTaller de Programacion\nProfesor: William Mata\nInstituto Tecnologico de Costa Rica\n\n")

def error():
    filewin = Toplevel(principal)
    err = Label(filewin,fg="black",text="Error accesando a la aplicacion predeterminada para pdf.",font="Verdana 20")
    err.pack()

def ayuda():
    try:
        if sys.platform == "linux":
            webbrowser.open_new(r'./manual_de_usuario_matpro.pdf')
        else:
            os.startfile("manual_de_usuario_matpro.pdf")
    except Exception as e:
        insertarTexto("Error: no se pudo abrir la aplicacion predeterminada para abrir el documento.\nRevise las configuraciones de su maquina y vualva a intentar.")
        error()

#################
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

filemenu.add_separator()

filemenu.add_command(label="Salir", command=root.destroy)
menubar.add_cascade(label="Programa", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Manual de Usuario", command=ayuda)
helpmenu.add_command(label="Acerca de..", command=desplegarAcercaDe)
menubar.add_cascade(label="Ayuda", menu=helpmenu)

root.config(menu=menubar)

#################


def abrirArchivo(nombreArchivo="datos_matpro.txt"):
    global nombreActual, state, matrices
    file= open(nombreArchivo,"r")
    first = True
    for line in file:
        if first:
            nombreActual = line[:-1]
            first = False
            insertarTexto(nombreActual)
        elif "." in line:
            instanMatriz()
            first = True
        else:
            print(line[:-1])
            print(arreglarString(line[:-1]))
            guardarFila(arreglarString(line[:-1]))
            #insertarTexto(pegarLista(line, True))
    insertarTexto(matrices[nombreActual])
    state = "idle"

def leeMatriz():
    global state, contMat, nombreActual
    com = getTextComando(True)
    #print("com[0]:",com[0], com)
    if com[0] == ".":
        state = "idle"
        insertarTexto(".\n", start="")
        instanMatriz()
    else:
        insertarTexto(pegarLista(com, True), start = " ")
        if contMat == 2:
            guardarFila(com)
        else:
            guardarFila(com)
        insertarTexto("Fila %d: "%contMat)
        contMat += 1

def confirmarSalida():
    com = getTextComando()
    if com[0] == "si":
        root.destroy()
    if com[0] == "no":
        insertarTexto("Continua la ejecucion del programa.")

def ingresaComando():
    global text, root, state, matrices, contMat, nombreActual
    com = getTextComando()
    if com[0].lower() == "fin" or com[0].lower() == "finalizar":
        state = "saliendo"
        insertarTexto("MATPRO:~$ %s"%com[0])
        insertarTexto("Va a salir del programa. Las matrices que no ha guardado se perderán. Esta seguro que desea salir?")
    elif com[0].lower() == "lee":
        if len(com) == 2:
            state = "leyendo"
            #string = "MATPRO:~$ {0} {1}\n".format(com[0],com[1])
            insertarTexto("MATPRO:~$ {0} {1}".format(com[0],com[1]))
            insertarTexto("Fila 1: ")
            nombreActual = com[1]
        else:
            insertarTexto("MATPRO:~$ %s"%com[0])
            insertarTexto("Error: El nombre de la matriz debe tener solo letras y numeros.")
    elif com[0].lower() == "leerarchivo" or com[0].lower() == "leearc":
        if len(com) == 2:
            state = "abriendo archivo"
            insertarTexto("MATPRO:~$ {0} {1}".format(com[0],com[1]))
            insertarTexto("Archivo: {}".format(com[1]))
            abrirArchivo(com[1])
        elif len(com) == 1:
            state = "abriendo archivo"
            insertarTexto("MATPRO:~$ {0} ".format(com[0]))
            insertarTexto("Como no hay argumentos, se va a abrir el archivo datos_matpro.txt")
            insertarTexto("Archivo: datos_matpro.txt")
            abrirArchivo()
    elif com[0].lower() == "ayuda" or com[0].lower() == "ayu":
        insertarTexto("Abriendo el pdf...", start="\n")
        ayuda()
    elif com[0].lower() == "acercade" or com[0].lower() == "ace":
        desplegarAcercaDe()
    else:
        insertarTexto(exec())

def revisaEstado(event):
    global state
    print(state)
    if state == "idle":
        return ingresaComando()
    if state == "leyendo":
        return leeMatriz()
    if state == "saliendo":
        return confirmarSalida()

root.bind("<Return>", revisaEstado)


root.mainloop()
