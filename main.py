import numpy as np
import imageio
import matplotlib.pyplot as plt
import sys
import src.interferencia, src.filtros
from matplotlib.colors import LogNorm


def rgb2gray(rgb):      #função para transformar a imagem RGB para tons de cinza
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def noise_menu():       #função para selecionar a opção de interferencia
    print("escolha quais opções de interferência deseja aplicar (ex:3 2):")
    print("(1) Interferência horizontal")
    print("(2) Interferência vertical")
    print("(3) Interferência diagonal")

    options = [int(opt) for opt in input().split()]

    return options

def filter_menu():       #função para selecionar a opção de filtro
    print("escolha quais opções de filtro deseja aplicar (ex:3 2):")
    print("(1) filtro de mediana")
    print("(2) filtro de corte de spectro")
    print("(3) filtro de fourier(low pass)")
    print("(4) filtro de fourier(bandstop)")

    options = [int(opt) for opt in input().split()]

    return options


if __name__ == '__main__':

    if len(sys.argv) != 2:                                  # pede a execução do programa com 
        print('usage: python3 main.py <INPUT IMAGE>')       # a imagem de entrada como argv[1]
        exit(0)

    img_orig = imageio.imread(sys.argv[1])                  # lê a imagem de entrada

    img_gray = rgb2gray(img_orig)                           # transforma a imagem em tons de cinza

    #print(img_gray.shape)                                   # mostra as dimensoes da imagem


    plt.imshow(img_gray, cmap='gray')                       # mostra a imagem original em tons de cinza
    plt.show()

    noise_options = noise_menu()                            # chama função para selecionar interferencias

    img_noise = np.copy(img_gray)                           #copia imagem

    for x in range( len(noise_options) ):                   #aplica as interferências selecionados
        if(noise_options[x] == 1):
            print("Aplcando interfência horizontal...\n")
            img_noise = src.interferencia.horizontal_noise(img_noise)
        elif(noise_options[x] == 2):
            print("Aplcando interfência vertical...\n")
            img_noise = src.interferencia.vertical_noise(img_noise)
        elif(noise_options[x] == 3):
            print("Aplcando interfência diagonal...\n")
            img_noise = src.interferencia.diagonal_noise(img_noise)

    plt.imshow(img_noise, cmap='gray')                      #mostra a imagem com interferencia
    plt.show()

    filter_options = filter_menu()                          # chama função para selecionar filtros

    for x in range( len(filter_options) ):                  #aplica os filtros selecionados
        if(filter_options[x] == 1):                         # e apresenta a imagem filtrada
            print("Aplcando filtro de mediana...\n")
            img_filtered = src.filtros.median_filter(img_noise)
            plt.imshow(img_filtered, cmap='gray')
            plt.show()
        elif(filter_options[x] == 2):
            print("Aplcando filtro de corte...\n")
            img_filtered = src.filtros.cut(img_noise)
            plt.imshow(np.abs(img_filtered), cmap='gray', norm=LogNorm(vmin=5))
            plt.show()
        elif(filter_options[x] == 3):
            print("Aplcando filtro low pass...\n")
            img_filtered = src.filtros.low_pass(img_noise)
            plt.imshow(np.abs(img_filtered), cmap='gray', norm=LogNorm(vmin=5))
            plt.show()  
        elif(filter_options[x] == 4):
            print("Aplcando filtro de threshold...\n")
            img_filtered = src.filtros.bandstop(img_noise)
            plt.imshow(img_filtered, cmap='gray')
            plt.show()                                    

