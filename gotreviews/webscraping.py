
import requests
import bs4
import csv



paginas = ['https://www.hermandades-de-sevilla.org/hermandades/penitencia/viernes-de-dolores/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/sabado-de-pasion/',
           'https://www.hermandades-de-sevilla.org/hermandades/penitencia/domingo-de-ramos/']

with open('hermandades.csv', 'w', newline='', encoding='utf8') as csvfile:
   spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

   for page in paginas:
      #OBTENGO EL HTML DE LA PÁGINA WEB
      html = requests.get(page)


      #CONVERTIR SOUP
      soup = bs4.BeautifulSoup(html.content, 'html.parser')


      #OBTENER DATOS

      elementos = soup.find_all('div', class_='elementor-image-box-wrapper')




      for elemento in elementos:
         title = elemento.find('h4', class_="elementor-image-box-title").text
         imagen = elemento.find('figure').find('img')["src"]

         print("Hermandad -> ",title, imagen)

         spamwriter.writerow([title.strip(),imagen])







