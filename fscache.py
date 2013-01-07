__doc__ = """
fscache provides a dictionary interface that stores cached values in the file system rather than in memory.
The file path is formed from an md5 hash of the key.
"""

import os
import sys
import datetime
import md5
import shutil


class fscache:
    """
    folder:
        the root level folder for the cache

    >>> cache = fscache()
    >>> # HTML to cache at URL
    >>> url = 'http://google.com/abc'
    >>> html = '<html>abc</html>'
    >>> # check if already in cache
    >>> url in cache
    False
    >>> # assign to cache
    >>> cache[url] = html
    >>> # check again whether in cache
    >>> url in cache
    True
    >>> # check content stored correctly
    >>> cache[url] == html
    True
    >>> # check the internal path where the html is cached
    >>> cache._key_path(url)
    '.fscache/c/1/3/9/3/b/d/2/0/3/4/2/6/f/3/c/3/f/4/7/5/5/b/0/3/0/a/1/d/b/a/c/index.html'
    >>> # check for non-existing key
    >>> cache.get(html, default='') == ''
    True
    >>> # clear the cache
    >>> cache.clear()
    """
    PARENT_DIR = '.fscache'
    FILE_NAME = 'index.html'

    def __init__(self, folder=''):
        self.folder = os.path.join(folder, fscache.PARENT_DIR)

    
    def __contains__(self, key):
        """Does data for this key exist
        """
        return os.path.exists(self._key_path(key))


    def __getitem__(self, key):
        path = self._key_path(key)
        try:
            fp = open(path, 'rb')
        except IOError:
            # key does not exist
            raise KeyError('%s does not exist' % key)
        else:
            # get value in key
            return fp.read()


    def __setitem__(self, key, value):
        """Save value at this key to this value
        """
        path = self._key_path(key)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        open(path, 'wb').write(value)


    def __delitem__(self, key):
        """Remove the value at this key and any empty parent sub-directories
        """
        path = self._key_path(key)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def _key_path(self, key):
        """The fils system path for this key
        """
        # create unique hash for this key
        try:
            key = key.encode('utf-8')
        except UnicodeDecodeError:
            pass
        h = md5.md5(key).hexdigest()
        # create file system path
        path = os.path.join(self.folder, os.path.sep.join(h), fscache.FILE_NAME)
        return path


    def get(self, key, default=''):
        """Get data at this key and return default if does not exist
        """
        try:
            value = self[key]
        except KeyError:
            value = default
        return value


    def clear(self):
        """Remove all the cached values
        """
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
