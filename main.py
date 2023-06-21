from pyzotero import zotero
import os
import shutil
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
        print('Getting book titles...')
        with open(USER_FILE, 'r') as f:
            books = f.readlines()
            for i in range(6,len(books)):
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
    print('Importing clippings from Kindle...')
    # copy_clippings_from_kindle()
    CLIPPINGS_FILE = MAIN_DIR + '/My Clippings.txt'
    with open(CLIPPINGS_FILE, 'r') as f:
        clippings = f.readlines()
        clippings = "".join(clippings).split('==========')
    return clippings


def get_clippings_for_book(book_title: str) -> list:
    '''
    Get clippings for a specific book
    @param: book_title title of book to get clippings for
    @param: clippings list of all clippings
    @return list of clippings for specified book
    '''
    clippings_for_book = []
    regex = r"Your Highlight .*:..:.."
    for clipping in all_clippings:
        clipping = re.split(regex, clipping)
        if book_title.lower() in clipping[0].lower():
            clippings_for_book.append(clipping[1].replace('\n', ''))
    return clippings_for_book


def get_author_for_book(book_title:str) -> list:
    '''
    Get author for a specific book
    @param: book_title title of book to get author for
    @param: clippings list of all clippings
    @return author for specified book
    '''
    
    for clipping in all_clippings:
        clipping_title = re.split(r"- Your Highlight .*:..:..", clipping)[0] # split into title/author and clipping
        if book_title.lower() in clipping_title.lower(): # if title matches
            s = re.findall(r'\(.*\)', clipping_title)[0] # find author
            s = re.sub(r"[\(\)]", "", s)
            if len(s.split(', ')) == 2:
                s = s.split(', ')
                s.reverse()
                return s
            else:
                return s.split(' ')
            
def add_book(book_title: str):
    b = zot.item_template('book')
    b['title'] = book_title    
    b['creators'][0]['firstName'], b['creators'][0]['lastName'] = get_author_for_book(book_title)
    try:
        resp = zot.create_items([b])
        return resp['success']['0']
    except Exception as e:
        print('Error: ' + e)
        

book_titles = get_book_titles() 
all_clippings = import_clippings() 
creds = get_credentials()
zot = zotero.Zotero(creds[0], creds[1], creds[2])
t2 = zot.item_template('note')


for book_title in book_titles:
    print('Adding ' + book_title + ' to Zotero...')
    
    book_id = add_book(book_title)
    
    notes = []
    for clipping in get_clippings_for_book(book_title):
        n = zot.item_template('note')
        n['note'] = clipping
        notes.append(n)
    try:
        zot.create_items(notes, parentid=book_id)
    except Exception as e:
        print('Error: ' + e.__str__())

print('Done')
'''
to do:
- add date accessed using earliest date from clippings
- get proper title from clippings instead of using book_title
'''