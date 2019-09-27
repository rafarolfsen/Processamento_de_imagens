#
#
# biblioteca para aplicação de interferencias
#
#

import numpy as np


def diagonal_noise(img):    # cria linhas diagonais pretas a cada 3 linhas

    img_noise = np.copy(img)     # copia imagem

    for x in range(img_noise.shape[0]):         # loop responsavel por pintar as linhas pretas
        for y in range(img_noise.shape[1]):
            if( (x*img_noise.shape[0]+y) % 3 == 0):
                img_noise[x,y] = 0

    return img_noise            #retorna a imagem com interferencia

def horizontal_noise(img):  # cria linhas horizontais a cada 3 pixeis da imagem

    img_noise = np.copy(img)    # copia imagem

    for x in range(0,img_noise.shape[0],3): # loop responsavel por pintar as linhas pretas
        for y in range(img_noise.shape[1]):
            img_noise[x,y] = 0

    return img_noise    # retorna a imagem com interferencia

def vertical_noise(img):    # cria linhas verticais a cada 3 pixeis da imagem

    img_noise = np.copy(img)    # copia imagem

    for x in range(img_noise.shape[0]): # loop responsavel por pintar as linhas pretas
        for y in range(0,img_noise.shape[1],3):
            img_noise[x,y] = 0

    return img_noise    # retorna imagem com interferencia
