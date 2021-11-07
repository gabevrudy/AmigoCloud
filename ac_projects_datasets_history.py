#Script to pull all Project IDs, Project Names, Dataset IDs, and Dataset Names
# Must have AmigoCloud Account w/ API access
# CREATED ON 5/14/2019

from amigocloud import AmigoCloud
import xlsxwriter
import pandas as pd

amigocloud = AmigoCloud(token='getTokenFromAmigoCloud')
projectOwner = 123 # changes based on project creator
projectCtID = []
projectCtName = []

datasetCtID = []
datasetCtName = []
recHistoryID = []

# project variables used to parse through all projects the user has
projects = amigocloud.get('users/%s/projects/' % (projectOwner))
projectsNext = projects['next']

# project list is offset by 20.  While loop is setup so if user has more than 20 projects it will grab the next set

while True:
    
   for x in projects['results']: # parse through projects
       projID = x['id'] # current Project ID in loop
       projName = x['name'] # current Project Name in loop
       projectCtID.append(x['id']) # list for export
       projectCtName.append(x['name']) # list for export
       projectDateCreation = x['created_on']
       projectsNext = projects['next']

       #parse through datasets
       datasets = amigocloud.get('users/%s/projects/%s/datasets' % (projectOwner,projID))

       for y in datasets['results']:
           dataID = y['id']
           dataName = y['name']
           datasetCtID.append(y['id']) # list for export
           datasetCtName.append(y['name']) # list for export

           if y['name'] == 'record_history':
               recHistoryID.append(y['id'])

       #print ('Currently looking at ' + str(projName))
   if projectsNext is None:
       break

   projects = amigocloud.get(projectsNext)

#setup workbook

excelFile = 'C:/path/to/file.xlsx'
workbook = xlsxwriter.Workbook(excelFile)

#write projects

worksheet1 = workbook.add_worksheet('Projects')
worksheet1.write('A1', 'Project ID')
worksheet1.write_column('A2', projectCtID)
worksheet1.write('B1', 'Project Name')
worksheet1.write_column('B2', projectCtName)

worksheet2 = workbook.add_worksheet('Datasets')
worksheet2.write('A1', 'Dataset ID')
worksheet2.write_column('A2', datasetCtID)
worksheet2.write('B1', 'Dataset Name')
worksheet2.write_column('B2', datasetCtName)

worksheet3 = workbook.add_worksheet('Records')
worksheet3.write('A1', 'Record History')
worksheet3.write_column('A2', recHistoryID)
worksheet3.write('B1', 'Project Number')
worksheet3.write_column('B2', projectCtName)

workbook.close()
