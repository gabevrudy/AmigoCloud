from amigocloud import AmigoCloud

amigocloud = AmigoCloud(token='')
pOwner = 123

pNum = input('Enter Project Number: ')
dNum = input('Enter Dataset Number: ')
acID = input('Enter Amigo_ID you wish to restore: ') #See Record History for deletions if unsure

#Find hash
stateInfo = amigocloud.get('users/%s/projects/%s/datasets/%s/states' % (pOwner, pNum, dNum))
for item in stateInfo['states']:
    findHash = amigocloud.get('projects/%s/datasets/%s/changeset?hash=%s' % (pNum, dNum, item))
    result = findHash['changeset']
    if acID in str(result) and 'DELETE' in str(result):
        print('Your Changeset Link is the following: ' + 'https://app.amigocloud.com/api/v1/projects/%s/datasets/%s/changeset?hash=%s' % (pNum, dNum, item))
        break
