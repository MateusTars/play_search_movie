import re
import sys
import string
import requests

# constants
CODE_REGIONS = [
    "ZA", "AR", "CZ", "DK", "AT", "CH", "DE", "GR", "GB", "US", "ES", "MX", "EE", "FI", "CA", "FR", "HR", "HU", "ID", "IS", "IT", "JP", 
    "KH", "KR", "LA", "LT", "LV", "NL", "NO", "NZ", "PL", "BR", "PT", "RO", "RU", "SK", "SI", "SE", "TH", "TR", "UA", "VN", "TW"
]

NAME_REGIONS = [
    "Afrikaans", "Argentina", "Czech", "Danish", "German (Austria)", "German (Switzerland)", "German (Germany)", "Greek",
    "English (UK)", "English (US)", "Spanish (Spain)", "Spanish (Mexico)", "Estonian", "Finnish", "French (Canada)", "French (France)",
    "Croatian", "Hungarian", "Indonesian", "Icelandic", "Italian", "Japanese", "Cambodja", "Korean", "Latin", "Lithuanian", "Latvian",
    "Nederlands", "Norwegian (Nynorsk)", "New Zealand", "Polish", "Português (Brasil)", "Português (Portugal)", "Romanian", "Russian", 
    "Slovak", "Slovenian", "Swedish", "Thai", "Turkish", "Ukrainian", "Vietnamese", "Chinese (Taiwan)"
]

class PlaySearchMovie(object):
    def __init__(self, name=""):
        self.name = name
        self.store = "https://play.google.com/store?hl=en&gl={0}"
        self.news = "https://play.google.com/store/movies/new?hl=en&gl={0}"
        self.movie = "https://play.google.com/store/movies/details/{0}&hl=en&gl={1}"
        self.session = requests.Session()
        self.session.headers.update({
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        })

    def print_help(self):
        print("Usage: python playsm.py [movie_name]")
        return 1

    def release_verify(self, rname, rcode):
        print("\nVerificando filme na região: {0} - {1}".format(rname, rcode))
        print("Região store: {0}".format(self.store.format(rcode)))
        resp = self.session.get(url=self.news.format(rcode))
        search_data = re.search(f'title="{self.name}([^^]*)', resp.text, re.IGNORECASE)
        if search_data:
            return True, search_data[1]
        else:
            return False, []

    def get_movie_and_info(self, data, rname, rcode):
        href_all = re.findall(r'href="/store/movies/details/(.+?)"', data, re.IGNORECASE)
        url = False
        for href in href_all:
            if self.is_similar(href.split('?id')[0], self.name) >= 0.8:
                url = self.movie.format(href, rcode)
                break
        if url:
            print("{0:><5}Parcialmente Encontrado{0:<<5}".format(''))
            print("O Filme: {0} foi encontrado na região: {1} - {2}".format(self.name, rname, rcode))
            resp = self.session.get(url=url)
            audios = self.is_available(resp.text, "audio language")
            subtitles = self.is_available(resp.text, "subtitles")
            return True, url, audios, subtitles
        else:
            return False, url, [], []

    def is_available(self, data, search):
        try:
            regex = re.search(f'"{search}"(.*?)"]', data, re.IGNORECASE)[0]
            split = regex.split(',"')[1][:-2]
            return split
        except:
            return "Não disponível"

    def is_similar(self, na, nb):
        counter = 0
        for l in string.ascii_lowercase:
            counter += abs(na.lower().count(l) - nb.lower().count(l))
        total = len(na) + len(nb)
        return (total - counter) / total

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(PlaySearchMovie().print_help())
    movie_name = sys.argv[1]
    print("Iniciando a busca pelo filme: {0}".format(movie_name))
    client = PlaySearchMovie(movie_name)
    array = []
    for rname, rcode in zip(NAME_REGIONS, CODE_REGIONS):
        success, data = client.release_verify(rname, rcode)
        if success:
            _success, movie_url, audios, subtitles = client.get_movie_and_info(data, rname, rcode)
            if _success:
                array.append({
                    "rcode": rcode, 
                    "rname": rname,
                    "url": movie_url, 
                    "audios": audios, 
                    "subtitles": subtitles
                })
    if len(array) > 0:
        print("\n{0:><5}Fim da busca{0:<<5}".format(''))
        print("O Filme: {0} foi encontrado em {1} das {2} regiões implementadas".format(movie_name, len(array), len(CODE_REGIONS)))
        for a in array:
            print("\nO Filme: {0} foi encontrado na região: {1} - {2}".format(movie_name, a["rname"], a["rcode"]))
            print("Filme url: {0}".format(a["url"]))
            print("Áudios disponíveis: {0}".format(a["audios"]))
            print("Legendas disponíveis: {0}".format(a["subtitles"]))
    else:
        print("\nFim da busca o Filme: {0} não foi encontrado em nenhuma das {1} regiões implementadas".format(movie_name, len(CODE_REGIONS)))

    sys.exit(0)
