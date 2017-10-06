#coding: utf-8

'''
Autor: Fabio Felix
Nome: Mouse Virtual
https://github.com/fabix83/Mouse_Virtual_Python

Este programa é um software livre: você pode redistribuí-lo e/ou modificá-lo.

Este programa é distribuído com a esperança de que seja útil, mas
SEM QUALQUER GARANTIA; sem a garantia implícita de COMERCIALIZAÇÃO
ou APTIDÃO PARA UM DETERMINADO PROPÓSITO.

'''

from Tkinter import *
from winsound import *
import threading
import time
import pyautogui

pyautogui.FAILSAFE = False #Desabilita o Fail Safe do pyautogui

#STATUS
statusOFF = True
statusEsquerdo = False
statusDireito = False
statusSegurar = False
statusDuploClique = False

#Primeiras Informações da Tela e Definição da Margem que será definida como raio
largura_tela, altura_tela = pyautogui.size()
margem = (largura_tela*3) / 100
largura_janela = 336
altura_janela = 56

#sinais utilizados
sinal_thread = True
sinal_desativa = False

#Trabalhando com String
TAMANHO_JANELA = str(largura_janela)+'x'+str(altura_janela)
pos_janela = '+500+0'
pos_desativa = str(altura_tela - altura_janela)

'''
    Funcao que ira comparar se os pontos estão na margem definida para a ação ser efetuada
'''
def estaNoRaio(pos_x_inicio, pos_y_inicio, pos_x_fim, pos_y_fim):
    global margem
    if((pos_x_fim >= pos_x_inicio - (margem/2) and pos_x_fim <= (pos_x_inicio + (margem/2))) and (pos_y_fim >= pos_y_inicio - (margem/2) and (pos_y_fim <= pos_y_inicio + (margem/2)))):
        return True
    return False

'''
    Função de Clique definida de acordo com as Tag Selecionada
'''
def clique():
    global statusOFF
    global statusEsquerdo
    global statusDireito
    global statusSegurar
    global statusDuploClique

    if (statusOFF):
        return False
    elif (statusEsquerdo):
        pyautogui.click(button='left')
    elif (statusDireito):
        pyautogui.rightClick()
    elif(statusDuploClique):
        pyautogui.doubleClick()
    elif(statusSegurar):
        pyautogui.mouseDown()
        statusSegurar = False
    else:
        pyautogui.mouseUp()
        statusSegurar = True

'''
    Animacao dos Botoes ao efetuar clique
'''
def pisca():
    global statusOFF
    global statusEsquerdo
    global statusDireito
    global statusDuploClique
    global statusSegurar

    if (statusOFF):
        return False
    elif (statusEsquerdo):
        PlaySound('click0.wav', SND_FILENAME)
        button_image_ESQUERDO['relief'] = SUNKEN
        photo = PhotoImage(file = "l2.gif")
        button_image_ESQUERDO.config(image=photo)
        button_image_ESQUERDO.image = photo
        time.sleep(0.3)
        button_image_ESQUERDO['relief'] = FLAT
        photo = PhotoImage(file = "l1.gif")
        button_image_ESQUERDO.config(image=photo)
        button_image_ESQUERDO.image = photo
    elif (statusDireito):
        PlaySound('click0.wav', SND_FILENAME)
        button_image_DIREITO['relief'] = SUNKEN
        photo = PhotoImage(file = "r2.gif")
        button_image_DIREITO.config(image=photo)
        button_image_DIREITO.image = photo
        time.sleep(0.3)
        photo = PhotoImage(file = "r1.gif")
        button_image_DIREITO.config(image=photo)
        button_image_DIREITO.image = photo
        button_image_DIREITO['relief'] = FLAT
    elif(statusDuploClique):
        PlaySound('click0.wav', SND_FILENAME)
        button_image_CLIQUEDUPLO['relief'] = SUNKEN
        photo = PhotoImage(file = "c22.gif")
        button_image_CLIQUEDUPLO.config(image=photo)
        button_image_CLIQUEDUPLO.image = photo
        time.sleep(0.3)
        photo = PhotoImage(file = "c21.gif")
        button_image_CLIQUEDUPLO.config(image=photo)
        button_image_CLIQUEDUPLO.image = photo
        button_image_CLIQUEDUPLO['relief'] = FLAT
    elif(statusSegurar):
        PlaySound('click0.wav', SND_FILENAME)
        button_image_ARRASTAR['relief'] = SUNKEN
        photo = PhotoImage(file = "d2.gif")
        button_image_ARRASTAR.config(image=photo)
        button_image_ARRASTAR.image = photo
        time.sleep(0.3)
        photo = PhotoImage(file = "d1.gif")
        button_image_ARRASTAR.config(image=photo)
        button_image_ARRASTAR.image = photo
        button_image_ARRASTAR['relief'] = FLAT
    else:
        PlaySound('click1.wav', SND_FILENAME)
        button_image_ARRASTAR['relief'] = SUNKEN
        photo = PhotoImage(file = "d2.gif")
        button_image_ARRASTAR.config(image=photo)
        button_image_ARRASTAR.image = photo
        time.sleep(0.3)
        photo = PhotoImage(file = "d1.gif")
        button_image_ARRASTAR.config(image=photo)
        button_image_ARRASTAR.image = photo
        button_image_ARRASTAR['relief'] = FLAT

