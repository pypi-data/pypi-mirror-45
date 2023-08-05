
catalog_file_description = """
        This JSON file has the following format.  Comments are, of course, not present (since JSON does not support
        comments).  Single quotes here are, of course, double quotes in the rest of the file (since JSON encloses
        strings in double quotes).  Anything inside <angle brackets> is just standing in for the relevant value.  An
        ellipsis ... indicates that the preceding structure can be repeated.  Also note that the metadata entries for
        simulations may not be present if the record on zenodo is closed-access; see catalog_private_metadata.json if
        you have access to those simulations, which will contain the missing information.  That file should be read
        and written automatically by functions in this module, so that the catalog dict returned will contain all
        available information.

        {
            'catalog_file_description': '<this description>',
            'modified': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # UTC time of last-modified record in this file
            'records': {  # Includes *all* versions of *all* records published in the 'sxs' community, not just simulations
                '<id>': {  # This Zenodo ID key is a *string* containing the 'id' value inside this object (JSON requires keys to be strings)
                    # More details about this 'representation' object at http://developers.zenodo.org/#depositions
                    'conceptdoi': '10.5281/zenodo.<conceptrecid>',  # Permanent DOI for all versions of this record
                    'conceptrecid': '<conceptrecid>',  # ~7-digit integer (as string) collectively identifying all versions of this record
                    'created': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # UTC time of creation of this record on Zenodo
                    'doi': '10.5281/zenodo.<id>',  # Permanent DOI for this record
                    'doi_url': 'https://doi.org/10.5281/zenodo.<id>',  # URL for permanent DOI of this record
                    'id': <id>,  # ~7-digit integer uniquely identifying this record
                    'links': {
                         'badge': 'https://zenodo.org/badge/doi/10.5281/zenodo.<id>.svg',
                         'bucket': 'https://zenodo.org/api/files/<uuid>',  # Base URL for file uploads and downloads
                         'conceptbadge': 'https://zenodo.org/badge/doi/10.5281/zenodo.<conceptrecid>.svg',
                         'conceptdoi': 'https://doi.org/10.5281/zenodo.<conceptrecid>',  # Permanent link to webpage for most-recent version
                         'discard': 'https://zenodo.org/api/deposit/depositions/<id>/actions/discard',  # API action to discard a draft
                         'doi': 'https://doi.org/10.5281/zenodo.<id>',  # Permanent URL for this version
                         'edit': 'https://zenodo.org/api/deposit/depositions/<id>/actions/edit',  # API action to edit this record
                         'files': 'https://zenodo.org/api/deposit/depositions/<id>/files',  # Only present for author
                         'html': 'https://zenodo.org/deposit/<id>',  # Webpage for this version
                         'latest': 'https://zenodo.org/api/records/<id>',  # API endpoint for most-recent version
                         'latest_html': 'https://zenodo.org/record/<id>',  # Webpage for most-recent version
                         'publish': 'https://zenodo.org/api/deposit/depositions/<id>/actions/publish',  # Only present for author
                         'record': 'https://zenodo.org/api/records/<id>',  # Only present for author
                         'record_html': 'https://zenodo.org/record/<id>',  # Webpage for this particular version; only present for author
                         'self': 'https://zenodo.org/api/deposit/depositions/<id>'
                    },
                    'metadata': {  # Note that this is Zenodo metadata, and is different from the SXS metadata found below
                        'access_right': '<access>',  # Can be 'open', 'closed', 'embargoed', or 'restricted'
                        'communities': [
                            {'identifier': '<community_name>'},  # Names may include 'sxs' and 'zenodo'
                            ...
                        ],
                        'creators': [
                            {
                                'name': '<name>',  # Name of this creator in the format Family name, Given names
                                'affiliation': '<affiliation>',  # (Optional) Affiliation of this creator
                                'orcid': '<orcid>',  # (Optional) ORCID identifier of this creator
                                'gnd': '<gnd>'  # (Optional) GND identifier of this creator
                            },
                            ...
                        ],
                        'description': '<description>',  # Text description of this record
                        'doi': '10.5281/zenodo.<id>',  # Permanent DOI of this record
                        'keywords': [
                            '<keyword>',  # Optional; this array may be empty
                            ...
                        ],
                        'license': '<license_type>',  # Usually 'CC-BY-4.0' for SXS
                        'prereserve_doi': {'doi': '10.5281/zenodo.<id>', 'recid': <id>},
                        'publication_date': '<YYYY-MM-DD>',  # Possibly meaningless date (UTC)
                        'title': '<title>',
                        'upload_type': 'dataset'
                    },
                    'modified': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # (UTC) Last modification of this record (possibly just Zenodo metadata modified)
                    'owner': <user_id>,  # ~5-digit integer identifying the user who owns this record
                    'record_id': <id>,  # Same as 'id'
                    'state': '<state>',  # Can be 'done', 'inprogress', 'error', 'unsubmitted', possibly others
                    'submitted': <submitted>,  # True or false (always true for published records)
                    'title': '<title>'  # Same as ['metadata']['title'],
                    'files': [  # May not be present if this simulation is closed-access; see catalog_private_metadata.json as noted above
                        # See https://data.black-holes.org/waveforms/documentation.html for
                        # detailed descriptions of the *contents* of the files in each record.
                        {
                            'checksum': '<checksum>',  # MD5 checksum of file on Zenodo
                            'filename': '<filename>',  # Name of file; may contain slashes denoting directories
                            'filesize': <filesize>,  # Number of bytes in the file
                            'id': '<fileid>',  # A standard UUID (hexadecimal with characters in the pattern 8-4-4-4-12)
                            'links': {
                                'download': 'https://zenodo.org/api/files/<bucket>/<filename>',  # The URL to use to download this file
                                'self': 'https://zenodo.org/api/deposit/depositions/<deposition_id>/files/<fileid>'  # Ignore this
                            }
                        },
                        ...  # Other file descriptions in the order in which they were uploaded (not necessarily a meaningful order)
                    ]
                },
                ...
            },
            'simulations': {
                '<sxs_id>': {  # The SXS ID is a string like SXS:BHNS:0001 or SXS:BBH:1234
                    'conceptrecid': '<conceptrecid>',  # The Zenodo ID of the 'concept' record, which *resolves to* the most-recent version
                    'versions': [  # Zenodo IDs of each version.  There may only be one; index this list with [-1] to always get the most recent
                        '<id1>',  # Oldest version first
                        ...
                    ],
                    'metadata': {  # May not be present if this simulation is closed-access; see catalog_private_metadata.json as noted above
                        # Variable content describing (mostly) physical parameters of the system.  It's basically a
                        # python-compatible version of the information contained in 'metadata.txt' from the
                        # highest-resolution run in the most-recent version of this simulation.  That file is meant to
                        # be more-or-less as suggested in <https://arxiv.org/abs/0709.0093>.  The conversion to a
                        # python-compatible format means that keys like 'simulation-name' have had hyphens replaced by
                        # underscores so that they can be used as variable names in python and any other sane language
                        # (with apologies to Lisp).  As far as possible, values that are just strings in that file
                        # have been converted into the relevant types -- like numbers, integers, and arrays.  Note
                        # that some keys like eccentricity are sometimes numbers and sometimes the string '<number'
                        # (meaning that the eccentricity is less than the number), which is necessarily a string.
                        #
                        # Below are just the first few keys that *may* be present.  Note that closed-access
                        # simulations will have empty dictionaries here.
                        #
                        'simulation_name': '<directory_name>',  # This may be distinctly uninformative
                        'alternative_names': '<sxs_id>',  # This may be a list of strings
                        'initial_data_type': '<type>',  # Something like 'BBH_CFMS'
                        'number_of_orbits': <number>,  # This is a float
                        'relaxed_mass1': <m2>,
                        'relaxed_mass2': <m1>,
                        'relaxed_dimensionless_spin1': [
                            <chi1_x>,
                            <chi1_y>,
                            <chi1_z>
                        ],
                        'relaxed_dimensionless_spin2': [
                            <chi2_x>,
                            <chi2_y>,
                            <chi2_z>
                        ],
                        'relaxed_eccentricity': <eccentricity>,  # Or maybe a string...
                        'relaxed_orbital_frequency': [
                            <omega_x>,
                            <omega_y>,
                            <omega_z>
                        ],
                        'relaxed_measurement_time': <time>,
                        ...
                    },
                },
                ...
            }
        }
"""


