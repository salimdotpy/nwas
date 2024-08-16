import os, random, time
from flask import url_for, request
from PIL import Image

# USEFUL FUNCTIONS

def makeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return True

def menuActive(routeName):
    if request.path.split('/')[-1] == routeName:
        return 'active'
    elif request.endpoint == routeName:
        return 'active'
    elif request.path.split('/')[-2] == routeName:
        return 'active'
    return False

def removeFile(path):
    path = url_for('static', filename=path)[1:]
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return True
    return False

def siteName():
    return ['Neighbourhood Watch Assistance System', 'NWAS']

def systemDetails():
        system = {}
        system['name'] = 'SalimTech'
        system['version'] = '1.0'
        return system
    
def uniqueFilename():
    return f"{random.getrandbits(64)}_{int(time.time())}"

def uploadFile(file, location, size=None, old=None):
    path = makeDirectory(url_for('static', filename=location))
    if not path:
        raise Exception('File could not be created.')

    if old:
        removeFile(os.path.join(location, old))

    filename = f"{uniqueFilename()}.{file.filename.split('.')[-1]}"
    file.save(os.path.join(location, filename))
    return filename

def uploadImage(file, location, size=None, old=None, name=None):
    location = url_for('static', filename=location)[1:]
    path = makeDirectory(location)
    if not path:
        raise Exception('File could not be created.')

    if old:
        removeFile(os.path.join(location, old))
    
    filename = name if name else f"{uniqueFilename()}.{file.filename.split('.')[-1]}"
    file.save(os.path.join(location, filename))
    
    if size:
        width, height = map(int, size.lower().split('x'))
        image = Image.open(os.path.join(location, filename))
        # image.thumbnail((width, height))
        image = image.resize((width, height))
        image.save(os.path.join(location, filename))
    
    return filename

def getImage(image):
    img = url_for('static', filename=image)
    if os.path.exists(img[1:]) and os.path.isfile(img[1:]):
        return url_for('static', filename=image+'')
    return url_for('static', filename='images/noimage.png')
