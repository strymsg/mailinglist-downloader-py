'''
mailisting-donwloader
copyright 2020 Rodrigo Garcia <rgarcia@laotra.red>
AGPL liberated.
'''
import requests
from bs4 import BeautifulSoup

import yaml

def getHtml(url):
    ''' get the html content'''
    result = requests.get(url)
    return result.content

def readYaml(filepath):
    ''' reads yaml file and returs dict'''
    with open(filepath) as file:
        dc = yaml.load(file, Loader=yaml.FullLoader)
        return dc

def getUrls(htmlContent):
    ''' reads `htmlContent' and get all valid URLS '''
    soup = BeautifulSoup(htmlContent, features='html.parser')
    samples = soup.find_all("a")
    urls = []
    for a in samples:
        urls.append(a.attrs['href'])
    return urls

def getUrlsSectionIndexDebian(url):
    ''' crawls the given `url' of the mailisting section and returns
    a dict with all urls related to archives
    { '2000' : url, '2001': url }
    '''
    dict = {}
    htmlContent = getHtml(url)
    urls = getUrls(htmlContent)
    print(urls)

    