def split_to_public_and_private(catalog):
    from collections import OrderedDict
    from copy import deepcopy
    public = deepcopy(catalog)
    private = {'records': OrderedDict(), 'simulations': OrderedDict()}
    for record_id in catalog['records']:
        is_public = (catalog['records'][record_id]['metadata']['access_right'] == 'open')
        if not is_public and 'files' in catalog['records'][record_id]:
            private['records'][record_id] = {'files': deepcopy(catalog['records'][record_id]['files'])}
            public['records'][record_id].pop('files', None)
    for sxs_id in catalog['simulations']:
        version = str(catalog['simulations'][sxs_id]['versions'][-1])
        record = catalog['records'][version]
        is_public = (record['metadata']['access_right'] == 'open')
        if not is_public and 'metadata' in catalog['simulations'][sxs_id]:
            private['simulations'][sxs_id] = {'metadata': deepcopy(catalog['simulations'][sxs_id]['metadata'])}
            public['simulations'][sxs_id].pop('metadata', None)
    return public, private


def join_public_and_private(public, private):
    from copy import deepcopy
    catalog = deepcopy(public)
    for record_id in private['records']:
        if record_id in public['records']:
            catalog['records'][record_id]['files'] = deepcopy(private['records'][record_id]['files'])
    for sxs_id in private['simulations']:
        if sxs_id in public['simulations']:
            catalog['simulations'][sxs_id]['metadata'] = deepcopy(private['simulations'][sxs_id]['metadata'])
    return catalog


