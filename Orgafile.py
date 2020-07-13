import os
import shutil
import eyed3
import time
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

import random

#FUNCIONALIDAD



def moverArchivo(arch, ruta):
	changed = False
	actual = os.getcwd()
	os.chdir(ruta)
	nuevo = arch
	while(os.path.exists(nuevo) or (changed and os.path.exists(actual + "/" + nuevo))):
		changed = True
		nombre, ext = nuevo.split(".")
		nombre = nombre + "_"
		nuevo = nombre + "." + ext
	os.chdir(actual)
	if changed:
		try:
			os.rename(arch, nuevo)
			shutil.move(nuevo, ruta)
		except:
			moverArchivo()
	else:
		shutil.move(arch, ruta)

def elPadreDe(hijo):
	partes = hijo.split()
	final = partes.pop()
	return final

def destruirCarpeta(padre, hijo):
	os.chdir(hijo)
	subdir = os.listdir(hijo)
	for f in subdir:
		if os.path.isdir(f):
			nieto = hijo + "/" + f
			destruirCarpeta(hijo, nieto)
			os.rmdir(f)
	subdir = os.listdir(hijo)
	for f in subdir:
			moverArchivo(f, padre)

	os.chdir(padre)



def destruirsubcarpetas(ruta):
	subdir = os.listdir(ruta)
	for f in subdir:
		os.chdir(ruta)
		if os.path.isdir(f):
			carpeta = ruta + "/" + f
			destruirCarpeta(ruta, carpeta)



def organizarAnio(dirs):
	for f in dirs:
		date_file = time.localtime(os.path.getmtime(f))
		month = date_file.tm_mon
		year = date_file.tm_year
		mes_escrito = str(month)
		if(len(mes_escrito) == 1):
			mes_escrito = "0" + mes_escrito
		nombrefol = str(year) + "_" + mes_escrito + " - " + months[month]
		if(nombrefol not in carpetas):
			carpetas.append(nombrefol)
			if(not os.path.exists(nombrefol)):
				os.mkdir(nombrefol)
		shutil.move(f, nombrefol)

def organizarTipo(ruta):
	subdir = os.listdir(ruta)
	for f in subdir:
		os.chdir(ruta)
		if(os.path.isdir(f)):
			organizarTipo(ruta + "/" + f)
	for f in subdir:
		os.chdir(ruta)
		if(os.path.isfile(f)):
			if(f.endswith(".jpg") or f.endswith(".png") or f.endswith(".bmp") or f.endswith(".gif")):
				carpeta = "Imágenes"
			elif(f.endswith(".doc") or f.endswith(".docx") or f.endswith(".xls") or f.endswith(".xlsx") or f.endswith(".ppt") or f.endswith(".pptx") or f.endswith(".ppsx") or f.endswith(".pdf") or f.endswith(".txt") or f.endswith(".dotx")):
				carpeta = "Documentos"
			elif(f.endswith(".mp3") or f.endswith(".wav")):
				carpeta = "Musica"
			else:
				carpeta = "Otros"

			if(not os.path.exists(carpeta)):
				os.mkdir(carpeta)
			shutil.move(f, carpeta)

#INTERFAZ


def elegircarpeta():
	micarpeta = filedialog.askdirectory(initialdir = "/", title = "Seleccione una carpeta...")
	directorio.set(micarpeta)

def organizar():
	origin = os.getcwd()
	prev = origin
	nueva_dir = directorio.get()
	if (mantener.get() == 0):
		texto = " sin "
	else:
		texto = " y "
	valor = "yes" == messagebox.askquestion("Organizar", "¿Deseas organizar los datos en el directorio " + nueva_dir + texto+ "mantener las carpetas existentes?")
	if valor:
		if(os.path.exists(nueva_dir) and os.path.isdir(nueva_dir)):
			os.chdir(nueva_dir)
			origin = nueva_dir
			dirs = os.listdir(origin)

			# ORGANIZA LOS NUEVOS ARCHIVOS POR AÑO

			if(mantener.get() == 0):
				destruirsubcarpetas(origin)
				dirs = os.listdir(origin)

			organizarAnio(dirs)

			organizarTipo(origin)

			#FIN
			messagebox.showinfo("Completado", "El directorio seleccionado ha sido organizado.")
			os.chdir(prev)
		else:
			messagebox.showwarning("ERROR", "El directorio seleccionado es inexistente.")
	




