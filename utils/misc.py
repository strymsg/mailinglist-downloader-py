'''
mailisting-donwloader
copyright 2020 Rodrigo Garcia <rgarcia@laotra.red>
AGPL liberated.
'''
import requests
from bs4 import BeautifulSoup

import yaml
from  datetime import datetime as dt

def getHtml(url):
    ''' get the html content'''
    result = requests.get(url)
    if result.status_code != 200:
        return None
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

# def yearsToSearch(initialYear=2004, endYear=None):
#     ''' yields years from initial to current or to endYear if given'''
#     n = initialYear-1
#     while n < endYear:
#         n += 1
#         yield n

def getUrlsSectionIndexDebian(url, name, debug=False, initialYear=2004, endYear=None):
    ''' crawls the given `url' of the mailisting section and returns
    a dict with all urls related to archives of the given `name'
    { '2000' : [url1, ..., urln], '2001': [url1, ..., urln] }
    '''
    dict = {}
    htmlContent = getHtml(url)
    urls = getUrls(htmlContent)
    # checking year by year
    if endYear is None:
        endYear = dt.now().year
    for url in urls:
        validIndexes = []
        month = 0
        for year in range(initialYear, endYear):
            dict[year] = []
            for month in range(1, 13):
                if month < 10:
                    month = '0'+str(month)
                # to try an url that is like {year}/{name}-{year}{month}
                # slug:
                # 2009/debian-vote-200901/threads.html
                # url:
                # https://lists.debian.org/debian-cd/1998/debian-cd-199811/threads.html
                # 'https://lists.debian.orgdebian-admin//2016/debian-admin/-201601/threads.html'
                slug = str(year) + '/' + str(name) + '-' + str(year) + str(month)

                indexUrl = 'https://lists.debian.org/' + name + '/' + slug + '/threads.html'
                dict[year].append(indexUrl)
    return dict
                # html = getHtml(indexUrl)
                # if html is None:
                #     # can't find url that should mean there are no more emails
                #     if debug:
                #         print(indexUrl, 'Not found!')
                #     break
                
                    

                
                    
                

        