def atualiza():
    global statusOFF
    global statusEsquerdo
    global statusDireito
    global statusDuploClique
    global statusSegurar

    if (statusOFF):
        desativaEsquerdo()
        desativaDireito()
        desativaArrastar()
        desativaDuploClique()
    elif (statusEsquerdo):
        desativaDireito()
        desativaArrastar()
        desativaDuploClique()
    elif (statusDireito):
        desativaEsquerdo()
        desativaArrastar()
        desativaDuploClique()
    elif (statusDuploClique):
        desativaEsquerdo()
        desativaDireito()
        desativaArrastar()
    elif (statusSegurar):
        desativaEsquerdo()
        desativaDireito()
        desativaDuploClique()

'''
    Thread que permite o uso das operações do mouse
'''
class App(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        global sinal_thread

        while (sinal_thread):
            pos_x_inicio, pos_y_inicio = pyautogui.position()
            time.sleep(1)
            pos_x_fim, pos_y_fim = pyautogui.position()

            if (estaNoRaio(pos_x_inicio, pos_y_inicio, pos_x_fim, pos_y_fim)):
                pisca()
                clique()
                atualiza()

#Inicio da Janela
ROOT = Tk()
APP = App(ROOT)

'''
	Função que permite o termino do app
'''
def fechar(event):
    global sinal_thread
    sinal_thread=False
    time.sleep(3)
    ROOT.destroy()

'''
	Funções que ativam os botões
'''
def ativaOFF(event):
    global statusOFF
    global sinal_desativa

    if(not (statusOFF)):
        photo = PhotoImage(file = "off1.gif")
        button_image_OFF.config(image=photo)
        button_image_OFF.image = photo
        statusOFF = True
        ROOT.geometry("56x56+0+"+pos_desativa)

        desativaEsquerdo()
        desativaDireito()
        desativaArrastar()
        desativaDuploClique()
    else:
        desativaOFF()

def ativaEsquerdo(event):
    global statusOFF
    global statusEsquerdo

    if(not (statusOFF) and not(statusEsquerdo)):
        photo = PhotoImage(file = "l1.gif")
        button_image_ESQUERDO.config(image=photo)
        button_image_ESQUERDO.image = photo
        statusEsquerdo = True

        desativaDireito()
        desativaArrastar()
        desativaDuploClique()


def ativaDireito(event):
    global statusOFF
    global statusDireito

    if (not (statusDireito) and not (statusOFF)):
        photo = PhotoImage(file="r1.gif")
        button_image_DIREITO.config(image=photo)
        button_image_DIREITO.image = photo
        statusDireito = True

        desativaEsquerdo()
        desativaArrastar()
        desativaDuploClique()


def ativaArrastar(event):
    global statusOFF
    global statusSegurar

    if (not(statusSegurar) and not(statusOFF)):
        photo = PhotoImage(file="d1.gif")
        button_image_ARRASTAR.config(image=photo)
        button_image_ARRASTAR.image = photo
        statusSegurar = True

        desativaEsquerdo()
        desativaDireito()
        desativaDuploClique()


def ativaDuploClique(event):
    global statusOFF
    global statusDuploClique
    if (not (statusDuploClique) and not (statusOFF)):
        photo = PhotoImage(file="c21.gif")
        button_image_CLIQUEDUPLO.config(image=photo)
        button_image_CLIQUEDUPLO.image = photo
        statusDuploClique = True

        desativaEsquerdo()
        desativaDireito()
        desativaArrastar()

'''
	Função que move a janela
'''
def moveJanela(event):

    global statusOFF
    statusOFF = True
    atualiza()

    photo = PhotoImage(file="off1.gif")
    button_image_OFF.config(image=photo)
    button_image_OFF.image = photo

    global pos_janela
    sinal = 1

    ROOT.withdraw()

    while (sinal):
        x, y = pyautogui.position()

        #testa se a janela esta proxima ou da direita ou da esquerda
        if ((0 <= x <= 6) or ((largura_tela-7) <= x <= (largura_tela))):
            #janela mais proxima da esquerda
            if(0 <= x <= 6):
                #evita que a janela suma na parte de baixo da tela
                if (y > (altura_tela - altura_janela)):
                    pos_janela = '+0+'+str(altura_tela - altura_janela)
                    ROOT.geometry(TAMANHO_JANELA+pos_janela)
                    time.sleep(1)
                    ROOT.deiconify()
                    sinal = 0
                else:
                    pos_janela = '+0+'+str(y)
                    ROOT.geometry(TAMANHO_JANELA+pos_janela)
                    time.sleep(1)
                    ROOT.deiconify()
                    sinal = 0
            #janela mais proxima da direita
            else:
                #ajustes para janela nao sumir
                if (y > (altura_tela - altura_janela)):
                    pos_janela = '+'+str(largura_tela - largura_janela)+'+'+str(altura_tela - altura_janela)
                    ROOT.geometry(TAMANHO_JANELA+pos_janela)
                    time.sleep(1)
                    ROOT.deiconify()
                    sinal = 0
                else:
                    pos_janela = '+'+str(largura_tela - largura_janela)+'+'+str(y)
                    ROOT.geometry(TAMANHO_JANELA+pos_janela)
                    time.sleep(1)
                    ROOT.deiconify()
                    sinal = 0
        else:
            #testa se a janela esta mais proxima do teto ou do rodape
            if ((0 <= y <= 6) or ((altura_tela-7) <= y <= (altura_tela))):
                #testa se esta proximo do teto
                if (0 <= y <= 6):
                    #testa se a janela nao some no teto
                    if(x > (largura_tela - largura_janela)):
                        pos_janela = '+'+str(largura_tela - largura_janela)+'+0'
                        ROOT.geometry(TAMANHO_JANELA+pos_janela)
                        time.sleep(1)
                        ROOT.deiconify()
                        sinal = 0
                    else:
                        pos_janela = '+'+str(x)+'+0'
                        ROOT.geometry(TAMANHO_JANELA+pos_janela)
                        time.sleep(1)
                        ROOT.deiconify()
                        sinal = 0
                #testa se esta proxima do rodape
                else:
                    # ajustes para nao sumir no rodape direito
                    if (x > (largura_tela - largura_janela)):
                        pos_janela = '+'+str(largura_tela-largura_janela)+'+'+str(altura_tela - altura_janela)
                        ROOT.geometry(TAMANHO_JANELA+pos_janela)
                        time.sleep(1)
                        ROOT.deiconify()
                        sinal = 0
                    else:
                        pos_janela = '+'+str(x)+'+'+str(altura_tela - altura_janela)
                        ROOT.geometry(TAMANHO_JANELA+pos_janela)
                        time.sleep(1)
                        ROOT.deiconify()
                        sinal = 0

'''
	Funções que desativam os botões
'''
def desativaOFF():
    global statusOFF
    statusOFF = False
    photo = PhotoImage(file = "off0.gif")
    button_image_OFF.config(image=photo)
    button_image_OFF.image = photo
    ROOT.geometry(TAMANHO_JANELA+pos_janela)
    ativaEsquerdo("<Enter>")

def desativaEsquerdo():
    global statusEsquerdo
    statusEsquerdo = False
    photo = PhotoImage(file = "l0.gif")
    button_image_ESQUERDO.config(image=photo)
    button_image_ESQUERDO.image = photo

def desativaDireito():
    global statusDireito
    statusDireito = False
    photo = PhotoImage(file = "r0.gif")
    button_image_DIREITO.config(image=photo)
    button_image_DIREITO.image = photo

def desativaArrastar():
    global statusSegurar
    statusSegurar = False
    photo = PhotoImage(file = "d0.gif")
    button_image_ARRASTAR.config(image=photo)
    button_image_ARRASTAR.image = photo

def desativaDuploClique():
    global statusDuploClique
    statusDuploClique = False
    photo = PhotoImage(file = "c20.gif")
    button_image_CLIQUEDUPLO.config(image=photo)
    button_image_CLIQUEDUPLO.image = photo

'''
	CRIAÇÃO DOS BOTOES
'''

#self.button_image_OFF - Desativar Mouse
photo0 = PhotoImage(file = "off1.gif")
button_image_OFF = Button(ROOT, image = photo0)
button_image_OFF.bind("<Enter>", ativaOFF)
button_image_OFF.grid(row=0, column=0)

#self.button_image_ESQUERDO - Esquerdo do Mouse
photo1 = PhotoImage(file = "l0.gif")
button_image_ESQUERDO = Button(ROOT, image = photo1)
button_image_ESQUERDO.bind("<Enter>", ativaEsquerdo)
button_image_ESQUERDO.grid(row=0, column=1)

#self.button_image_DIREITO - Direito do Mouse
photo2 = PhotoImage(file = "r0.gif")
button_image_DIREITO = Button(ROOT, image = photo2)
button_image_DIREITO.bind("<Enter>", ativaDireito)
button_image_DIREITO.grid(row=0, column=2)

#self.button_image_ARRASTAR - Arrastar do Mouse
photo3 = PhotoImage(file = "d0.gif")
button_image_ARRASTAR = Button(ROOT, image = photo3)
button_image_ARRASTAR.bind("<Enter>", ativaArrastar)
button_image_ARRASTAR.grid(row=0, column=3)

#self.button_image_CLIQUEDUPLO - Clique do Mouse
photo4 = PhotoImage(file = "c20.gif")
button_image_CLIQUEDUPLO = Button(ROOT, image = photo4)
button_image_CLIQUEDUPLO.bind("<Enter>", ativaDuploClique)
button_image_CLIQUEDUPLO.grid(row=0, column=4)

#self.button_image_MOVEJANELA - Move Janela
photo5 = PhotoImage(file = "mv0.gif")
button_image_MOVEJANELA = Button(ROOT, image = photo5)
button_image_MOVEJANELA.bind("<Enter>", moveJanela)
button_image_MOVEJANELA.grid(row=0, column=5)

ROOT.bind('<Escape>', fechar)

#Propriedades da Janela
ROOT.geometry("56x56+500+0") #tamanho e posicao da janela larguraxaltura+posicaox(horizontal)+posicaoy(largura-56)
ROOT.attributes('-alpha', 0.30) #transparencia
ROOT.attributes('-topmost', True) #sempre no topo
ROOT.overrideredirect(True) #retira opcoes de fechar e transforma em uma barra

#Event Loop
ROOT.mainloop()