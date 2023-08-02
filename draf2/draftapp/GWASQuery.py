from dataclasses import dataclass
from typing import Dict, List


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

@dataclass
class GeneLine:
    rsid: str
    snp_position: str
    associated_tfs: str
    associated_gwas_traits: str
    associated_enhancers: str   
    associated_gwas_efoids: str

@dataclass 
class GeneDict:
    geneInfo: Dict[str, List[GeneLine]]