def update(path='~/.sxs/catalog/catalog.json', verbosity=1):
    """Update a local copy of the SXS catalog

    Because git has better handling of revision history with incremental updates, and because most
    users will have set up their credentials for github, we prefer git to simply re-downloading the
    catalog from black-holes.  Specifically, we try to update the catalog in the following order.

    1) Private copy via github (git scheme)
    2) Private copy via github (https scheme)
    3) Public copy via direct download (https://data.black-holes.org/catalog.json)

    Parameters
    ==========
    path: str, defaults to '~/.sxs/catalog/catalog.json'
        Absolute or relative path to JSON file containing the catalog.  If the path does not end
        with '.json', it is assumed to be a directory containing a 'catalog.json' file.
    verbosity: int, defaults to 1
        Amount of information to output.  Less than 1 corresponds to no output; 1 to only print a
        notice if the private file cannot be retrieved; greater than 1 to print a notice about
        wherever the file is retrieved; greater than 2 shows the stdout/stderr from external calls;
        and greater than 3 also asks git to be verbose.

    """
    from os.path import expanduser, isdir, join, dirname, basename, exists
    from os import makedirs, chdir, getcwd, remove
    from shutil import copyfile
    from subprocess import call, check_call, DEVNULL
    from warnings import warn
    from .api.utilities import download
    from . import records

    path = expanduser(path)
    if not path.endswith('.json'):
        path = join(path, 'catalog.json')
    directory = dirname(path)
    if not exists(directory):
        makedirs(directory)
    chdir(directory)
    if verbosity > 2:
        stdout = None
        stderr = None
    else:
        stdout = DEVNULL
        stderr = DEVNULL
    if verbosity > 4:
        git_verbosity = '-v -v'
    elif verbosity > 3:
        git_verbosity = '-v'
    else:
        git_verbosity = ''
    if exists(path):
        copyfile(path, path+'.bak')
    try:
        git_success = False
        try:
            if call("git status {0} .".format(git_verbosity), shell=True, stdout=stdout, stderr=stderr):
                check_call("git init {0} .".format(git_verbosity), shell=True, stdout=stdout, stderr=stderr)
            call("git remote {0} add origin_git git@github.com:sxs-collaboration/zenodo_catalog.git".format(git_verbosity),
                 shell=True, stdout=stdout, stderr=stderr)
            call("git remote {0} add origin_https https://github.com/sxs-collaboration/zenodo_catalog.git".format(git_verbosity),
                 shell=True, stdout=stdout, stderr=stderr)
            for remote in ["origin_git", "origin_https"]:
                if not call("git pull {0} {1} master".format(git_verbosity, remote), shell=True, stdout=stdout, stderr=stderr):
                    call("git reset --hard HEAD", shell=True, stdout=stdout, stderr=stderr)
                    git_success = True
                    if verbosity>1:
                        print('Retrieved catalog from {0}.'.format(remote))
                    break
        except:  # If for *any* reason git failed...
            pass
        if not git_success:  # ...fall back to direct download
            print("Failed to pull private copy of catalog; downloading public version.")
            if verbosity >= 1:
                verbose = 1
            download('https://data.black-holes.org/catalog.json', basename(path), verbose)
    except:  # If for *any* reason that failed...
        if exists(path+'.bak'):  # ... move the original file (if it exists) back into place
            rename(path+'.bak', path)
        raise
    else:  # If everything went well...
        if exists(path+'.bak'):  # ... remove the backup
            remove(path+'.bak')

    catalog = read(path)
    representation_list = records(sxs=True, all_versions=True)
    update_records(catalog, representation_list)
    update_simulations(catalog, representation_list)
    write(catalog, catalog_file_name=path)


