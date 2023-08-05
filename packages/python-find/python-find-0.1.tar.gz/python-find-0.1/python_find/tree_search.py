import os

from pathlib import Path
from typing import Optional, Union, List

class TreeSearch():
    def __init__(self, root: str = '.',
                name: str = None,
                file_type: str = '*',
            ) -> None:
        self.search_root = Path(os.path.expanduser(root))
        self.name = name

        valid_file_types = ['d', 'f', 'l', '*']
        if file_type not in valid_file_types:
            raise ValueError(f'{file_type}: Invalid file_type.')

        # searching for directories
        if file_type == 'd':
            self._add_dirs = True
            self._add_files = False
            self._add_links = False

        # search for files
        if file_type == 'f':
            self._add_dirs = False
            self._add_files = True
            self._add_links = False
    
        # searching for links
        if file_type == 'l':
            self._add_dirs = True
            self._add_files = True
            self._add_links = True
    
        # default file type search
        if file_type == '*':
            self._add_dirs = True
            self._add_files = True
            self._add_links = False

    def generate_found_files(self) -> str:
        for f in self.search_root.rglob('*'):
            if f.is_symlink() and self._add_links:
                if (self.name
                        and f.match(os.path.join(f.parent.name, self.name))):
                    if f.is_dir() and self._add_dirs:
                        yield str(f)

                    else:
                        yield str(f)

                if not self.name:
                    if f.is_dir() and self._add_dirs:
                        yield str(f)

                    else:
                        yield str(f)

            if not f.is_symlink() and not self._add_links:
                if f.is_file() and self._add_files:
                    if (self.name
                            and f.match(os.path.join(
                            f.parent.name, self.name))):
                        yield str(f)
    
                    if not self.name:
                        yield str(f)
                        
                if f.is_dir() and self._add_dirs:
                    if (self.name
                            and f.match(os.path.join(
                            f.parent.name, self.name))):
                        yield str(f)
    
                    if not self.name:
                        yield str(f)

    def get_list(self) -> List[str]:
        found_files = []
        for f in self.generate_found_files():
            found_files.append(f)

        return found_files

    def display(self) -> None:
        for f in self.generate_found_files():
            print(f)

