# ============================================================
# TP Integrador - Sistema de Gestión de Inventario
# Fundamentos de Informática - UADE
# Grupo 8: Katavic, Iñaki - Piñeyro, Ignacio
#
# Estructura de la matriz (lista de listas). Cada fila es un producto:
#   columna 0: codigo    (int, único)
#   columna 1: nombre    (str)
#   columna 2: categoria (str)
#   columna 3: precio    (float)
#   columna 4: stock     (int)
# ============================================================


# ------------------------------------------------------------
# BÚSQUEDA SECUENCIAL
# Va primero porque alta, baja y modificar_stock la usan para saber
# si un código existe. Así no repetimos esa lógica en cada función.
# ------------------------------------------------------------

# busqueda_secuencial: recorre la matriz fila por fila comparando el código.
# Parámetros: matriz (lista de listas), codigo (int)
# Retorna dos valores: el índice de la fila (o -1 si no está)
#                      y la cantidad de comparaciones realizadas.
def busqueda_secuencial(matriz, codigo):
    comparaciones = 0

    # for + range(len(matriz)): i toma los valores 0, 1, 2, ... hasta la
    # última fila. len(matriz) es la cantidad de filas (productos).
    for i in range(len(matriz)):
        comparaciones += 1  # += suma 1 al contador en cada comparación

        # matriz[i] es la fila i (un producto) y matriz[i][0] es el
        # dato de la columna 0 de esa fila, o sea, su código.
        if matriz[i][0] == codigo:
            return i, comparaciones  # return corta la función y devuelve dos valores

    # Si el for terminó sin encontrarlo, el código no está en la matriz
    return -1, comparaciones


# ------------------------------------------------------------
# ALTA, BAJA Y MODIFICACIÓN DE STOCK
# ------------------------------------------------------------

# tiene_coma: indica si un texto tiene alguna coma.
# Hace falta porque el CSV separa los campos con comas: un nombre con
# coma rompería esa línea del archivo al guardarlo.
# Parámetro: texto (str). Retorna: True si tiene coma, False si no.
def tiene_coma(texto):
    # for sobre un texto: en cada vuelta, "letra" es un carácter del texto
    for letra in texto:
        if letra == ",":
            return True
    return False


# alta_producto: agrega un producto nuevo al final de la matriz.
# Parámetros: matriz, codigo (int), nombre (str), categoria (str),
#             precio (número), stock (int)
# Retorna: True si lo agregó.
#          False si el código ya existe o algún dato no es válido.
def alta_producto(matriz, codigo, nombre, categoria, precio, stock):
    # strip() borra los espacios del principio y del final del texto
    nombre = nombre.strip()
    categoria = categoria.strip()

    # Validaciones con if. Con "or" alcanza con que UNA de las condiciones
    # sea verdadera para rechazar el producto.
    if codigo <= 0 or nombre == "" or categoria == "":
        return False
    if tiene_coma(nombre) or tiene_coma(categoria):
        return False
    if precio < 0 or stock < 0:
        return False

    # El código tiene que ser único: lo buscamos con la búsqueda secuencial
    indice, comparaciones = busqueda_secuencial(matriz, codigo)
    if indice != -1:
        return False

    # float() asegura que el precio quede como número con decimales (3500.0)
    fila_nueva = [codigo, nombre, categoria, float(precio), stock]
    matriz.append(fila_nueva)  # append agrega la fila al final de la matriz
    return True


# baja_producto: elimina de la matriz el producto con ese código.
# Parámetros: matriz, codigo (int)
# Retorna: True si lo eliminó, False si el código no existe.
def baja_producto(matriz, codigo):
    indice, comparaciones = busqueda_secuencial(matriz, codigo)

    # Si el índice es -1, el producto no existe y no hay nada que borrar
    if indice == -1:
        return False

    matriz.pop(indice)  # pop(indice) saca de la lista la fila de esa posición
    return True


# modificar_stock: suma "cantidad" (positiva o negativa) al stock del producto.
# Parámetros: matriz, codigo (int), cantidad (int)
# Retorna: True si modificó el stock.
#          False si el producto no existe o si el stock quedaría negativo.
def modificar_stock(matriz, codigo, cantidad):
    indice, comparaciones = busqueda_secuencial(matriz, codigo)
    if indice == -1:
        return False

    # matriz[indice][4] es la columna 4 (stock) de la fila encontrada.
    # Primero calculamos el resultado y recién después decidimos si se guarda.
    nuevo_stock = matriz[indice][4] + cantidad
    if nuevo_stock < 0:
        return False

    matriz[indice][4] = nuevo_stock
    return True


