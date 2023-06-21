# kindleToZotero
A python program to send Kindle highlights to Zotero along with book metadata 

### 1) Set up Zotero API

**To use with personal library:**
1. Go to https://www.zotero.org/settings/keys - copy the number after 'Your userID for API calls is' and paste after `LIBRARY ID:` in `user.txt`
2. Now go to https://www.zotero.org/settings/keys/new - give the key any description (e.g. kindleToZotero) and tick to allow library, notes, and write access.
3. Click 'save key' and then copy the key that is displayed. Paste this after `API KEY:` in `user.txt`
4. Write `user` after `LIBRARY TYPE:` in `user.txt`
5. save `user.txt`

**To use with group library:**
1. Follow steps 2 and 3 from the instructions for personal library use above
2. Open your group library online - the URL should be something like https://www.zotero.org/groups/<some_number>/<group_name>/library
3. Copy <some_number> from the URL and paste after `LIBRARY ID:` in `user.txt`
4. Write `group` after `LIBRARY TYPE:` in `user.txt`
5. save `user.txt`

### 2) Running the program
1. Plug in Kindle
2. Open terminal in root directory of package and run the following commands:
   ```
   pip install -r requirements.txt
   python main.py
   ```

---
### to do
- [ ] don't add repeat books/notes
- [ ] add metadata from books
