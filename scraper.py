import scraperwiki
import sys
import requests
import re
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding("utf-8")

def parse_club_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    team = soup.find_all('h1', class_='team')[0]
    team_name = team.get_text()
    players = soup.find_all('a', class_='playerOverviewCard')
    for player in players:
        name = player.find_all('h4', class_='name')[0].get_text()
        position = player.find_all('span', class_='position')[0].get_text()
        match =  re.search(r"/players/(.*)/.*/overview", player['href'])
        identifier = match.group(1)
        scraperwiki.sqlite.save(unique_keys=['id'], data={"id": identifier, "name": name, "position":position, "team":team_name})
        


# check the downloads page for the latest release (assumed to be the first download button we find)
page = requests.get("https://www.premierleague.com/clubs")
soup = BeautifulSoup(page.content, 'html.parser')

downloads = soup.find_all('a', class_='indexItem')
for download in downloads:
    url =  'https://www.premierleague.com'+download['href'].replace("overview","squad")

    parse_club_page(url)
