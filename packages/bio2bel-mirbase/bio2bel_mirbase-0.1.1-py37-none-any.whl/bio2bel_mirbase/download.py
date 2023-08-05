# -*- coding: utf-8 -*-

"""Utilities for downloading miRBase."""

import logging
from collections import defaultdict
from typing import List, Mapping, Tuple

from bio2bel.downloading import make_df_getter, make_downloader
from .constants import (
    ALIASES_PATH, ALIASES_URL, DEFINITIONS_PATH, DEFINITIONS_URL, SPECIES_HEADER, SPECIES_PATH, SPECIES_URL,
)

__all__ = [
    'get_species_df',
    'download_definitions',
    'get_aliases_df',
    'get_mirbase_alias_to_id',
]

logger = logging.getLogger(__name__)

get_species_df = make_df_getter(
    SPECIES_URL,
    SPECIES_PATH,
    sep='\t',
    names=SPECIES_HEADER,
    skiprows=1,
)

download_definitions = make_downloader(DEFINITIONS_URL, DEFINITIONS_PATH)

get_aliases_df = make_df_getter(
    ALIASES_URL,
    ALIASES_PATH,
    sep='\t',
)


def get_mirbase_alias_to_id() -> Tuple[Mapping[str, str], Mapping[str, List[str]]]:
    """Get the miRBase alias to miRBase identifier dictionary."""
    rv = {}
    multiple = defaultdict(list)
    df = get_aliases_df()
    for _, identifier, synonyms in df.itertuples():
        for k in set(synonyms.strip().split(';')):
            if not k:
                continue
            if k in rv:
                logger.info(f'multiple for {k} and {identifier}')
                multiple[identifier].append(k)
            else:
                rv[k] = identifier

    return rv, dict(multiple)
