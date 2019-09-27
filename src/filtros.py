#
#
# biblioteca para aplicação de filtros
#
#


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.fftpack import fftn, ifftn, fftshift

def median_filter(img): # função para aplicar mediana no pixel
    k = 3
    m, n = img.shape
    img_filtered = np.copy(img)
    for x in range(0, m):           #percorre toda a imagem
        for y in range(0, n):
            if((x-k >= 0 and x+k < m) and (y-k >= 0 and y+k < n)):  # para cada pixel avalia sua vizinhança
                flat = img[x-k:x+k+1,y-k: y+k+1].flatten()          # e utiliza a mediana dos valores no pixel
                flat.sort()
                img_filtered[x, y] = flat[len(flat)//2]

    return img_filtered #retorna a imagem filtrada

def cut(img):                                                               # função para cortar o spectro de fourier removendo interferencias

    img_fft = fftn(img)                                                     #aplica a transformação de fourier
    img_fft_shift = fftshift(img_fft)                                       #shifta o spectro do fourier para centralizar as bordas
    
    plt.imshow(np.abs(img_fft_shift), cmap='gray', norm=LogNorm(vmin=5))    # apresenta o spectro formado
    plt.show()

    img_fft_shift_filtered = np.copy(img_fft_shift)  #copia imagem

    #for x in range(img.shape[0]):                                          # remove partes da imagem deixando apenas 
    #    for y in range(img.shape[1]):                                      # o 1/3 central da imagem (remove horizontal superior e inferior)   
    #        or y < img.shape[1]//3 or y > img.shape[1]*2//3):              #comentado para ver o efeito de remover apenas#apenas linhas horizontais
    #            img_fft_shift_filtered[x,y] = 0                            #apenas linhas horizontais

    for x in range(img.shape[0]):                                           # remove o restante horizontal da imagem
        for y in range(img.shape[1]):                                       # deixando apenas o centro quadrado de 1/3 de cada dimensão
            if( x < img.shape[0]//3 or x > img.shape[0]*2//3):
                img_fft_shift_filtered[x,y] = 0 

    plt.imshow(np.abs(img_fft_shift_filtered), cmap='gray', norm=LogNorm(vmin=5))
    plt.show()                                                              #mostra o spectro cortado
    res = ifftn( fftshift(img_fft_shift_filtered) )                         # cria a imagem final utilizando a inversa

    return res                                                              #return cut image

def low_pass(img): # função que aplica o filtro low pass

    radius = 501                                    #define variáveis necessárias
    final_shape = img.shape
    
    img_fft = fftn(img)                             #aplica a transformada de fourier
    img_fft_shift = fftshift(img_fft)               #shifita a imagem
    plt.imshow(np.abs(img_fft_shift), cmap='gray', norm=LogNorm(vmin=5))
    plt.show()                                      #apresenta o espectro obtido

    filt = np.zeros((radius, radius))   #cria matriz do filtro
  
    for x in range(radius):     #cria região circular representante do filtro
        for y in range(radius): 
            if (radius//2 - x)**2 + (radius//2 - y)**2 < (radius//2)**2:
                filt[x][y] = 1

    plt.imshow(filt, cmap='gray')   #mostra o filtro
    plt.show()

    aux1 = final_shape[0] - filt.shape[0]   #calcula diferença do filtro e da imagem real para criar padding
    if(aux1%2 == 0):                        
        pad_cols = ( (final_shape[0] - filt.shape[0])//2, \
                    (final_shape[0] - filt.shape[0])//2)
    else:                                   
        pad_rows = ( (final_shape[0] - filt.shape[0])//2+1, \
                     (final_shape[0] - filt.shape[0])//2+1 )

    aux2 = final_shape[1] - filt.shape[1]   
    if(aux2%2 == 0):                        
        pad_cols = ( (final_shape[1] - filt.shape[1])//2, \
                     (final_shape[1] - filt.shape[1])//2)
    else:                                   
        pad_cols = ( (final_shape[1] - filt.shape[1])//2+1, \
                     (final_shape[1] - filt.shape[1])//2+1)

    pad_shape = (pad_rows, pad_cols)        #define o padding

    filt = np.pad(filt, pad_shape, 'constant', constant_values=0)
                                             # verifica valores pares e impares do tamanho da imagem
    if(aux1%2 != 0 and aux2%2 != 0):         
        filt = filt[0:filt.shape[0]-1, 0:filt.shape[1]-1]
    elif(aux1%2 != 0 and aux2%2 == 0):       
        filt = filt[0:filt.shape[0]-1, 0:filt.shape[1]]
    elif(aux1%2 == 0 and aux2%2 != 0):
        filt = filt[0:filt.shape[0], 0:filt.shape[1]-1]

    #print(filt.shape)               #printa o filtro com padding
    plt.imshow(filt, cmap='gray')
    plt.show()

    img_fft_shift_filtered = img_fft_shift * filt   #aplica o filtro na imagem
    plt.imshow(np.abs(img_fft_shift_filtered), cmap='gray', norm=LogNorm(vmin=5))
    plt.show()                                      #mostra o spectro gerado 
    res = ifftn( fftshift(img_fft_shift_filtered) ) # aplica a inversa para gerar o resultado final

    return res


def bandstop(img):  #funçaõ que aplica o bandstop

    threshold = 0.0001  #define o threshold

    img_fft = fftn(img) #aplica o fourier

    #pega os valores das bordas, onde deverá estar o maior valor
    borders = [
        img_fft[0, 0],
        img_fft[0, img.shape[1]-1],
        img_fft[img.shape[0]-1, 0],
        img_fft[img.shape[0]-1, img.shape[1]-1]
    ]

    #seleciona o maior valor e calcula o threshold
    borders = np.array(borders)
    max_value = np.max(borders)
    T = threshold * np.abs(max_value)
    print("Max: ", np.max(img_fft)) #mostra o maior e menor valor e o threshold definido
    print("Min: ", np.min(img_fft))
    print("Threshold: ", T)
    img_fft_shifted = fftshift(img_fft) #aplica o shift na imagem

    center_x = img_fft_shifted.shape[0]//2  #marca o centro da imagem e o raio
    center_y = img_fft_shifted.shape[1]//2
    radius = img_fft_shifted.shape[0] // 6 
    
    # aplica o threshold fora do circulo central
    for x in range(img_fft_shifted.shape[0]):
        for y in range(img_fft_shifted.shape[1]):
            if (center_x - x)**2 + (center_y - y)**2 > (radius)**2 and np.abs(img_fft_shifted[x, y]) > T :
                img_fft_shifted[x, y] = 0
    
    # mostra o spectro após a filtragem
    plt.imshow(np.abs(img_fft_shifted), cmap='gray', norm=LogNorm(vmin=5))
    plt.show()

    return np.abs(ifftn(fftshift(img_fft_shifted)))