#VARIABLES

title = "OrgaFile"
icono = os.getcwd() + "/icono.ico"

bg_root = "#552222"
# bg_root = "#EEEEF8"
bg_frame = "#FFF5A8"
# bg_frame = "#AAAAEE"
pad = 5
fontsize = 12



#LISTAS

carpetas = []
months = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


#ROOT

root = Tk()
root.config(bg = bg_frame)
root.title(title)
if os.path.exists(icono):
	root.iconbitmap(icono)
root.resizable(0, 0)

#MENU

barraMenu = Menu(root)
root.config(menu = barraMenu)

opcionesMenu = Menu(barraMenu, tearoff = 0)

def borrarTodo():
	mantener.set(1)
	directorio.set("")

opcionesMenu.add_command(label = "Borrar todo", command = borrarTodo)
opcionesMenu.add_command(label = "Cerrar", command = lambda: root.destroy())

ayudaMenu = Menu(barraMenu, tearoff = 0)

texto_acercade = "Simplicidad, Facilidad,\nOtra forma de trabajar\n\n"
texto_formadeuso ="Este programa organiza los archivos por año y mes, y luego los clasifica en Imágenes, Documentos y Otros.\n\nCon el botón Buscar elija la carpeta que contenga los archivos a organizar. Luego elija si quiere mantener las carpetas que se encuentren dentro del directorio o no.\n\nPara ejecutar la tarea, pulse Organizar y confirme la acción.\nPROHIBIDA SU REDISTRIBUCIÓN\n\n¡Disfrute el programa!"
texto_contacto = "Federx\n\nMail: federxc@gmail.com"

ayudaMenu.add_command(label = "Acerca de...", command = lambda: messagebox.showinfo("Acerca de...", texto_acercade))
ayudaMenu.add_command(label = "Forma de uso", command = lambda: messagebox.showinfo("Forma de uso", texto_formadeuso))
ayudaMenu.add_command(label = "Contacto", command = lambda: messagebox.showinfo("Contacto", texto_contacto))

barraMenu.add_cascade(label = "Opciones", menu = opcionesMenu)
barraMenu.add_cascade(label = "Ayuda", menu = ayudaMenu)


#FRAME

frameTitulo = Label(root, text = title, font = ("bold", fontsize * 2), bg = bg_frame, fg = bg_root, padx = pad, pady = pad)
frameTitulo.pack()


miFrame = Frame(root, bg = bg_frame)
miFrame.pack(ipadx = pad, ipady = pad)

directorio = StringVar()

Label(miFrame, text = "Directorio:", font = fontsize, bg = bg_frame).grid(row = 0, column = 0, padx = pad, pady = pad, sticky = "nswe")

cuadroTexto = Entry(miFrame, width = 40, textvariable = directorio, font = fontsize)
cuadroTexto.grid(row = 0, column = 1, padx = pad, pady = pad, sticky = "nswe")

buscar = Button(miFrame, text = "Buscar", font = fontsize, cursor = "hand2", command = elegircarpeta)
buscar.grid(row = 0, column = 2, padx = pad, pady = pad)

mantener = IntVar()
mantener.set(1)

Checkbutton(miFrame, text="Mantener carpetas existentes", font = fontsize, bg = bg_frame, cursor = "hand2", variable = mantener, onvalue = 1, offvalue = 0).grid(row = 1, column = 1, padx = pad, pady = pad)

organizar = Button(miFrame, text = "Organizar", font = fontsize, cursor = "hand2", command = organizar)
organizar.grid(row = 2, column = 0, columnspan = 3, padx = pad, pady = pad)


root.mainloop()