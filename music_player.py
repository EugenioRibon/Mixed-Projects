import os
import random
import time
import random
from pygame import mixer
import pygame
import sys

class Cancion():
    def __init__(self, path, nombre):
        self.path = path
        self.nombre = nombre
        self.next = None
        self.previous = None

    def __str__(self):
        return self.nombre
    
    def tocar(self):
        mixer.music.load(self.path + self.nombre)
        mixer.music.play()
    
    def parar(self):
        mixer.music.stop()

class Lista_doble_enlazada():
    def __init__(self):
        self.head = None
        self.reproduciendo = None
        self.tipo_salto = "normal"

    def cambiar_tipo_salto(self):
        if self.tipo_salto == "normal":
            self.tipo_salto = "aleatorio"
        else:
            self.tipo_salto = "normal"


    def anadir_nodo(self, nodo):
        if not self.head:
            self.head = nodo
            
        else:
            nodo.next = self.head
            self.head.previous = nodo
            self.head = nodo

        self.reproduciendo = self.head

    def mostrar_lista(self):
        nodo = self.head
        while nodo:
            print(nodo)
            nodo = nodo.next

    def reproducir(self):
        self.reproduciendo.tocar()

    def next_song(self):
        self.reproduciendo.parar()
        if self.tipo_salto == "aleatorio":
            saltos = random.randint(1, 8)
            for _ in range(saltos + 1):
                if not self.reproduciendo.next:
                    self.reproduciendo = self.head
                else:
                    self.reproduciendo = self.reproduciendo.next
            
        else:
            if not self.reproduciendo.next:
                return False
            self.reproduciendo = self.reproduciendo.next
        self.reproduciendo.tocar()
        return True

    def previous(self):
        self.reproduciendo.parar()
        
        if not self.reproduciendo.previous:
            return False
        self.reproduciendo = self.reproduciendo.previous
        self.reproduciendo.tocar()
        return True


if __name__ == "__main__":

    
    pygame.init()

    # Display
    ancho = 640
    alto = 700
    screen = pygame.display.set_mode((ancho, alto))

    running = True


    mixer.init()

    path='./songs/'
    files = os.listdir(path)

    lista = Lista_doble_enlazada()
    for file in files:
        cancion = Cancion(path, file)
        lista.anadir_nodo(cancion)

    lista.mostrar_lista()

    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    lista.reproducir()
                elif event.key == pygame.K_RIGHT:
                    running = lista.next_song()
                    #Aqui va el código de avanzar 
                elif event.key == pygame.K_LEFT:
                    running = lista.previous()
                    #Aqui va el código de volver a la anterior
                elif event.key == pygame.K_SPACE:
                    lista.cambiar_tipo_salto()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()

            # while pygame.mixer.music.get_busy():
            #     song_length = pygame.mixer.music.get_length()
            #     # Calculate how much time is left
            #     time_left = song_length - pygame.mixer.music.get_pos()

            #     # Convert milliseconds to seconds and round to 2 decimal places
            #     time_left = round(time_left / 1000, 2)

            #     # Print the time left
            #     print(f'Time left: {time_left} seconds')
            
    pygame.display.update()
    
    # for i in range(300):
    #     sel1 = random.choice(files)
    #     sel2=path+sel1
    #     print("Sonando:", sel1)
    #     mixer.music.load(sel2) # you may use .mp3 but support is limited
    #     mixer.music.play()
    #     time.sleep(260)
    mixer.music.stop()
