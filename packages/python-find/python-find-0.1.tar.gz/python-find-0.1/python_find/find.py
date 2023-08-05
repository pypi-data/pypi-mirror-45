#!/usr/bin/env python3

import argparse
import os
import re
import sys

from typing import Optional, List, Union

from .tree_search import TreeSearch

def find(root: str = '.',
            name: str = None,
            file_type: str = '*'
        ) -> None:
    search = TreeSearch(root, name, file_type)
    search.display()
    
def find_list(root: str = '.',
            name: str = None,
            file_type: str = '*'
        ) -> List[str]:
    search = TreeSearch(root, name, file_type)
    return search.get_list()