def read(path=None, join_private=True):
    """Read the catalog from a JSON file

    Parameters
    ==========
    path: None or string [defaults to None]
        Relative or absolute path to the catalog.json file described in this submodule.  If `None`,
        the function first searches in the current working directory, then in
        '~/.sxs/catalog/catalog.json'.
    join_private: bool [defaults to True]
        If True, look for 'catalog_private_metadata.json' in the same directory as the `path`, and
        add the metadata to the output catalog object.

    Returns
    =======
    catalog: dict
        The format is described in `sxs.zenodo.catalog.catalog_file_description`.

    """
    from os.path import expanduser, exists, join, dirname
    from json import load
    import sxs
    if path is None:
        if exists('catalog.json'):
            path = 'catalog.json'
        elif exists(expanduser('~/.sxs/catalog/catalog.json')):
            path = expanduser('~/.sxs/catalog/catalog.json')
        else:
            raise ValueError("Cannot find 'catalog.json' file in current directory or ~/.sxs/catalog/catalog.json.")
    else:
        path = expanduser(path)
    with open(path, 'r') as f:
        catalog = load(f)
    if join_private:
        try:
            private = read(join(dirname(path), 'catalog_private_metadata.json'), join_private=False)
            catalog = join_public_and_private(catalog, private)
        except:
            pass
    return catalog


def write(catalog, catalog_file_name=None, private_metadata_file_name=None):
    """Write catalog dictionary to file
    
    This function separates the catalog into a public part and any private SXS metadata.  If the
    latter exists, it gets written to the file given as the third parameter, or simply the file
    'catalog_private_metadata.json' in the same directory as the public part.

    Parameters
    ==========
    catalog: dict
        The catalog information in the format described by the string
        `sxs.zenodo.catalog.catalog_file_description`.
    catalog_file_name: str or None
        Path to the output public JSON file describing this catalog.  If None, the file is
        '~/.sxs/catalog/catalog.json'.  If the string is precisely 'sxs/zenodo/catalog.json', the
        file will be placed in the sxs module's path, which is typically in some directory like
        .../lib/python3.x/site-packages/sxs/zenodo.
    private_metadata_file_name: str or None
        Path to the output private JSON file describing any private metadata.  If None, the file
        will be placed alongside the 'catalog.json' file, and named 'catalog_private_metadata.json'.
        Note that this file will not be written at all if there are no private metadata sets.

    """
    from os.path import expanduser, join, dirname
    from json import dump
    import sxs
    if catalog_file_name == 'sxs/zenodo/catalog.json':
        catalog_file_name = join(dirname(sxs.__file__), 'zenodo', 'catalog.json')
    elif catalog_file_name is None:
        catalog_file_name = expanduser('~/.sxs/catalog/catalog.json')
    else:
        catalog_file_name = expanduser(catalog_file_name)
    if private_metadata_file_name is None:
        private_metadata_file_name = join(dirname(catalog_file_name), 'catalog_private_metadata.json')
    public, private = split_to_public_and_private(catalog)
    with open(catalog_file_name, 'w') as f:
        dump(public, f, indent=4, separators=(',', ': '), ensure_ascii=True)
    if private['simulations']:
        with open(private_metadata_file_name, 'w') as f:
            dump(private, f, indent=4, separators=(',', ': '), ensure_ascii=True)


