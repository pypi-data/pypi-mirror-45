# -*- coding: utf-8 -*-

"""Constants for Bio2BEL miRBase."""

import os

from bio2bel import get_data_dir

VERSION = '0.1.1'

MODULE_NAME = 'mirbase'
DATA_DIR = get_data_dir(MODULE_NAME)

DEFINITIONS_URL = "ftp://mirbase.org/pub/mirbase/CURRENT/miRNA.dat.gz"
DEFINITIONS_PATH = os.path.join(DATA_DIR, "miRNA.dat.gz")

SPECIES_URL = 'ftp://mirbase.org/pub/mirbase/CURRENT/organisms.txt.gz'
SPECIES_PATH = os.path.join(DATA_DIR, 'organisms.txt.gz')
SPECIES_HEADER = [
    'organism',
    'division',
    'name',
    'tree',
    'taxonomy_id',
]

ALIASES_URL = 'ftp://mirbase.org/pub/mirbase/CURRENT/aliases.txt.gz'
ALIASES_PATH = os.path.join(DATA_DIR, 'aliases.txt.gz')
