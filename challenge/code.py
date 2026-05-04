import requests
from bs4 import BeautifulSoup

url = 'https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub'
url2 = 'https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub'


def GetDataFromGoogleSheet(url: str) -> dict[(int, int), str]:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the page
        text = soup.get_text()

        data: dict[(int, int), str] = {}
        table = soup.find(lambda tag: tag.name == 'table')
        rows = table.findAll(lambda tag: tag.name == 'tr')
        for row in rows:
            columns = row.findAll(lambda tag: tag.name == 'td')
            if columns[0].text != 'x-coordinate':
                data[(int(columns[0].text), int(columns[2].text))] = columns[1].text

        return data
    else:
        print(f'Access error: {response.status_code}')


def PrintSecret(url: str):
    data = GetDataFromGoogleSheet(url)
    print(data)
    maxwidth = 0
    maxheight = 0
    for key in data:
        if key[0]+1 > maxwidth:
            maxwidth = key[0]+1
        if key[1]+1 > maxheight:
            maxheight = key[1]+1

    for height in range(maxheight):
        line = ''
        for width in range(maxwidth):
            if (width, maxheight - 1 - height) in data:
                line += data[(width, maxheight - 1 - height)]
            else:
                line += ' '
        print(line)


PrintSecret(url2)
