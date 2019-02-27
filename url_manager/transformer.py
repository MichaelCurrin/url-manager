"""
Transform module.

Iterate over raw JSON files in a given location, containing bookmark or
Onetab data. Process files structure appropriately based on the prefix in
the filename.

Then convert the data of the input files to the following structure and
write out.

    {
        # Folders in the root folder.
        'folders': {
            # Folder title names are used as keys here.
            str: {
                # Recursive folder structure, containing zero or more key-value
                # pairs for folders and zero or more URLs as a list.
                'folders': dict
                'urls': list
            },
            str: {
               'folders': dict
               'urls': list
            },
            ...,
            ...
        },
        # URLs in the root folder - always empty but kept to match the
        # structure of the recursive folders.
        'urls': []
    }

Notes on bookmark data:
    For where 'root' is the top-level unamed folder in which folders and
    URLs as located and folders may contain folders and URLs. Though, a URL
    may not be in the root folder.

Notes on OneTab data:
    URLs must exist in groups.
    The group names can be customised but may be omitted.
    The structure is flat - groups cannot be nested.
    URLs may not exist at the top level, as they need to belong to a group.
"""
import glob
import json
import os

from lib import convert
from lib.config import AppConf


conf = AppConf()


def process_chrome_bookmarks(data):
    """
    Convert Chrome bookmarks data to the project's own structure.

    Process input Chrome bookmark data. With a folder, separate the children
    items, which are a mix of folders and URLs. Only extract required fields.

    :param data: dict object from a Chromer profile's Prefereces JSON file.
        With structure as:
            {
                'roots': {
                    'synced': dict, # Nested dict of folder and URL data.
                    'other': dict
                    'bookmark_bar': dict
                    'sync_transaction_version': ... # Optional field.
                }
                'checksum': str,
                'version': int
            }

    :return out_data: dict of transformed Chrombe book data, with structure
        as per this module's docstring.
    """
    bookmark_data = data['roots']

    bookmark_data.pop('sync_transaction_version', None)

    out_data = {}

    # The key can be ignored at this section level, since the folder's details
    # within the section provides a name and it is more readable there.
    for folder in bookmark_data.values():
         folder_name, child_data = process_chrome_folder(folder)
         out_data[folder_name] = child_data

    return {
        'folders': out_data,
        'urls': []
    }


def process_chrome_folder(folder):
    """
    Handle bookmark folder data and return as folder name and child data.

    Note: dict_keys(['children', 'date_modified', 'type', 'date_added',
                     'name', 'id'])

    :param folder: dict of data for a folder. The folder can contain URL data
        and subfolders (which are processed recursively).

    :return: 2-tuple of folder_name and child_data.
        folder_name: The name of the current folder.
        child_data: dict object with the following structure:
                {
                    'data': {
                        'folders': dict,
                        'urls': list
                    }
                }
            Where the value for 'folders' values is a dict of zero or more
            folders, each with recursive structure the same as the child_data
            structure.

            And where the value for 'urls' is a list of zero or more dict
            objects, each with the following structure:
                {
                    'title': str,
                    'url': str,
                    'date_added': str,
                }
            The time value is a stringified form of a datetime.datetime
            object. e.g. '2017-11-19 17:57'.
    """
    assert folder['type'] == 'folder', \
        "Expected folder but got: {}".format(folder['type'])

    folder_name = folder['name']
    folders = {}
    urls = []

    for child in folder['children']:
        if child['type'] == 'folder':
            assert child['name'] not in folders, "Folder name '{}' already "\
                "in current level.".format(child['name'])
            # Do recursive logic on the folder's subfolders.
            subfolder_name, child_data = process_chrome_folder(child)
            folders[subfolder_name] = child_data
        elif child['type'] == 'url':
            date_added = convert.from_chrome_epoch(child['date_added'])

            url = {
               'title': child['name'],
               'url': child['url'],
               'date_added': date_added.strftime(convert.DATETIME_FORMAT),
            }
            urls.append(url)
        else:
            raise AssertionError("Expect folder or url but got: {}"
                                 .format(child['type']))
    child_data = {
        'folders': folders,
        'urls': urls
    }

    return folder_name, child_data


def transform_onetab(data):
    """
    Process Onetab data and return in the project's own standard structure.

    :param data: dict of JSON data exported from Onetab browser extension,
        with structure as follows:
            {
                'tabGroups': [
                    # List of groups.
                    {
                        'createDate': int,
                        'label'     : str, # Optional field.
                        ...,

                        'tabsMeta': [
                            # List of tabs.
                            {
                                'id'   : int,
                                'title': str,
                                'url   : str

                            },
                            {
                                ...
                            },
                            ...
                        ]
                    }
                ]
            }

        The group's date is applied to all the tabs within it. If the group's
        label is available, we check that is unique across the tab groups.
        If not available, then use the folder's time to generate a UUID.
        This produces a deterministic result, which is preferred over a random
        value.

    :return out_data: dict of transformed Onetab data, with structure
        as per this module's docstring.
    """
    groups = data['tabGroups']

    out_data = {}

    for group in groups:
        group_time = group['createDate']
        date_added = convert.from_onetab_epoch(group_time)

        folder_name = group.get('label', None)
        if folder_name is None:
            folder_name = "onetab_group_{}".format(int(date_added.timestamp()))
        else:
            assert out_data.get(folder_name, None) is None

        tabs = [
            {
                'title': tab['title'],
                'url': tab['url'],
                'date_added': date_added.strftime(convert.DATETIME_FORMAT)
            } for tab in group['tabsMeta']
        ]

        out_data[folder_name] = {
            'folders': {},
            'urls': tabs
        }

    return {
        'folders': out_data,
        'urls': []
    }


def transform_file(in_path):
    """
    Transform data at a path to a given bookmark JSON file.

    Expect bookmark files in certain formats, convert them to a specific
    structure and write out to JSON files. These can then can be parsed
    later and added to the database.
    """
    filename = os.path.basename(in_path)
    # TODO: Confirm these values against notes and the model.
    # e.g. "bookmarks_chrome_mycompany_work" where last term is "personal"
    # or "work" and company name could be "private".
    description = os.path.splitext(filename)[0]
    try:
        area, browser, location, purpose = description.split("_")
    except ValueError:
        raise ValueError("Could not get metadata from filename: {}"
                         .format(filename))

    print("Reading: {}".format(in_path))
    with open(in_path) as f_in:
        data = json.load(f_in)

    if area == 'bookmarks':
        if browser in ['chrome', 'chromium']:
            transformed_data = process_chrome_bookmarks(data)
        else:
            raise ValueError("Bookmark conversion not supported for browser:"
                             " {}".format(browser))
    elif area == 'onetab':
        # The data format should be the same for all browsers.
        transformed_data = transform_onetab(data)

    processed_dir = conf.get('text_files', 'processed_dir')
    out_path = os.path.join(processed_dir, filename)
    print("Writing: {}".format(out_path))
    with open(out_path, 'w') as f_out:
        json.dump(
            transformed_data,
            f_out,
            indent=4,
            sort_keys=True
        )


def convert_and_write():
    """
    Convert available bookmark and OneTab data and write out files.
    """
    raw_dir = conf.get('text_files', 'raw_dir')
    file_paths = glob.glob("{}/*.json".format(raw_dir))

    for in_path in file_paths:
        transform_file(in_path)


def main():
    """
    Handle command-line arguments.
    """
    convert_and_write()


if __name__ == '__main__':
    main()
