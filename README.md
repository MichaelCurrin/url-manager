# URL Manager
> Centralize, view, edit, label and organize collections of your favorite URLs 

The aim is to help you create and find your URL more efficiently and within a personalised structure. The result is a tool for you to import browser bookmark-related URL data from various sources and manage them in a single structured, easy-to-search data source.

Import data from the following data sources:

- Bookmark files
    * Firefox
    * Chrome
- History file
- OneTab data
- A CSV created by hand in the required format

You can also add and manage records with a command-line tool.


# Documentation:

- Read this project's [docs](/docs) directory.
- [plyvel](https://plyvel.readthedocs.io) Python library to access LevelDB. This is used getting OneTab data from Chrome's _LevelDB_ storage. See also this LevelDB [Wiki page](https://en.wikipedia.org/wiki/LevelDB) and [article](https://www.developerfusion.com/news/123063/google-talks-leveldb-keyvalue-store-for-chrome/).
