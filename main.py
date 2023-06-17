from pyzotero import zotero
import os
import shutil

MAIN_DIR = os.getcwd()
CREDENTIALS_PATH = MAIN_DIR + '/credentials.txt'

def copy_from_kindle():
    '''
    Copy 'My Clippings.txt' from Kindle to current directory
    '''
    try:
        os.chdir('/Volumes/Kindle/documents')
        shutil.copy('My Clippings.txt', MAIN_DIR)
    except:
        print('ERROR: Unable to access Kindle/documents/My Clippings.txt')
        exit(1)


# Get credentials for Zotero from credentials.txt
try:
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = f.readlines()
        LIBRARY_ID = credentials[0].split(':')[1].strip()
        LIBRARY_TYPE = credentials[1].split(':')[1].strip()   
        API_KEY = credentials[2].split(':')[1].strip()
except Exception as e:
    print(e)
    exit(1)


zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
items = zot.top(limit=30)

for item in items:
    print(item['data']['title'])
    item_id = item['data']['key']
    children = zot.children(item_id)
    for child in children:
        if (child['data']['itemType'] == 'note'):
            print(child['data']['note'])
    print()
            


