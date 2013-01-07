=================
File System Cache
=================

File System Cache (fscache) provides a dictionary like interface and stores cached values in the file system rather than in memory.
The file path is formed from an md5 hash of the key.

Example use: ::

    >>> import fscache
    >>> cache = fscache.fscache()
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
