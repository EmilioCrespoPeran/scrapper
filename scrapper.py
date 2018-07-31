import urllib
import re
import time
import sys

# Define las caracteristicas de un libro
class Book:
    def __init__ (self, title, author, price, rating):
        self.title = title
        self.author = author
        self.price = price
        self.rating = rating

    def get_title (self):
        return self.title

    def get_author (self):
        return self.author

    def get_price (self):
        return self.price

    def get_rating (self):
        return self.rating



# Devuelve el contenido de la pagina
def get_page (url):
    reader = urllib.urlopen(url)
    return reader.read()



# Devuelve los libros del listado
def get_books (url, max_books):
    # Recoge las url de los libros
    links = get_books_link(url, max_books)

    books = []
    time_waiting = 2

    # Muestra el progreso
    print '\r>> Progress...%d%%' % ( 0 ),
    sys.stdout.flush()

    for x in range(0, max_books):
        # Duerme al scrapper n segundos
        time.sleep(time_waiting)

        # Recoge el contenido de la pagina del libro
        page_details = get_page(url + links[x])

        # Recoge los detalles del libro
        title, author, price, rating = get_book_details(page_details)

        # Agrega el libro al listado
        books.append(Book(title, author, price, rating))

        # Muestra el progreso
        print '\r>> Progress...%d%%' % ( ((x + 1) * 100) / max_books ),
        sys.stdout.flush()

    # Devuelve los libros
    return books



# Devuelve las url de los libros
def get_books_link (url, max_books):
    # Recoge el contenido de la pagina
    page = get_page(url)

    # Define el patron regular para recoger las url de los libros
    item = '<div class="carousel-info">'
    regex = item + '.*?' + '<a href="(.*?)" class="title-link"'

    # Devuelve el resultado
    return re.findall(regex, page, re.DOTALL)[:max_books]



# Devuelve los detalles de un libro
def get_book_details(page):
    # Expresiones regulares de cada campo
    item = 'class="book-header-2"'
    reg_title = '<h1[^>]*?>(.*?)</h1>'
    reg_author = '<h2[^>]*?>[^<]*?(?:<a[^>]*?>(.*?)</a>|<span[^>]*?>(.*?)</span>)'
    reg_rating = '<span class="average-rating star0(\d)"></span>'
    reg_price = '<p class="currentPrice">(.*?)</p>'

    # Expresion regular final
    regex = item + '.*?' + reg_title + '.*?' + reg_author + '.*?(?:' + reg_rating + '.*?' + reg_price + '|' + reg_price + ')'

    # Recoge los campos extraidos en un array
    details = re.findall(regex, page, re.DOTALL)[0]

    # Recoge el campo titulo
    title = details[0]

    # Recoge el campo autor, dos posibles indices
    if details[1] != '':
        author = details[1]
    else:
        author = details[2]

    # Si existe el campo puntuacion, recoge la puntuacion y precio,
    # en caso contrario, agrega '0' a la puntuacion y recoge el precio
    if details [3] != '':
        rating = details[3]
        price = details[4]
    else:
        rating = '0'
        price = details[5]

    # Devuelve los campos
    return title, author, price, rating



# Escribe los resultados en un fichero html
def write_results (books):
    # Abre el fichero html para escribir
    file = open('listado_libros.html', 'w')

    # Escribe los resultados en el fichero
    file.write("<html>")
    file.write("<head>")
    file.write("<title>Scrapper libros</title>")
    file.write("<link rel='stylesheet' href='https://www.w3schools.com/w3css/4/w3.css'>")
    file.write("</head>")
    file.write("<body>")
    file.write("<h2>Lista de libros</h2>")
    file.write("<table class='w3-table w3-bordered w3-striped w3-border test w3-hoverable'>")
    file.write("<tr class='w3-green'><th>Titulo</th><th>Autor</th><th>Precio</th><th>Puntuacion</th></tr>")

    # Escribe las filas de los resultados
    for book in books:
        col_title = book.get_title()
        col_author = book.get_author()
        col_price = book.get_price()
        col_rating = book.get_rating()
        file.write("<tr><td>" + col_title + "</td><td>" + col_author + "</td><td>" + col_price + "</td><td>" + col_rating + "</td></tr>")

    file.write("</table>")
    file.write("</body>")
    file.write("</html>")

    # Cierra el fichero
    file.close()




################################
# Comienza el scrapping
################################

# Variables iniciales
url = "hello world!"
num_books = 7

# Variable para guardar los resultados
items = get_books(url, num_books)

# Escribe los resultados
write_results(items)

# Muestra un mensaje en consola
print '\r>> Progress complete!'