def modification_time(representation_list):
    return sorted([r['modified'] for r in representation_list])[-1]


def sxs_metadata_file_description(representation):
    """Find metadata file from highest Lev for this simulation"""
    from os.path import basename
    files = representation.get('files', [])
    metadata_files = [f for f in files if basename(f['filename'])=='metadata.json']
    metadata_files = sorted(metadata_files, key=lambda f: f['filename'])
    if not metadata_files:
        return None
    return metadata_files[-1]


def fetch_metadata(url, login, *args, **kwargs):
    """Get the json file from zenodo"""
    from .api import Login
    login = login or Login(*args, **kwargs)
    r = login.session.get(url)
    if r.status_code != 200:
        return {}
    try:
        return r.json()
    except:
        return {}


def update_records(catalog, representation_list):
    """Update list of records from list of representations

    Note that this function updates the 'records' dictionary in place AND returns that updated
    dictionary.

    Parameters
    ==========
    catalog: dict
        The catalog information in the format described by the string
        `sxs.zenodo.catalog.catalog_file_description`.
    representation_list: list
        List of "representation" dictionaries as returned by Zenodo.

    """
    for representation in representation_list:
        record_id = str(representation['record_id'])
        catalog['records'][record_id] = representation
    return catalog['records']


def order_version_list(representation_dict, versions):
    return sorted([str(v) for v in set(versions)], key=lambda v: representation_dict[v]['created'])


def update_simulations(catalog, representation_list, login=None, *args, **kwargs):
    """Update list of simulations (and SXS metadata) from list of representations

    This function can be used to refresh the information about simulations found in the catalog from
    a list of "representation" objects as returned by zenodo.  Thus, if you search for new records
    on zenodo, and get that list back, you can simply run this function on the catalog and that
    list, and it will update all the information about simulations.  Note that this function updates
    the 'simulations' dictionary in place AND returns that updated dictionary.

    Parameters
    ==========
    catalog: dict
        The catalog information in the format described by the string
        `sxs.zenodo.catalog.catalog_file_description`.
    representation_list: list
        List of "representation" dictionaries as returned by Zenodo.
    
    All remaining parameters are passed to the `fetch_metadata` function.

    """
    from copy import deepcopy
    import re
    from collections import OrderedDict
    # from .. import sxs_identifier_regex
    from sxs import sxs_identifier_regex
    sxs_identifier_regex = re.compile(sxs_identifier_regex)
    simulations = deepcopy(catalog['simulations'])
    for i, r in enumerate(representation_list, 1):
        print('{0:6} of {1}: {2}'.format(i, len(representation_list), r['id']))
        sxs_id_match = sxs_identifier_regex.search(r['title'])
        if sxs_id_match:
            sxs_id = sxs_id_match['sxs_identifier']
            zenodo_id = r['id']
            conceptrecid = r['conceptrecid']
            if sxs_id in simulations:
                if zenodo_id not in simulations[sxs_id]['versions']:
                    # First, get the information for the current most-recent metadata
                    last_record_id = str(simulations[sxs_id]['versions'][-1])
                    last_representation = catalog['records'][last_record_id]
                    last_metadata_file_description = sxs_metadata_file_description(last_representation)
                    # Now, create the new sorted version list
                    simulations[sxs_id]['versions'] = order_version_list(catalog['records'], simulations[sxs_id]['versions'] + [zenodo_id])
                    new_last_record_id = str(simulations[sxs_id]['versions'][-1])
                    if last_record_id != new_last_record_id:
                        # Only if the most-recent Zenodo ID has changed do we need to check any more
                        new_last_representation = catalog['records'][new_last_record_id]
                        new_last_metadata_file_description = sxs_metadata_file_description(new_last_representation)
                        if (new_last_metadata_file_description is not None
                            and last_metadata_file_description['checksum'] != new_last_metadata_file_description['checksum']):
                            # Only if the metadata checksum has changed do we need to change the metadata
                            url = new_last_metadata_file_description['links']['download']
                            simulations[sxs_id]['metadata'] = fetch_metadata(url, login, *args, **kwargs)
                elif not simulations[sxs_id]['metadata']:
                    # Try to download the most-recent metadata; nothing else has changed.
                    last_record_id = str(simulations[sxs_id]['versions'][-1])
                    last_representation = catalog['records'][last_record_id]
                    last_metadata_file = sxs_metadata_file_description(last_representation)
                    if last_metadata_file is not None:
                        url = last_metadata_file['links']['download']
                        simulations[sxs_id]['metadata'] = fetch_metadata(url, login, *args, **kwargs)
                else:
                    pass  # Nothing for 'simulations' changed.  Something might have changed for 'records', though.
            else:
                metadata_file_description = sxs_metadata_file_description(r)
                simulations[sxs_id] = {
                    'conceptrecid': conceptrecid,
                    'versions': [zenodo_id],
                    'metadata': {}
                }
                if metadata_file_description is not None:
                    url = metadata_file_description['links']['download']
                    simulations[sxs_id]['metadata'] = fetch_metadata(url, login, *args, **kwargs)
    catalog['simulations'] = OrderedDict([(s, simulations[s]) for s in sorted(simulations)])
    return catalog['simulations']


