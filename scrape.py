
#%%
from dataclasses import dataclass
from pybliometrics.scopus import AbstractRetrieval, ScopusSearch
import bibtexparser
from thefuzz import process
import multiprocessing
import pandas as pd


#%%

@dataclass
class ScopusSearchTerms:
    _STARTBLOCK_AI: str = '''(
	"artificial intelligence" OR
	"machine learning" OR
	"deep learning" OR
	"reinforcement learning" OR
	"supervised learning" OR
	"unsupervised learning")'''

    _ENDBLOCK: str = '''
	AND PUBYEAR > 2013 AND PUBYEAR < 2025
	AND SRCTYPE ( j )
	AND DOCTYPE ( ar )
	AND LANGUAGE ( english )'''

    _EXCLUDE: str = '''NOT
	( "genetic algorithm" 
	OR "evolutionary algorithm" )'''

    _D_PPS: str = '''(
	"production" OR
	"manufacturing")'''

    _SD_SEQENCING: str = '''(
	"job sequencing" OR
	"heuristic rule" OR
	"priority rule")'''

    @property
    def STARTBLOCK_AI(self) -> str:
        return self._STARTBLOCK_AI.replace('\n\t', ' ').replace('\n', '')
    
    @property
    def ENDBLOCK(self) -> str:
        return self._ENDBLOCK.replace('\n\t', ' ').replace('\n', '')
    @property
    def EXCLUDE(self) -> str:
        return self._EXCLUDE.replace('\n\t', ' ').replace('\n', '')
    
    @property
    def D_PPS(self) -> str:
        return self._D_PPS.replace('\n\t', ' ').replace('\n', '')
    
    @property
    def SD_SEQENCING(self) -> str:
        return self._SD_SEQENCING.replace('\n\t', ' ').replace('\n', '')
    


#%% 
terms = ScopusSearchTerms()
term = ('TITLE-ABS-KEY (' + terms.STARTBLOCK_AI +
       ' AND ' + terms.D_PPS +
       ' AND ' + terms.SD_SEQENCING +
       ' AND ' + terms.EXCLUDE + 
       ')'
       + terms.ENDBLOCK)
term
#%%
print(f'Searching for: {term}')
s = ScopusSearch(term, integrity_fields=["eid"], integrity_action="warn")
#%%
print(s.get_results_size())
print(s.get_key_remaining_quota())

#%%
ids = s.get_eids()
print(len(ids), ids[:5])


#%%
bibtex_str = ""
for single_id in ids[:8]:
    ab = AbstractRetrieval(single_id, view='FULL', id_type='eid')
    bibtex_str += ab.get_bibtex()


print(bibtex_str)
#%%
library = bibtexparser.parse_string(bibtex_str)
bibtexparser.write_file("library.bib", library)
# %%
