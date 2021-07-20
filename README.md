# URL Manager 🔗 📙
> Centralize, view, edit, label and organize collections of your favorite URLs 

[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/url-manager?include_prereleases=&sort=semver)](https://github.com/MichaelCurrin/url-manager/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org)

[![dependency - SQLObject](https://img.shields.io/badge/dependency-SQLObject-blue)](https://pypi.org/project/SQLObject)
[![dependency - beautifulsoup4](https://img.shields.io/badge/dependency-beautifulsoup4-blue)](https://pypi.org/project/beautifulsoup4)


A meta bookmark manager to rule them all.


## About

The aim is to help you create and find your URL more efficiently and within a personalised structure. The result is a tool for you to import browser bookmark-related URL data from various sources and manage them in a single structured, easy-to-search data source.

Import data from the following data sources:

- Bookmark files
    * Firefox
    * Chrome
- History file
- OneTab data
- A CSV created by hand in the required format

You can also add and manage records with a command-line tool.


## Documentation

- Read this project's [docs](/docs) directory.
- [plyvel](https://plyvel.readthedocs.io) Python library to access LevelDB. 
   - This is used for getting OneTab data from Chrome's _LevelDB_ storage.
   - This have proven to cause some issues and the location changed I think, so scraping the frontend (for Firefox and Chrome) or using the text export might be easier than using LevelDB. 
   - See also this LevelDB [Wiki page](https://en.wikipedia.org/wiki/LevelDB) and [article](https://www.developerfusion.com/news/123063/google-talks-leveldb-keyvalue-store-for-chrome/).


## License

Released under [MIT](/LICENSE).
