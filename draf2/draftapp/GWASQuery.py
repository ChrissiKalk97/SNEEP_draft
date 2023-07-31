from dataclasses import dataclass
from typing import List, Dict
from typing import NamedTuple



@dataclass
class SnpLine:
    snp_info: str
    tfs: str
    genenames: str
    geneids: str
    enhancers: str

@dataclass 
class SnpList:
    rsid: List[SnpLine]

@dataclass
class SnpDict:
    SnpDict: Dict[str, SnpList]


@dataclass
class GwasDict:
    gwasInfo: Dict[str, Dict[str, List[str]]]


dicty = {"rsid1": ["snp1, chr1", "tfs1", "genes1", "genes1", "enhnacers1"], "rsid2": ["snp2, chr2", "tfs2", "genes2", "genes2", "enhnacers2"]}


snpl1 = SnpLine("snp1, chr1", "tfs1", "genes1", "genes1", "enhnacers1")
snplist1 = SnpList(snpl1)

snpl2 = SnpLine("snp2, chr2", "tfs2", "genes2", "genes2", "enhnacers2")
snplist2 = SnpList(snpl2)

#print(GwasDict("gwas1", snplist1))





#class GwasDictSerializer(DataclassSerializer):
 #   class Meta:
 ##       dataclass = GwasDict

#print(SnpDict(dicty))
#gDict= {"gwas1": {"rsid1": snplist1, "rsid2": snplist2}, "gwas2": {"rsid1": snplist1, "rsid2": snplist2}}
#print(GwasDict(gDict))



#serializer = GwasDictSerializer(GwasDict(gDict))
#print(serializer.data)


