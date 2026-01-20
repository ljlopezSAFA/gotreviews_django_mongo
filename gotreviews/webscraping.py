import requests
import bs4
import csv

paginas = ['https://www.hermandades-de-sevilla.org/hermandades/penitencia/viernes-de-dolores/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/sabado-de-pasion/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/domingo-de-ramos/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/lunes-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/martes-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/miercoles-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/jueves-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/viernes-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/sabado-santo/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/domingo-resurreccion/',
           ]
dias = ['Viernes de Dolores', 'Sábado de Pasión', 'Domingo de Ramos',
        'Lunes Santo','Martes Santo','Miércoles Santo','Jueves Santo','Viernes Santo', 'Sábado Santo', 'Domingo de  Resurrección']

with open('hermandades.csv', 'w', newline='', encoding='utf8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(['Hermandad', 'Logo', 'Día'])

    for i in range (10):
        #OBTENGO EL HTML DE LA PÁGINA WEB
        html = requests.get(paginas[i])

        #CONVERTIR SOUP
        soup = bs4.BeautifulSoup(html.content, 'html.parser')

        #OBTENER DATOS

        elementos = soup.find_all('div', class_='elementor-image-box-wrapper')

        for elemento in elementos:
            title = elemento.find('h4', class_="elementor-image-box-title").text
            imagen = elemento.find('figure').find('img')["src"]
            dia = dias[i]

            print("Hermandad -> ", title, imagen,dia)

            spamwriter.writerow([title.strip(), imagen,dia])
