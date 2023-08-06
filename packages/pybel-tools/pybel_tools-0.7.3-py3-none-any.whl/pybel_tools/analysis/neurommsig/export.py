# -*- coding: utf-8 -*-

"""This module contains the functions needed to process the NeuroMMSig excel sheets as well as export as BEL.

To run, type :code:`python3 -m pybel_tools.analysis.neurommsig` in the command line
"""

import itertools as itt
import logging
import os
import re
import time
from functools import partial
from typing import Mapping

import pandas as pd

from bel_resources import get_bel_resource, make_knowledge_header
from pybel import BELGraph
from pybel.dsl import Abundance, Gene
from pybel.utils import ensure_quotes

log = logging.getLogger(__name__)

HGNCsymbolpattern = re.compile(r"^[A-Z0-9-]+$|^C[0-9XY]+orf[0-9]+$")

SNPpattern = re.compile(r"^rs[0-9]+$")
SNPspatternSpace = re.compile(r"^(rs[0-9]+)\s((rs[0-9]+)\s)*(rs[0-9]+)$")
SNPspatternComma = re.compile(r"^(rs[0-9]+),((rs[0-9]+),)*(rs[0-9]+)$")
SNPspatternSpaceComma = re.compile(r"^(rs[0-9]+), ((rs[0-9]+), )*(rs[0-9]+)$")
Checked_by_Anandhi = re.compile(r"No")

miRNApattern = re.compile(r"^MIR.*$")
miRNAspattern = re.compile(r"^(MIR.*),((MIR.*$),)*(MIR.*$)$")


