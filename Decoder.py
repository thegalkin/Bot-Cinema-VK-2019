from bs4 import BeautifulSoup as BF
import re
import requests as req

todayKARO_raw = open("Today_Parser_KARO_raw.txt", 'r')
todayKARO = open("Today_Parser_KARO.txt", 'w')

soup = BF(todayKARO_raw, "html.parser")
theatres = soup.findAll('li', {'class' : 'cinemalist__cinema-item'})


def remove_all(string):
    pattern = re.compile(r'[А-Яа-яёЁ0-9 ]+')
    return pattern.findall(string)[0].strip()
def removerForFormat(string):
    pattern = re.compile(r"[\S]")
    return ''.join(pattern.findall(string))
def findAllTheatres(theatres):
    dataIds = []
    theatresDicti = {}
    for theater in theatres:
        dataIds.append(theater['data-id'])
        theatresDicti[theater.findAll('h4')[0].text] = {
            'metro': [remove_all(i.text) for i in theater.findAll('li', {"class" : "cinemalist__cinema-item__metro__station-list__station-item"})],
            'address': theater.findAll('p')[0].text.split('+')[0].strip(),
            'phone': '+' + theater.findAll('p')[0].text.split('+')[-1],
            'data-id': theater['data-id']
        }
    return theatresDicti
theatresDicti = findAllTheatres(theatres)
#print(theatresDicti)
def inCinema(key):
    filmsDicti = {}
    cinemaUrl = "https://karofilm.ru/theatres?id=" + str(key) #заменить на key
    soup = BF(req.get(cinemaUrl).text, "html.parser")
    #films = soup.findAll("div", {"class" : "cinema-page-item__schedule__row__data"})
    films = soup.findAll('div', class_='cinema-page-item__schedule__row__board-row')
    #print(films)
    for film in films:
        print(film)
        #print(removerForFormat(film.findAll("div", {"class" : "cinema-page-item__schedule__row__board-row__left"})[0].text))
        #print(film.findAll('div', class_ = 'cinema-page-item__schedule__row__board-row__right')[0].findAll('a')[0].text)
        #tempFilm = film.findAll(('div', {'class' : 'cinema-page-item__schedule__row__board-row__right'})[0])
        #print(tempFilm.findAll('a'))
        notWorkingShit = film.findAll('div', class_ = 'cinema-page-item__schedule__row__board-row__right')[0].findAll('a')[0].text
        filmsDicti[films.findAll("div", {"class" : "cinema-page-item__schedule__row__title"})[0].findAll('h3')[0].text] = {
            #'f': 'to f'
            #removerForFormat(film.findAll("div", class_= "cinema-page-item__schedule__row__board-row__left")[0].text) : "жопа"
            #: [notWorkingShit[i] for i in range(len(notWorkingShit))]
        }
    print(filmsDicti)
    return(filmsDicti)



for key in theatresDicti:
    filmsDicti = inCinema(key)

#cinemaShedule = inCinema(key)
#for key in theatresDicti.keys():
 #   cinemaShedule = inCinema(key)


#print(findAllTheatres(theatres))