def filtro_mediana_2d(imagen, ventana=3):
    alto = len(imagen)
    ancho = len(imagen[0])
    mitad = ventana // 2

    nueva = [[0 for _ in range(ancho)] for _ in range(alto)]

    for i in range(alto):
        for j in range(ancho):
            vecinos = []
            for di in range(-mitad, mitad + 1):
                for dj in range(-mitad, mitad + 1):
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < alto and 0 <= nj < ancho:
                        vecinos.append(imagen[ni][nj])
            vecinos.sort()
            nueva[i][j] = vecinos[len(vecinos) // 2]
    
    return nueva
