'''
mailisting-donwloader
copyright 2020 Rodrigo Garcia <rgarcia@laotra.red>
GPLv3 liberated.
'''
import requests
from bs4 import BeautifulSoup

import yaml
from  datetime import datetime as dt

import re
import os

def readYaml(filepath):
    ''' reads yaml file and returs dict'''
    with open(filepath) as file:
        dc = yaml.load(file, Loader=yaml.FullLoader)
        return dc

def getHtml(url):
    ''' get the html content'''
    result = requests.get(url)
    try:
        if result.status_code != 200:
            return None
        return result.content
    except Exception as e:
        print(e)
        return None

def getUrls(htmlContent):
    ''' reads `htmlContent' and get all valid URLS '''
    soup = BeautifulSoup(htmlContent, features='html.parser')
    samples = soup.find_all("a")
    urls = []
    for a in samples:
        urls.append(a.attrs['href'])
    return urls

def getUrlsFromSectionIndexDebian(url, name, debug=False, initialYear=2004, endYear=None):
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


def prefixMessageUrlDebian(threadUrl):
    ''' The debian server redirects like this:
    - Thread url: https://lists.debian.org/debian-devel/2004/debian-devel-200406/threads.html
    - redirect:   https://lists.debian.org/debian-devel/2004/06/threads.html

    This function mimics the redirect and returns the string
    https://lists.debian.org/debian-devel/2004/06/
    '''
    # example: https://lists.debian.org/debian-devel/2004/debian-devel-200406/threads.html
    p1 = threadUrl.split('/')[-2] # getting the debian-devel-200406 part
    name = ''
    for c in p1.split('-')[0:-1]:
        name += c + '-'
    name = name[0:-1] # getting rid of last '-'
    
    regex = '(?P<year>20[0-9][0-9])(?P<month>[0-9][0-9])'
    m = re.search(regex, p1.split('-')[-1])
    year = m.group('year')
    month = m.group('month')

    # example: https://lists.debian.org/debian-devel/2004/06/
    prefix = 'https://lists.debian.org/' + name + '/' + year + '/' + month + '/'
    return prefix

def getUrlsMessagesFromThreadDebian(threadUrl):
    ''' crawls the give `threadUrl' and returns a list of all urls found. 
    It tries to open pagination thread indexes.
    
    - threadUrl (example): https://lists.debian.org/debian-devel/2004/debian-devel-200406/threads.html
    '''
    urls = []

    '''
    first trying to find exsiting index page indexes, starting the first
    page "threads.html" and then "thrd2.html" to "thrd{n}.html" until it fails
    '''
    pageNotFound = False
    page = 2
    pageIndexes = []
    pageIndexes.append(threadUrl)

    # Debian server redirects Index page of the section to a url like https://lists.debian.org/{name}/{year}/{month}/threads.html and the same for next pages
    prefix = prefixMessageUrlDebian(threadUrl)

    while not pageNotFound:
        threadIndexUrl = prefix + 'thrd' + str(page) + '.html'
        # print('trying:', threadIndexUrl)
        try:
            resp = requests.get(threadIndexUrl)
            if resp.status_code != 200:
                pageNotFound = True
            else:
                pageIndexes.append(threadIndexUrl)
        except Exception as E:
            pageNotFound = True
        page += 1
    # once having all valid index pages, crawls on them and gets the message urls
    for pageUrl in pageIndexes:
        html = getHtml(pageUrl)
        if html is None:
            # can't find url that should mean there are no email messages
            print(pageUrl, 'Not found!')
            continue

        pageUrls = getUrls(html)
        # to get actual email message url it should have the form:
        # {prefix}msg{number}.html
        # where prefix has the form: https://lists.debian.org/{name}/{year}/{month}/
        # number format is five digit zero formated, for instasnce: msg00005.html
        # regex to validate the url like: https://lists.debian.org/debian-cd/1999/01/msg00138.html
        regex = '^(' + prefix + ')(msg[0-9][0-9][0-9][0-9][0-9].html)$'
        for page in pageUrls:
            url = prefix + page
            # print('trying:', url)
            if re.search(regex, url) is not None:
                urls.append(url)
    return urls

def getMessageText(url='', html=None):
    '''crawls the url or the html (if given) and gets the message.
    Returns a dict of the form:
    { 'text': 'Text message', type: 'html|plain' }
    '''
    htmlContent = ''
    if html is not None:
        htmlContent = html
    else:
        htmlContent = getHtml(url)
    if htmlContent is not None:
        soup = BeautifulSoup(htmlContent, features='html.parser')
        p = soup.find_all('pre')

        try:
            return {
                'text': p[0].contents[0],
                'type': 'plain'
            }
        except Exception as e:
            pass
            # This may be the case of an html formated email.

        try:
            b = str(htmlContent).split('<!--X-Body-of-Message-->')
            return {
                'text': b[1].split('<!--X-Body-of-Message-End-->')[0],
                'type': 'html'
            }
            return 
        except Exception as e:
            print('✖ [',os.path.abspath(__file__),'] - url:', url)
            print(e)
            return { 'text': '', 'type': '' }
    else:
        return None

def crawlMessageAndWriteFromUrls(urls, directory, name=None, year=None):
    ''' loops on `urls' give, crawling and getting the message text of the
    containing html page. The email message got is written to a file in 
    `directory' given.
    optionals:
    -param year: to write the file on directory/name/year, or writes to directory/year if no `name' is given
    -param name: to write the file on directory name/year,  or writes to directory/name if no `year' is given
    Returns filename of written files.
    '''
    written = []
    pathToWrite = directory
    if year is not None and name is None:
        pathToWrite = os.path.join(directory, year)
    if name is not None and year is None:
        pathToWrite = os.path.join(directory, name)
    if name is not None and year is not None:
        pathToWrite = os.path.join(directory, name, year)
    # checking directory    
    try:
        if not os.path.exists(pathToWrite):
            os.makedirs(pathToWrite)
            print('created directory:', directory)
    except FileExistsError:
        print('Directory:', pathToWrite, 'already exists.')

    for url in urls:
        slug1 = url.split('https://lists.debian.org/')[-1]
        fileContent = getMessageText(url)
        fileName = slug1.replace('/', '_') + '.txt'
        if fileContent['type'] == 'plain':
            fileName = fileName.replace('.html.', '.')
        try:
            file = open(os.path.join(pathToWrite, fileName), 'w')
            file.write(fileContent['text'])
            file.close()
            print('✓', os.path.join(pathToWrite, fileName), 'written')
            written.append(os.path.join(pathToWrite, fileName))
        except Exception as e:
            print('✖ file:', e)
    return written