def preprocessing_excel(path):
    """Preprocess the excel sheet

    :param filepath: filepath of the excel data
    :return: df: pandas dataframe with excel data
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(path):
        raise ValueError("Error: %s file not found" % path)

    # Import Models from Excel sheet, independent for AD and PD
    df = pd.read_excel(path, sheetname=0, header=0)

    # Indexes and column name
    # [log.info(str(x)+': '+str((df.columns.values[x]))) for x in range (0,len(df.columns.values))]

    # Starting from 4: Pathway Name

    # Fill Pathway cells that are merged and are 'NaN' after deleting rows where there is no genes
    df.iloc[:, 0] = pd.Series(df.iloc[:, 0]).fillna(method='ffill')

    # Number of gaps
    # log.info(df.ix[:,6].isnull().sum())

    df = df[df.ix[:, 1].notnull()]
    df = df.reset_index(drop=True)

    # Fill NaN to ceros in PubmedID column
    df.ix[:, 2].fillna(0, inplace=True)

    # Number of gaps in the gene column should be already zero
    if (df.ix[:, 1].isnull().sum()) != 0:
        raise ValueError("Error: Empty cells in the gene column")

    # Check current state
    # df.to_csv('out.csv')

    return df


def munge_cell(cell, line=None, validators=None):
    """

    :param cell:
    :param line:
    :param validators:
    :return:
    """
    if pd.isnull(cell) or isinstance(cell, int):
        return None

    c = ' '.join(cell.split())

    if validators is not None and all(re.match(validator, c) is None for validator in validators):
        if line:
            log.info("Munge cell error: aprox in line: %s: %s", line, c)
        return None

    return [x.strip() for x in str(c).strip().split(',')]


def preprocessing_br_projection_excel(path: str) -> pd.DataFrame:
    """Preprocess the excel file.

    Parameters
    ----------
    path : Filepath of the excel sheet
    """
    if not os.path.exists(path):
        raise ValueError("Error: %s file not found" % path)

    return pd.read_excel(path, sheetname=0, header=0)


munge_snp = partial(munge_cell, validators=[SNPpattern, SNPspatternSpaceComma])

mesh_alzheimer = "Alzheimer Disease"  # Death to the eponym!
mesh_parkinson = "Parkinson Disease"

pathway_column = 'Subgraph Name'
genes_column = 'Genes'
pmids_column = 'PMIDs'
snp_from_literature_column = 'SNPs from Literature (Aybuge)'
snp_from_gwas_column = 'Genome wide associated SNPs (Mufassra)'
snp_from_ld_block_column = 'LD block analysis (Mufassra)'
clinical_features_column = 'Imaging Features (Anandhi)'
snp_from_imaging_column = 'SNP_Image Feature (Mufassra & Anandhi)'

columns = [
    genes_column,
    pmids_column,
    snp_from_literature_column,
    snp_from_gwas_column,
    snp_from_ld_block_column,
    clinical_features_column,
    snp_from_imaging_column,
]


def preprocess(path: str) -> pd.DataFrame:
    df = preprocessing_excel(path)
    df[snp_from_literature_column] = df[snp_from_literature_column].map(munge_snp)
    df[snp_from_gwas_column] = df[snp_from_gwas_column].map(munge_snp)
    df[snp_from_ld_block_column] = df[snp_from_ld_block_column].map(munge_snp)
    df[clinical_features_column] = df[clinical_features_column].map(munge_cell)
    df[clinical_features_column] = df[clinical_features_column].map(
        lambda c: None if c is not None and c[0] == 'No' else c)
    df[snp_from_imaging_column] = df[snp_from_imaging_column].map(munge_snp)
    return df


def get_nift_values() -> Mapping[str, str]:
    """Extract the list of NIFT names from the BEL resource and builds a dictionary mapping from the lowercased version
    to the uppercase version.
    """
    r = get_bel_resource(NIFT)
    return {
        name.lower(): name
        for name in r['Values']
    }


def write_neurommsig_biolerplate(disease, file):
    lines = make_knowledge_header(
        name='NeuroMMSigDB for {}'.format(disease),
        description='SNP and Clinical Features for Subgraphs in {}'.format(disease),
        authors='Daniel Domingo-Fernandez, Charles Tapley Hoyt, Mufassra Naz, Aybuge Altay, Anandhi Iyappan',
        contact='daniel.domingo.fernandez@scai.fraunhofer.de',
        version=time.strftime('%Y%m%d'),
        namespace_url={
            'NIFT': NIFT,
            'HGNC': HGNC_HUMAN_GENES,
        },
        namespace_patterns={
            'dbSNP': DBSNP_PATTERN
        },
        annotation_url={
            'Subgraph': NEUROMMSIG,
            'MeSHDisease': MESHD
        },
    )

    for line in lines:
        print(line, file=file)

    print('SET Citation = {"PubMed", "NeuroMMSigDB", "28651363"}', file=file)
    print('SET Evidence = "Serialized from NeuroMMSigDB"', file=file)
    print('SET MeSHDisease = "{}"\n'.format(disease), file=file)


def write_neurommsig_bel(file,
                         df: pd.DataFrame,
                         disease: str,
                         nift_values: Mapping[str, str],
                         ):
    """Writes the NeuroMMSigDB excel sheet to BEL

    :param file: a file or file-like that can be writen to
    :param df:
    :param disease:
    :param nift_values: a dictionary of lowercased to normal names in NIFT
    """
    write_neurommsig_biolerplate(disease, file)

    missing_features = set()
    fixed_caps = set()
    nift_value_originals = set(nift_values.values())

    graph = BELGraph(
        name=f'NeuroMMSigDB for {disease}',
        description=f'SNP and Clinical Features for Subgraphs in {disease}',
        authors='Daniel Domingo-Fernández, Charles Tapley Hoyt, Mufassra Naz, Aybuge Altay, Anandhi Iyappan',
        contact='daniel.domingo.fernandez@scai.fraunhofer.de',
        version=time.strftime('%Y%m%d'),
    )

    for pathway, pathway_df in df.groupby(pathway_column):
        sorted_pathway_df = pathway_df.sort_values(genes_column)
        sliced_df = sorted_pathway_df[columns].itertuples()

        for _, gene, pubmeds, lit_snps, gwas_snps, ld_block_snps, clinical_features, clinical_snps in sliced_df:
            gene = ensure_quotes(gene)

            for snp in itt.chain(lit_snps or [], gwas_snps or [], ld_block_snps or [], clinical_snps or []):
                if not snp.strip():
                    continue
                graph.add_association(
                    Gene('HGNC', gene),
                    Gene('DBSNP', snp),
                    evidence='Serialized from NeuroMMSigDB',
                    citation='28651363',
                    annotations={
                        'MeSHDisease': disease,
                    },
                )

            for clinical_feature in clinical_features or []:
                if not clinical_feature.strip():
                    continue

                if clinical_feature.lower() not in nift_values:
                    missing_features.add(clinical_feature)
                    continue

                if clinical_feature not in nift_value_originals:
                    fixed_caps.add((clinical_feature, nift_values[clinical_feature.lower()]))
                    clinical_feature = nift_values[clinical_feature.lower()]  # fix capitalization

                graph.add_association(
                    Gene('HGNC', gene),
                    Abundance('NIFT', clinical_feature),
                    evidence='Serialized from NeuroMMSigDB',
                    citation='28651363',
                    annotations={
                        'MeSHDisease': disease,
                    },
                )

                if clinical_snps:
                    for clinical_snp in clinical_snps:
                        graph.add_association(
                            Gene('DBSNP', clinical_snp),
                            Abundance('NIFT', clinical_feature),
                            evidence='Serialized from NeuroMMSigDB',
                            citation='28651363',
                            annotations={
                                'MeSHDisease': disease,
                            },
                        )

    if missing_features:
        log.warning('Missing Features in %s', disease)
        for feature in missing_features:
            log.warning(feature)

    if fixed_caps:
        log.warning('Fixed capitalization')
        for broken, fixed in fixed_caps:
            log.warning('%s -> %s', broken, fixed)
