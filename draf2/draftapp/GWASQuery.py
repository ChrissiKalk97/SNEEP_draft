from dataclasses import dataclass
from typing import Dict




@dataclass
class SnpLine:
    snp_position: str
    associated_tfs: str
    associated_genes: str
    geneids: str
    associated_enhancers: str


@dataclass
class SnpDict:
    SnpInfo: Dict[str, SnpLine]


@dataclass
class GwasDict:
    gwasInfo: Dict[str, SnpDict]


