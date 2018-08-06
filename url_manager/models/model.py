# -*- coding: utf-8 -*-
"""
Model application file.

TODO: Case insensitive uniqueness for path.
TODO: Validate on domain name that it is lower case. Or to_python is lowercased.
"""
__all__ = ['Location', 'Format', 'Browser', 'Source', 'Label', 'Folder',
           'Domain', 'Page', 'PageLabel']


import sqlobject as so
from formencode.validators import URL

from lib import validators
from models.connection import conn

# Set this here to give all classes a valid _connection attribute for
# doing queries with.
so.sqlhub.processConnection = conn


class Page(so.SQLObject):
    """
    Model a URI for a webpage on the internet.

    Do not worry about duplicate pairs of domain and path, since we want
    to allow those to occur on an import and to clean them up later.

    A page may have a null Folder (as unsorted), though a folder must always
    have a parent folder, even if the top folder is "root".
    """

    # The host website for the page.
    # TODO: Ensure this is always converted lowercase rather than raising
    # an error.
    domain = so.ForeignKey('Domain', notNull=True)

    # The location of the webpage relative to the domain.
    # TODO: Should this start with forwardslash? Check what happens when
    # splitting and joining.
    # TODO: Create custom validator?
    path = so.UnicodeCol(notNull=True)

    # Webpage title, usually taken from the metadata of the HTML head section.
    title = so.UnicodeCol(default=None)

    # The date and time when the record was created. Defaults to the
    # current time.
    created_at = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)

    # Optional preview image for the link, scraped from the metadata.
    image_url = so.UnicodeCol(default=None)

    description = so.UnicodeCol(default=None)

    # The folder this link is placed into. If null then the link must still
    # be sorted. Domain and path pairs must be unique in a folder.
    folder = so.ForeignKey('Folder')
    unique_idx = so.DatabaseIndex(domain, path, folder, unique=True)

    source = so.ForeignKey('Source', notNull=True)

    # Link to labels which this page is assigned to.
    labels = so.SQLRelatedJoin('Labels',
                               intermediateTable='page_label',
                               createRelatedTable=False)

    def get_url(self):
        return "".join((self.domain.value, self.path))


class Domain(so.SQLObject):
    """
    Model a website domain.

    TODO: Add columns for metadata including title, keywords, image and icon.
    """

    class sqlmeta:
        defaultOrder = 'value'

    # Full hostname or domain of the website.
    value = so.UnicodeCol(alternateID=True, validator=URL)

    # The date and time when the record was created. Defaults to the
    # current time.
    datetime_created = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)

    # Link to Page objects which have paths relative to the Domain name.
    pages = so.SQLMultipleJoin('Page')

    # Get Page objects for the domain as a list. This is less efficient
    # for filtering, but slightly more convenient for development.
    pages_list = so.MultipleJoin('Page')


class Folder(so.SQLObject):
    """
    Model a folder, which can contain Page objects.

    A folder can be a tree structure with one parent and many children. A
    folder may contain zero or more Page objects.

    Folder name has a unique constrainst. If the same folder name needs
    to be used in different parts of the folder tree, it should probably
    by a label instead.
    """

    name = so.UnicodeCol(alternateID=True)

    # Self-join to an optional parent folder. If NULL, then it is at the top
    # level.
    # TODO: Unique constraint to prevent multiple top level folders?
    # Or use "root" instead and the res are unsorted?
    parent = so.ForeignKey('Folder', default=None)

    # Link to the child Folder records of a Folder.
    children = so.SQLMultipleJoin('Folder')

    # Link to Page records within a Folder.
    pages = so.SQLMultipleJoin('Page')


class Label(so.SQLObject):
    """
    Model a label.

    Unlike a folder, a label does not fit into a tree hierarchy and its name
    must be unique in order to look it up properly.
    """

    # Descriptive name of the label, which must be unique.
    name = so.UnicodeCol(alternateID=True)

    # Link to pages assigned to the label.
    pages = so.SQLRelatedJoin('Page',
                              intermediateTable='page_label',
                              createRelatedTable=False)

class PageLabel(so.SQLObject):
    """
    Model the many-to-many relationship between Page and Label records.

    A Label may be applied to many Pages and a Page may have many Labels.
    But a paired relationship must be unique.

    Attributes here are based on a recommendation in the SQLObject docs.
    """

    page = so.ForeignKey('Page', notNull=True, cascade=True)
    label = so.ForeignKey('Label', notNull=True, cascade=True)
    unique_idx = so.DatabaseIndex(page, label, unique=True)


# TODO:
#class Task(so.SQLObject):
#    """
#    Model a ...
#    """

#    ...



# TODO: Move to metadata file.
class Source(so.SQLObject):
    """
    Model a datasource of exported or manually created webpage data.
    """

    # Creation date of source. This could be the last day that a source
    # was used and that could be related to moving away from using a device
    # or exporting data from a company computer before leaving a job.
    date_created = so.DateCol(notNull=True)
    date_created_idx = so.DatabaseIndex(date_created)

    # The format of the datasource.
    format_ = so.ForeignKey('Format', notNull=True)

    # The web browser where the data originated.
    browser = so.ForeignKey('Browser')

    # The location where one lived and worked when creating the datasource.
    location = so.ForeignKey('Location')

    # True if it was work related, false if it was personal.
    is_work = so.BoolCol(notNull=True)


class Browser(so.SQLObject):
    """
    Model a webpage browser.
    """

    name = so.UnicodeCol(alternateID=True, validator=validators.LowerCaseStr)


class Format(so.SQLObject):
    """
    Model a datasource format.

    For example, a manual entry, user-created CSV, bookmark export,
    history export, or OneTab export.
    """

    name = so.UnicodeCol(alternateID=True, validator=validators.LowerCaseStr)


class Location(so.SQLObject):
    """
    Model a location, such as where one lived or worked.
    """

    name = so.UnicodeCol(alternateID=True, validator=validators.LowerCaseStr)
