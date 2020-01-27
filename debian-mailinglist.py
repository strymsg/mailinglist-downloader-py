'''
mailisting-donwloader
copyright 2020 Rodrigo Garcia <rgarcia@laotra.red>
GPLv3 liberated.
'''
# Download debian mailing list emails

import utils
import os

configParams = utils.misc.readYaml('debian-mailinglist.yaml')

htmlContent = utils.misc.getHtml(configParams['index_url'])
allUrls = utils.misc.getUrls(htmlContent)

mailistingNames = []
# filtering
for url in allUrls:
    # getting only mailisting urls
    
    # TODO: add startswith(prefix) based on the types of mailisting on https://lists.debian.org/ for now it is just a hard-coded prefix list
    if ((url.startswith('debian-') \
        or url.startswith('cdwrite') \
        or url.startswith('debconf-') \
        or url.startswith('deity-') \
        or url.startswith('gopher-project-') \
        or url.startswith('lcs-eng') \
        or url.startswith('lbs-') \
        or url.startswith('nbd') \
        or url.startswith('package-sponsorship-requests') \
        or url.startswith('sart') \
        or url.startswith('spi-') \
        or url.startswith('vgui-discuss')) \
        or url.startswith('whitelist')) and url.endswith('/'):
        if configParams['download_all'] == False:
            # only listed url in config file
            section = url.split('/')[0]
            if section in configParams['section_download']:
                mailistingNames.append(url)
        else:
            mailistingNames.append(url)
print(mailistingNames)

# creating directory to store files
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'debian-mailinglist')
try:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('created directory:', directory)
    else:
        print('Direcotry:', directory, 'already exists.')
except FileExistsError:
    print('Direcotry:', directory, 'already exists.')

allUrls = []
writtenFiles = []

print('*** Getting urls ***')
for name in mailistingNames:
    print('Crawling','https://lists.debian.org/'+ name)
    indexes = utils.misc.getUrlsFromSectionIndexDebian('https://lists.debian.org/'+ name, name[:-1])
    years = configParams.get('years', None)
    # print('****************')
    # print(indexes)
    for year, indexPage in indexes.items():
        if year is not None:
            if year not in years:
                print('year:', year, 'ignored')
                continue
        print('Year: ', year)
        for page in indexPage:
            print('"'+page+ '"')
            newUrls = utils.misc.getUrlsMessagesFromThreadDebian(page)
            print('crawling', str(len(newUrls)) + ' url(s)')
            allUrls += newUrls
            written = utils.misc.crawlMessageAndWriteFromUrls(newUrls, directory)
            writtenFiles += written

print('**********************************')                
print('Total of:', str(len(allUrls)), 'urls found')
print('Total of:', str(len(writtenFiles)), 'files written')