def catalog_from_representation_list(representation_list, simulation_dict={}, login=None, *args, **kwargs):
    """Convert list of representations from Zenodo into catalog dictionary

    Given a list of "representation" dictionaries as returned by Zenodo, this function returns a "catalog" dictionary,
    as described by `catalog_file_description`.  In brief, this dictionary contains the `catalog_file_description`
    itself under that key, the UTC timestamp of the last modification of any item in the list, and then a series of keys
    given by the SXS identifiers of all the simulations in the input list, values for which are just the representations
    themselves.

    """
    from copy import deepcopy
    from collections import OrderedDict
    from textwrap import dedent
    catalog = OrderedDict()
    catalog['catalog_file_description'] = dedent(catalog_file_description).split('\n')[1:-1]
    catalog['modified'] = modification_time(representation_list)
    catalog['records'] = OrderedDict(sorted([(str(r['id']), r) for r in representation_list], key=lambda kv:kv[0]))
    catalog['simulations'] = deepcopy(simulation_dict)
    update_simulations(catalog, representation_list=representation_list, login=login, *args, **kwargs)
    return catalog


def nginx_map(map_file_path=None, catalog_path=None):
    """Create a mapping from SXS identifiers to Zenodo record numbers for nginx

    The input must be a catalog file.  The output is formatted for inclusion into an nginx
    configuration.  Note that this map file includes a `map_hash_max_size` directive, and thus must
    precede any `map` directives, or you will get an error that this directive is a duplicate (even
    if you never explicitly gave it previously).

    The output map matches both the plain SXS identifier (with nothing following it) and the
    identifier followed by an arbitrary file path.

    Parameters
    ==========
    catalog_path: None or string [defaults to None]
        This argument is passed to the `read` function in this submodule.
    map_file_path: None or string [defaults to None]
        Relative or absolute path to the nginx map file to be output.  If `None`, the function first
        attempts to write the file into '~/.sxs/catalog/sxs_to_zenodo.map'; if that is not possible,
        it tries to write to the same file in the current working directory.

    """
    from os.path import expanduser, exists, join, dirname
    import json
    import math
    from sxs.zenodo.catalog import read
    def touch(fname, times=None):
        from os import utime
        try:
            with open(fname, 'a'):
                utime(fname, times)
            return True
        except:
            pass
        return False
    # Decide on where to get the input
    if catalog_path is None:
        if exists('catalog.json'):
            catalog_path = 'catalog.json'
        elif exists(expanduser('~/.sxs/catalog/catalog.json')):
            catalog_path = expanduser('~/.sxs/catalog/catalog.json')
        else:
            raise ValueError("Cannot find 'catalog.json' file in current directory or ~/.sxs/catalog/catalog.json.")
    else:
        catalog_path = expanduser(catalog_path)
    # Decide on where to put the output
    if map_file_path is None:
        if touch(expanduser('~/.sxs/catalog/sxs_to_zenodo.map')):
            map_file_path = expanduser('~/.sxs/catalog/sxs_to_zenodo.map')
        elif touch('sxs_to_zenodo.map'):
            map_file_path = 'sxs_to_zenodo.map'
        else:
            raise ValueError("Cannot write to 'sxs_to_zenodo.map' file in current directory or in ~/.sxs/catalog/.")
    else:
        map_file_path = expanduser(map_file_path)
    # Get the input
    catalog = read(catalog_path)
    records = {sim: catalog['records'][str(catalog['simulations'][sim]['conceptrecid'])] for sim in catalog['simulations']}
    # Figure out how to construct the output
    size = 256 * 2**math.ceil(math.log2(len(records)+1))  # nginx needs this to know the hash size
    def file_prefix(sxs_id):
        prefix = sxs_id + '/'
        files = records[sxs_id].get('files', [])
        for f in files:
            if not f['filename'].startswith(prefix):
                return ''
        return prefix
    record_string = "    /waveforms/data/{0} record/{1};\n"
    file_string = "    ~/waveforms/data/{0}/(.*) record/{1}/files/{2}$1;\n"
    # Construct the output
    with open(map_file_path, 'w') as f:
        f.write("map_hash_max_size {0};\n".format(size))
        f.write("map $uri $zenodo_identifier {\n")
        f.write("    default communities/sxs;\n")
        for sxs_identifier in sorted(records):
            f.write(record_string.format(sxs_identifier, records[sxs_identifier]['id']))
        for sxs_identifier in sorted(records):
            f.write(file_string.format(sxs_identifier, records[sxs_identifier]['id'], file_prefix(sxs_identifier)))
        f.write("}\n")


