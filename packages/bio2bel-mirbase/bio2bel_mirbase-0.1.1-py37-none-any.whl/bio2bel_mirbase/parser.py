# coding: utf-8

"""This module has the parser for miRBase."""

import gzip
from typing import Dict, Iterable, List, Mapping, Optional

from tqdm import tqdm

from bio2bel_mirbase.download import download_definitions

__all__ = [
    'get_definitions',
    'parse_definitions',
    'get_mirbase_name_to_id',
]


def get_definitions(path: Optional[str] = None, force_download: bool = False) -> List[Dict]:
    """Get the definitions as a list of dictionaries."""
    if path is None:
        path = download_definitions(force_download=force_download)
    return parse_definitions(path)


def get_mirbase_name_to_id() -> Mapping[str, str]:
    """Get the name to id mapping."""
    return {
        d['name']: d['identifier']
        for d in get_definitions()
    }


def parse_definitions(path: str) -> List[Dict]:
    """Parse miRNA data from filepath and convert it to dictionary.

    The structure of dictionary is {ID:[AC,DE,[[miRNA],[miRNA]]]}

    :param path: The path to the miRBase file
    """
    file_handle = (
        gzip.open(path, 'rt')
        if path.endswith('.gz') else
        open(path)
    )
    with file_handle as file:
        print(file_handle)
        return _process_definitions_lines(file)


def _process_definitions_lines(lines: Iterable[str]) -> List[Dict]:
    """Process the lines of the definitions file."""
    groups = []

    for line in lines:  # TODO replace with itertools.groupby
        if line.startswith('ID'):
            listnew = []
            groups.append(listnew)

        groups[-1].append(line)

    # print(groups[0][0][5:18])
    rv = []
    for group in tqdm(groups, desc='parsing'):
        name = group[0][5:23].strip()
        identifier = group[2][3:-2].strip()
        description = group[4][3:-1].strip()

        entry_data = {
            'name': name,
            'description': description,
            'identifier': identifier
        }

        mature_mirna_lines = [
            i
            for i, element in enumerate(group)
            if 'FT   miRNA    ' in element
        ]

        entry_data['products'] = [
            {
                'location': group[index][10:-1].strip(),
                'accession': group[index + 1][33:-2],
                'product': group[index + 2][31:-2],
            }
            for index in mature_mirna_lines
        ]

        entry_data['xrefs'] = [
            {
                'database': '',
                'identifier': '',
            }
        ]  # TODO @lingling93

        rv.append(entry_data)

    return rv
