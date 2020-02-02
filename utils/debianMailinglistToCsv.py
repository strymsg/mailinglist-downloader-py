#!/bin/python3
'''
This is a sample script to read messages downloaded and write the messages to a csv file.

This script should be called from projects root, then

python debianMailing
'''

import os
import csv

csvHeaders = ['category', 'year','month', 'message']
# lista = ['debian-cli', 'debian-desktop', 'debian-firewall', 'debian-jobs', 'debian-legal', 'debian-mirrors', 'debian-python', 'debian-r','debian-edu']

outputDirectory = os.path.join(os.path.abspath(os.getcwd()))
print('outputDir:', outputDirectory)
print(outputDirectory)
outputFile = os.path.join(outputDirectory, 'output', 'debian-mailinglist', 'debian-mailinglist.csv')

with open(outputFile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile,
                            fieldnames=csvHeaders,
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    # messageWriter = csv.writer(csvfile, delimiter=',',
    #                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for roots, dirs, files in os.walk(outputDirectory, topdown=True):
        print('---------------')
        print('roots:', roots)
        # input('ver dirs>')
        # for name in dirs:
        #     print(os.path.join(roots, name))
        # if (input('ver files>') == 'o'):
        #     break
        for name in files:
            filePath = os.path.join(roots, name)
            # getting features
            try:
                slug1 = filePath.split('/')
                category = slug1[1]
                # if category not in lista:
                #     continue
                print(filePath)
                slug2 = slug1[3].split(category + '_')
                year = slug2[1].split('_')[0]
                month = slug2[1].split('_')[1]
                # print('cateogory:', cateogory, 'year:', year, 'month:', month)
                # reading file contents
                message = ''
                with open(filePath) as fileMessage:
                    message = fileMessage.read()
                
                writer.writerow({
                    'category': category,
                    'year': year,
                    'month': month,
                    'message': message
                })
            except Exception as E:
                print(E)
print('Done, check output/debian-mailinglist/debian-mailinglist.csv')

        