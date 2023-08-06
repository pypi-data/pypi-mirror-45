# Copyright 2019 John Reese
# Licensed under the MIT license

from attr import dataclass


@dataclass
class Config:
    # regex to match lines - unmatched lines will not be converted
    line_prefix: str = r""
