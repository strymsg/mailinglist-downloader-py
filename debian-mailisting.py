# Download debian mailing list emails

import utils

configParams = utils.misc.readYaml('debian-mailisting.yaml')

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
mailistingNames = ['debian-admin/', 'debian-cli/', 'debian-desktop/', 'debian-devel/', 'debian-gcc/', 'debian-kernel/', 'debian-legal/', 'debian-mirrors/', 'debian-news/', 'debian-vote/']

allUrls = []
for name in mailistingNames:
    print('Crawling','https://lists.debian.org/'+ name)
    indexes = utils.misc.getUrlsFromSectionIndexDebian('https://lists.debian.org/'+ name, name[:-1])
    # print(indexes)
    for index in indexes:
        newUrls = utils.misc.getUrlsMessagesFromThreadDebian(index)
        print('newUrls---')
        print(newUrls)
        print()
        allUrls.append(newUrls)
