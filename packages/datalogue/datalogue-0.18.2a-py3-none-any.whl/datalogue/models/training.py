from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Union
from datalogue.models.ontology import OntologyNode
from uuid import UUID
import itertools

from datalogue.errors import _enum_parse_error, DtlError
from datalogue.utils import _parse_list, _parse_string_list, SerializableStringEnum


class DataRef:
    def __init__(self, node: OntologyNode, path_list: List[List[str]]):
        self.node = node
        self.path_list = path_list