def basic(catalog=None, path=None, join_private=True):
    """Return a more basic version of the catalog with just the simulations

    Basically, this function simply returns a copy of `catalog['simulations']`, except that the
    zenodo keys are removed (both conceptrecid and the list of versions) and replaced with a link to
    the DOI that resolves to the concept record, which then resolves to the most recent version.

    """
    from copy import deepcopy
    if catalog is None:
        catalog = read(path=path, join_private=join_private)
    simulations = deepcopy(catalog['simulations'])
    for sim in simulations:
        conceptrecid = simulations[sim].pop('conceptrecid', '')
        versions = simulations[sim].pop('versions', [])
        simulations[sim]['url'] = 'https://doi.org/10.5281/zenodo.{0}'.format(conceptrecid)
    return simulations


def to_pandas(catalog=None, path=None, join_private=True):
    """Convert simulations to pandas DataFrame

    This function interprets the fields strictly, so that we can do things like sorting and
    selection more sensibly.  Only pre-defined fields are stored, and any data that cannot be
    readily converted to each fields data type is set to the default value like an empty string,
    empty list, or NaN.

    """
    import pandas as pd
    from copy import deepcopy
    from ..metadata.fields import metadata_fields
    if catalog is None:
        catalog = read(path=path, join_private=join_private)
    simulations = deepcopy(catalog['simulations'])
    for sim in simulations:
        conceptrecid = simulations[sim].pop('conceptrecid', '')
        versions = simulations[sim].pop('versions', [])
        simulations[sim]['url'] = 'https://doi.org/10.5281/zenodo.{0}'.format(conceptrecid)
    columns = [field['name'] for field in metadata_fields if 'name' in field] + ['url']
