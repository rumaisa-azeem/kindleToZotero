from pyzotero import zotero
import os
import shutil
import pprint
import re

MAIN_DIR = os.getcwd()
USER_FILE = MAIN_DIR + '/user.txt'


def copy_clippings_from_kindle():
    '''
    Copy 'My Clippings.txt' from Kindle to current directory
    '''
    try:
        os.chdir('/Volumes/Kindle/documents')
        shutil.copy('My Clippings.txt', MAIN_DIR)
    except:
        print('ERROR: Unable to access Kindle/documents/My Clippings.txt')
        exit(1)


def get_credentials() -> tuple:
    '''
    Get credentials for Zotero API from user.txt
    @return: LIBRARY_ID, LIBRARY_TYPE, API_KEY
    '''
    try:
        with open(USER_FILE, 'r') as f:
            credentials = f.readlines()
            LIBRARY_ID = credentials[1].split(':')[1].strip()
            LIBRARY_TYPE = credentials[2].split(':')[1].strip()   
            API_KEY = credentials[3].split(':')[1].strip()
            return LIBRARY_ID, LIBRARY_TYPE, API_KEY
    except Exception as e:
        print(e)
        exit(1)


def get_book_titles() -> list:
    '''
    Get names of books to be added to Zotero
    @return: book_titles list
    '''
    book_titles = []
    try:
        with open(USER_FILE, 'r') as f:
            books = f.readlines()
            for i in range(5,len(books)):
                book_titles.append(books[i].strip())
        return book_titles
    except Exception as e:
        print(e)
        exit(1)


def import_clippings() -> list:
    '''
    Get clippings from 'My Clippings.txt'
    @return: clippings list
    '''
    # copy_clippings_from_kindle()
    CLIPPINGS_FILE = MAIN_DIR + '/My Clippings.txt'
    with open(CLIPPINGS_FILE, 'r') as f:
        clippings = f.readlines()
        clippings = "".join(clippings).split('==========')
    return clippings


def get_clippings_for_book(book_title: str, clippings: list) -> list:
    '''
    Get clippings for a specific book
    @param: book_title title of book to get clippings for
    @param: clippings list of all clippings
    @return list of clippings for specified book
    '''
    clippings_for_book = []
    regex = r"Your Highlight .*:..:.."
    for clipping in clippings:
        clipping = re.split(regex, clipping)
        if book_title.lower() in clipping[0].lower():
            clippings_for_book.append(clipping[1].replace('\n', ''))
    return clippings_for_book


book_titles = get_book_titles() 
all_clippings = import_clippings() 
creds = get_credentials()
zot = zotero.Zotero(creds[0], creds[1], creds[2])

# pprint.pprint(zot.item_template('book'), width=1)

for book in book_titles:
    clippings = get_clippings_for_book(book, all_clippings)
    for c in clippings:
        print('\n'+ c)
    # template = zot.item_template('book')
    


# items = zot.top(limit=30)
# for item in items:
#     print(item['data']['title'])
#     item_id = item['data']['key']
#     children = zot.children(item_id)
#     for child in children:
#         if (child['data']['itemType'] == 'note'):
#             print(child['data']['note'])
#     print()


