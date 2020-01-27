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
# for url in allUrls:
#     # getting only mailisting urls
    
#     # TODO: add startswith(prefix) based on the types of mailisting on https://lists.debian.org/ for now it is just a hard-coded prefix list
#     if ((url.startswith('debian-') \
#         or url.startswith('cdwrite') \
#         or url.startswith('debconf-') \
#         or url.startswith('deity-') \
#         or url.startswith('gopher-project-') \
#         or url.startswith('lcs-eng') \
#         or url.startswith('lbs-') \
#         or url.startswith('nbd') \
#         or url.startswith('package-sponsorship-requests') \
#         or url.startswith('sart') \
#         or url.startswith('spi-') \
#         or url.startswith('vgui-discuss')) \
#         or url.startswith('whitelist')) and url.endswith('/'):
#         if configParams['download_all'] == False:
#             # only listed url in config file
#             section = url.split('/')[0]
#             if section in configParams['section_download']:
#                 mailistingNames.append(url)
#         else:
#             mailistingNames.append(url)
# print(mailistingNames)
#mailistingNames = ['debian-cli/', 'debian-desktop/', 'debian-devel/', 'debian-gcc/', 'debian-kernel/', 'debian-legal/', 'debian-mirrors/', 'debian-news/', 'debian-vote/']
mailistingNames = ['debian-cli/']

allUrls = []
print('*** Getting urls ***')
for name in mailistingNames:
    print('Crawling','https://lists.debian.org/'+ name)
    indexes = utils.misc.getUrlsFromSectionIndexDebian('https://lists.debian.org/'+ name, name[:-1])
    # print('****************')
    # print(indexes)
    for year, indexPage in indexes.items():
        print('Year: ', year)
        for page in indexPage:
            print('"'+page+ '"')
            newUrls = utils.misc.getUrlsMessagesFromThreadDebian(page)
            print('urls:', len(newUrls))
            print()
            allUrls += newUrls
# for testing
# allUrls = ['https://lists.debian.org/debian-cli/2018/04/msg00000.html', 'https://lists.debian.org/debian-cli/2018/12/msg00000.html', 'https://lists.debian.org/debian-cli/2018/12/msg00001.html', 'https://lists.debian.org/debian-cli/2018/12/msg00002.html', 'https://lists.debian.org/debian-cli/2018/12/msg00003.html', 'https://lists.debian.org/debian-cli/2018/12/msg00004.html']
                
print('Total of:', str(len(allUrls)))
print(allUrls)
print('*********************')
print('**** downloading ****')

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

# writes a file for every
for url in allUrls:
    slug1 = url.split('https://lists.debian.org/')[-1]
    fileName = slug1.replace('/', '_') + '.txt'
    fileContent = utils.misc.getMessageText(url)
    # creating and writing to file
    try:
        file = open(os.path.join(directory, fileName), 'w')
        file.write(fileContent)
        file.close()
        print('file:', os.path.join(directory, fileName), 'written')
    except Exception as e:
        print('Error writing file:', e)
