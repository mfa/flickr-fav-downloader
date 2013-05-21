import flickrapi
from credentials import KEY, SECRET, STORAGE, USERID
import shelve
import os
import requests
from docopt import docopt

def get_shelf(filename='fav.shelf'):
    return shelve.open(os.path.join(STORAGE, filename))

def init_api():
    return flickrapi.FlickrAPI(KEY, SECRET)

def update_database(user_id=USERID):
    """ update favs from specified user via flickr api and save data in shelf
    """
    shelf = get_shelf()
    flickr = init_api()
    # get list of favorites
    a = flickr.favorites_getList(user_id=user_id)
    # and extract max_page and total (total atm unused)
    max_page = int(a[0].attrib.get('pages'))
    total = a[0].attrib.get('total')
    # iterate over all pages
    for page in range(1,max_page):
        # get photos on page
        photos = flickr.favorites_getList(user_id=user_id, page=page)[0]
        for photo in photos:
            d = {}
            # get id of image / used as key for shelf
            id = photo.attrib.get('id')
            if id not in shelf:
                d['date_faved'] = photo.attrib.get('date_faved')
                d['owner'] = photo.attrib.get('owner')
                # get original sized image data via api
                sizes = flickr.photos_getSizes(photo_id=id)[0]
                print("%s" % id)
                best = None
                best_height=0
                for size in sizes:
                    if int(size.attrib.get('height')) > best_height:
                        best = size
                        best_height = int(size.attrib.get('height'))
                if best is not None:
                    # hopefully mostly this is downloading "Original"
                    d['label'] = best.attrib.get('label')
                    d['url'] = best.attrib.get('url')
                    d['width'] = best.attrib.get('width')
                    d['height'] = best.attrib.get('height')
                    d['source'] = best.attrib.get('source')
                    # safe dict in shelf
                    shelf[id] = d
                    print("added to shelf: %s" % id)
            else:
                print("already in shelf: %s" % id)
    shelf.close()

def download_images():
    """ download all images in shelf that has no file attribute.
        file attribute gets set after download of image
    """
    flickr = init_api()
    shelf = get_shelf()
    for key in shelf.keys():
        element = shelf[key]
        if 'file' not in element:
            # build filename with the end of the source-url of image
            filename = os.path.join(STORAGE, 'images',
                                    element['source'].split('/')[-1])
            r = requests.get(element['source'])
            if r.status_code == 200:
                img = r.raw.read()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(10240):
                        f.write(chunk)
                print("downloaded %s" % filename)
                element['file'] = filename
                shelf[key] = element
                shelf.sync()
        else:
            print("already downloaded %s" % key)
            

def auth():
    """ start browser to authorize your app for read access to your profile

    THIS MAY NOT BE NECESSARY!!
    """
    flickr = init_api()
    (token, frob) = flickr.get_token_part_one(perms='read')
    if not token: raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))


def by_username(username=None):
    flickr = init_api()
    rsp = flickr.people_findByUsername(username=username)
    for user in rsp:
        print("%s: %s" % (user[0].text, user.attrib.get('nsid')))


help_text = """Flickr Favorites downloader

Usage:
  favdownloader.py auth
  favdownloader.py get_userid <username>
  favdownloader.py update
  favdownloader.py download
  favdownloader.py (-h | --help)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

if __name__ == '__main__':
    args = docopt(help_text, version='Favdownloader V0.1')
    if args.get('auth'):
        auth()
    elif args.get('get_userid'):
        by_username(args['<username>'])
    elif args.get('update'):
        update_database()
    elif args.get('download'):
        download_images()