# ------------------------------------------------------------
# ARCHIVO CSV (carga y guardado)
# ------------------------------------------------------------

# cargar_csv: lee el archivo CSV y devuelve la matriz de productos.
# Cada línea se agrega con alta_producto, así se aplican las mismas
# validaciones que en el alta (y se rechazan los códigos repetidos).
# Parámetro: nombre_archivo (str)
# Retorna: la matriz (lista de listas). Si el archivo no existe, una matriz vacía.
def cargar_csv(nombre_archivo):
    matriz = []  # matriz vacía: acá vamos agregando cada producto

    # try / except: intenta hacer lo que está en el try; si ocurre el error
    # indicado en el except, en vez de cortarse el programa se ejecuta ese bloque.
    # encoding="utf-8" indica cómo están guardadas las letras con tilde y la ñ.
    try:
        archivo = open(nombre_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()  # lista con todas las líneas del archivo
        archivo.close()
    except FileNotFoundError:
        # El archivo no está en la carpeta desde donde se ejecuta el programa
        print("No se encontró el archivo", nombre_archivo)
        print("Ejecute el programa desde la carpeta donde está el archivo (por ejemplo, con IDLE y F5).")
        print("Se inicia con el inventario vacío.")
        return matriz
    except UnicodeDecodeError:
        # Pasa si el archivo se guardó con Excel u otro programa que no usa UTF-8.
        # Lo volvemos a leer con "latin-1": puede leer cualquier archivo sin error
        # y, para las letras del castellano (á, é, ñ...), coincide con la
        # codificación que usa Excel en Windows. Al guardar, queda otra vez en UTF-8.
        archivo = open(nombre_archivo, "r", encoding="latin-1")
        lineas = archivo.readlines()
        archivo.close()

    # for + range: range(1, len(lineas)) arranca en 1 (y no en 0)
    # para saltear la primera línea, que es el encabezado.
    for i in range(1, len(lineas)):
        linea = lineas[i].strip()  # strip() saca el salto de línea del final

        if linea != "":  # ignoramos las líneas vacías
            campos = linea.split(",")  # corta la línea en cada coma -> lista de textos

            if len(campos) == 5:
                # int() y float() dan ValueError si el texto no es un número
                try:
                    codigo = int(campos[0])
                    precio = float(campos[3])
                    stock = int(campos[4])
                    if not alta_producto(matriz, codigo, campos[1], campos[2], precio, stock):
                        print("Línea ignorada (código repetido o dato inválido):", linea)
                except ValueError:
                    print("Línea ignorada (dato que no es un número):", linea)
            else:
                print("Línea ignorada (no tiene 5 campos):", linea)

    return matriz


# guardar_csv: escribe la matriz en el archivo, con la línea de encabezado
# y un producto por línea (campos separados por coma).
# Parámetros: matriz, nombre_archivo (str)
# Retorna: True si pudo guardar, False si no tenía permiso para escribir
#          el archivo (por ejemplo, porque está abierto en Excel).
def guardar_csv(matriz, nombre_archivo):
    # modo "w" (write): crea el archivo, o lo BORRA y lo reescribe si ya existía
    try:
        archivo = open(nombre_archivo, "w", encoding="utf-8")
    except PermissionError:
        return False

    archivo.write("codigo,nombre,categoria,precio,stock\n")  # "\n" es el salto de línea

    for fila in matriz:
        # str() convierte un número en texto, porque con "+" solo se pueden unir textos
        linea = str(fila[0]) + "," + fila[1] + "," + fila[2] + "," + str(fila[3]) + "," + str(fila[4]) + "\n"
        archivo.write(linea)

    archivo.close()  # cerrar el archivo asegura que todo quede escrito
    return True


# ------------------------------------------------------------
# ORDENAMIENTO (selección e inserción, como en la Clase 12)
# Columnas: 0 código, 1 nombre, 2 categoría, 3 precio, 4 stock
# En las dos funciones se compara el dato de una columna, pero se
# mueve la FILA completa, para que cada producto no se desarme.
# ------------------------------------------------------------

# ordenar_seleccion: ordena la matriz de menor a mayor según la columna,
# con el método de selección.
# Parámetros: matriz, columna (int). Retorna: la matriz ordenada.
def ordenar_seleccion(matriz, columna):
    # El for de afuera elige la posición i que se va a completar
    for i in range(len(matriz) - 1):
        minimo = i  # suponemos que el menor está en la posición i

        # El for de adentro recorre el resto buscando un valor más chico
        for j in range(i + 1, len(matriz)):
            if matriz[j][columna] < matriz[minimo][columna]:
                minimo = j

        # Intercambio de las dos filas con asignación múltiple
        matriz[i], matriz[minimo] = matriz[minimo], matriz[i]

    return matriz


# ordenar_insercion: ordena la matriz de menor a mayor según la columna,
# con el método de inserción (como ordenar cartas en la mano).
# Parámetros: matriz, columna (int). Retorna: la matriz ordenada.
def ordenar_insercion(matriz, columna):
    # Arranca en 1: la fila 0 sola ya cuenta como parte ordenada
    for i in range(1, len(matriz)):
        fila_actual = matriz[i]  # la fila que hay que insertar
        j = i - 1

        # while: retrocede MIENTRAS j sea una posición válida Y la fila de
        # esa posición sea mayor. Cada fila mayor se corre un lugar a la derecha.
        while j >= 0 and matriz[j][columna] > fila_actual[columna]:
            matriz[j + 1] = matriz[j]
            j = j - 1

        matriz[j + 1] = fila_actual  # la insertamos en el hueco que quedó

    return matriz


# ------------------------------------------------------------
# BÚSQUEDA BINARIA (como en la Clase 11)
# ------------------------------------------------------------

# busqueda_binaria: busca el código dividiendo la zona de búsqueda a la mitad.
# IMPORTANTE: la matriz tiene que estar ORDENADA por código (columna 0).
# Parámetros: matriz (ordenada por código), codigo (int)
# Retorna dos valores: el índice de la fila (o -1 si no está)
#                      y la cantidad de comparaciones realizadas.
def busqueda_binaria(matriz, codigo):
    izquierda = 0               # límite izquierdo de la zona donde buscamos
    derecha = len(matriz) - 1   # límite derecho
    comparaciones = 0

    # while: repite MIENTRAS quede una zona para revisar
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2  # // es la división entera
        comparaciones += 1

        if matriz[medio][0] == codigo:
            return medio, comparaciones
        elif matriz[medio][0] < codigo:
            izquierda = medio + 1  # está a la derecha: descartamos la mitad izquierda
        else:
            derecha = medio - 1    # está a la izquierda: descartamos la mitad derecha

    return -1, comparaciones


# ------------------------------------------------------------
# REPORTES (máximo y mínimo calculados a mano, sin max() ni min())
# ------------------------------------------------------------

# stock_bajo: arma una lista con los productos cuyo stock es menor al umbral.
# Parámetros: matriz, umbral (int). Retorna: lista de filas (puede quedar vacía).
def stock_bajo(matriz, umbral):
    productos_bajos = []

    for fila in matriz:  # en cada vuelta, "fila" es un producto
        if fila[4] < umbral:  # fila[4] es el stock
            productos_bajos.append(fila)

    return productos_bajos


# valor_total: suma precio × stock de todos los productos.
# Parámetro: matriz. Retorna: el total (0.0 si la matriz está vacía).
def valor_total(matriz):
    total = 0.0  # acumulador: arranca en 0 y va sumando en cada vuelta

    for fila in matriz:
        total = total + fila[3] * fila[4]  # precio (col 3) por stock (col 4)

    return total


# producto_mas_caro: devuelve la fila del producto con el precio más alto.
# Si hay empate, devuelve el primero. Con la matriz vacía devuelve [].
def producto_mas_caro(matriz):
    if len(matriz) == 0:
        return []

    mas_caro = matriz[0]  # suponemos que el primero es el más caro

    # Recorremos desde la fila 1; si alguna es más cara, pasa a ser la candidata
    for i in range(1, len(matriz)):
        if matriz[i][3] > mas_caro[3]:
            mas_caro = matriz[i]

    return mas_caro


# producto_mas_barato: devuelve la fila del producto con el precio más bajo.
# Si hay empate, devuelve el primero. Con la matriz vacía devuelve [].
def producto_mas_barato(matriz):
    if len(matriz) == 0:
        return []

    mas_barato = matriz[0]  # suponemos que el primero es el más barato

    for i in range(1, len(matriz)):
        if matriz[i][3] < mas_barato[3]:
            mas_barato = matriz[i]

    return mas_barato


# ------------------------------------------------------------
# FUNCIONES AUXILIARES PARA PEDIR DATOS AL USUARIO
# ------------------------------------------------------------

# pedir_entero: pide un número entero y repite la pregunta hasta que sea válido.
# Parámetro: mensaje (str). Retorna: el número ingresado (int).
def pedir_entero(mensaje):
    valor = 0
    valido = False  # "bandera": indica si ya tenemos un dato correcto

    # while not valido: repite MIENTRAS valido sea False
    while not valido:
        texto = input(mensaje)
        # int(texto) da ValueError si el texto no es un entero ("abc", "3.5")
        try:
            valor = int(texto)
            valido = True
        except ValueError:
            print("Error: ingrese un número entero.")

    return valor


# pedir_decimal: igual que pedir_entero, pero acepta números con decimales.
# Parámetro: mensaje (str). Retorna: el número ingresado (float).
def pedir_decimal(mensaje):
    valor = 0.0
    valido = False

    while not valido:
        texto = input(mensaje)
        try:
            valor = float(texto)
            valido = True
        except ValueError:
            print("Error: ingrese un número (use punto para los decimales, ej: 2500.50).")

    return valor


# pedir_alta: pide los datos de un producto y lo da de alta.
def pedir_alta(matriz):
    print("--- Alta de producto ---")
    codigo = pedir_entero("Código (entero positivo): ")
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    precio = pedir_decimal("Precio unitario: ")
    stock = pedir_entero("Stock inicial: ")

    # alta_producto devuelve True o False, y el if usa ese valor directamente
    if alta_producto(matriz, codigo, nombre, categoria, precio, stock):
        print("Producto agregado correctamente.")
    else:
        print("No se pudo agregar: el código ya existe o algún dato es inválido.")
        print("(El código debe ser positivo; nombre y categoría no pueden estar")
        print(" vacíos ni tener comas; precio y stock no pueden ser negativos.)")


# pedir_baja: pide un código y elimina ese producto.
def pedir_baja(matriz):
    print("--- Baja de producto ---")
    codigo = pedir_entero("Código del producto a eliminar: ")

    if baja_producto(matriz, codigo):
        print("Producto eliminado.")
    else:
        print("No se pudo eliminar: no existe un producto con ese código.")


# pedir_modificar_stock: pide un código y una cantidad, y la suma al stock.
def pedir_modificar_stock(matriz):
    print("--- Modificar stock ---")
    codigo = pedir_entero("Código del producto: ")
    cantidad = pedir_entero("Cantidad a sumar (negativa para restar): ")

    if modificar_stock(matriz, codigo, cantidad):
        print("Stock actualizado correctamente.")
    else:
        print("No se pudo modificar: el producto no existe o el stock quedaría negativo.")


# pedir_busqueda: pide un código, lo busca con los dos métodos y muestra
# cuántas comparaciones hizo cada uno.
def pedir_busqueda(matriz):
    print("--- Buscar producto por código ---")
    codigo = pedir_entero("Código a buscar: ")

    # La búsqueda binaria necesita la matriz ordenada por código (columna 0),
    # así que primero la ordenamos. Las dos búsquedas se hacen sobre la misma
    # matriz ordenada, para que la comparación sea justa.
    ordenar_insercion(matriz, 0)

    indice_sec, comparaciones_sec = busqueda_secuencial(matriz, codigo)
    indice_bin, comparaciones_bin = busqueda_binaria(matriz, codigo)

    if indice_sec == -1:
        print("No existe un producto con el código", codigo)
    else:
        print("Producto encontrado:")
        mostrar_producto(matriz[indice_sec])

    print("Búsqueda secuencial:", comparaciones_sec, "comparaciones")
    print("Búsqueda binaria:", comparaciones_bin, "comparaciones")


# pedir_ordenamiento: el usuario elige el criterio (Nombre, Precio o Stock)
# y el método (selección o inserción); se ordena y se muestra el listado.
def pedir_ordenamiento(matriz):
    print("--- Ordenar inventario ---")
    print("Ordenar por: 1. Nombre   2. Precio   3. Stock")
    criterio = input("Criterio: ")
    print("Método: 1. Selección   2. Inserción")
    metodo = input("Método: ")

    # Traducimos el criterio al número de columna de la matriz.
    # Si no es válido, usamos -1 como marca de "criterio inválido".
    if criterio == "1":
        columna = 1  # nombre
    elif criterio == "2":
        columna = 3  # precio
    elif criterio == "3":
        columna = 4  # stock
    else:
        columna = -1

    if columna == -1:
        print("Criterio inválido: elija 1, 2 o 3.")
    elif metodo == "1":
        ordenar_seleccion(matriz, columna)
        mostrar_matriz(matriz)
    elif metodo == "2":
        ordenar_insercion(matriz, columna)
        mostrar_matriz(matriz)
    else:
        print("Método inválido: elija 1 o 2.")


# reporte_stock_bajo: pide un umbral y muestra los productos con stock menor.
def reporte_stock_bajo(matriz):
    print("--- Productos con stock bajo ---")
    umbral = pedir_entero("Mostrar productos con stock menor a: ")
    productos_bajos = stock_bajo(matriz, umbral)

    if len(productos_bajos) == 0:
        print("No hay productos con stock menor a", umbral)
    else:
        print("Productos con stock menor a", umbral, ":")
        mostrar_matriz(productos_bajos)


# reporte_valor_total: muestra la suma de precio × stock del inventario.
def reporte_valor_total(matriz):
    total = valor_total(matriz)
    # round(total, 2) redondea a 2 decimales
    print("Valor total del inventario: $", round(total, 2))


# reporte_extremos: muestra el producto más caro y el más barato.
def reporte_extremos(matriz):
    if len(matriz) == 0:
        print("El inventario está vacío.")
    else:
        print("Producto más caro:")
        mostrar_producto(producto_mas_caro(matriz))
        print("Producto más barato:")
        mostrar_producto(producto_mas_barato(matriz))


# menu_reportes: submenú de reportes; se repite hasta elegir 0 (volver).
def menu_reportes(matriz):
    opcion = ""

    while opcion != "0":
        print()
        print("----- REPORTES -----")
        print("1. Listado completo ordenado")
        print("2. Productos con stock bajo")
        print("3. Valor total del inventario")
        print("4. Producto más caro y más barato")
        print("0. Volver al menú principal")
        opcion = input("Elija una opción: ")

        if opcion == "1":
            pedir_ordenamiento(matriz)
        elif opcion == "2":
            reporte_stock_bajo(matriz)
        elif opcion == "3":
            reporte_valor_total(matriz)
        elif opcion == "4":
            reporte_extremos(matriz)
        elif opcion != "0":
            print("Opción inválida.")


# guardar_cambios: guarda la matriz en el archivo e informa el resultado.
# Parámetros: matriz, nombre_archivo (str)
def guardar_cambios(matriz, nombre_archivo):
    if guardar_csv(matriz, nombre_archivo):
        print("Cambios guardados en", nombre_archivo)
    else:
        print("Error: no se pudo guardar", nombre_archivo, "(¿está abierto en otro programa?)")


# ------------------------------------------------------------
# FUNCIONES AUXILIARES PARA MOSTRAR EN PANTALLA
# ------------------------------------------------------------

# mostrar_producto: muestra una fila (un producto) en una línea.
def mostrar_producto(fila):
    print(fila[0], "|", fila[1], "|", fila[2], "| $", fila[3], "|", fila[4])


# mostrar_matriz: muestra todos los productos de la matriz.
def mostrar_matriz(matriz):
    if len(matriz) == 0:
        print("No hay productos para mostrar.")
    else:
        print("Código | Nombre | Categoría | Precio | Stock")
        print("---------------------------------------------")
        for fila in matriz:
            mostrar_producto(fila)


# mostrar_menu: imprime las opciones del menú principal.
def mostrar_menu():
    print()
    print("===== SISTEMA DE GESTIÓN DE INVENTARIO =====")
    print("1. Mostrar inventario")
    print("2. Alta de producto")
    print("3. Baja de producto")
    print("4. Modificar stock")
    print("5. Buscar producto por código")
    print("6. Ordenar inventario")
    print("7. Reportes")
    print("8. Guardar cambios")
    print("0. Guardar y salir")


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

# main: carga el inventario y muestra el menú hasta que el usuario elija salir.
# Al salir, guarda el estado final en el CSV (como pide la consigna).
def main():
    nombre_archivo = "inventario.csv"
    matriz = cargar_csv(nombre_archivo)
    print("Se cargaron", len(matriz), "productos.")

    opcion = ""  # la inicializamos para que el while pueda evaluar la condición

    # while: repite el menú MIENTRAS la opción no sea "0"
    while opcion != "0":
        mostrar_menu()
        opcion = input("Elija una opción: ")

        # if / elif / else: se ejecuta SOLO la primera condición verdadera;
        # el else se ejecuta si ninguna lo fue.
        if opcion == "1":
            mostrar_matriz(matriz)
        elif opcion == "2":
            pedir_alta(matriz)
        elif opcion == "3":
            pedir_baja(matriz)
        elif opcion == "4":
            pedir_modificar_stock(matriz)
        elif opcion == "5":
            pedir_busqueda(matriz)
        elif opcion == "6":
            pedir_ordenamiento(matriz)
        elif opcion == "7":
            menu_reportes(matriz)
        elif opcion == "8":
            guardar_cambios(matriz, nombre_archivo)
        elif opcion == "0":
            guardar_cambios(matriz, nombre_archivo)
            print("Saliendo del sistema...")
        else:
            print("Opción inválida.")


main()
