""" lineage

tools for genetic genealogy and the analysis of consumer DNA test results

"""

"""
Copyright (C) 2016 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from itertools import chain
import os

import numpy as np
import pandas as pd

# http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html
from lineage.ensembl import EnsemblRestClient
from lineage.individual import Individual
from lineage.resources import Resources
from lineage.snps import SNPs
from lineage.utils import Parallelizer, create_dir, save_df_as_csv
from lineage.visualization import plot_chromosomes

# set version string with Versioneer
from lineage._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class Lineage:
    """ Object used to interact with the `lineage` framework. """

    def __init__(
        self,
        output_dir="output",
        resources_dir="resources",
        parallelize=True,
        processes=os.cpu_count(),
    ):
        """ Initialize a ``Lineage`` object.

        Parameters
        ----------
        output_dir : str
            name / path of output directory
        resources_dir : str
            name / path of resources directory
        parallelize : bool
            utilize multiprocessing to speedup calculations
        processes : int
            processes to launch if multiprocessing
        """
        self._output_dir = os.path.abspath(output_dir)
        self._ensembl_rest_client = EnsemblRestClient()
        self._resources = Resources(
            resources_dir=resources_dir, ensembl_rest_client=self._ensembl_rest_client
        )
        self._parallelizer = Parallelizer(parallelize=parallelize, processes=processes)

    def create_individual(self, name, raw_data=None):
        """ Initialize an individual in the context of the `lineage` framework.

        Parameters
        ----------
        name : str
            name of the individual
        raw_data : list or str
            path(s) to file(s) with raw genotype data

        Returns
        -------
        Individual
            ``Individual`` initialized in the context of the `lineage` framework
        """
        return Individual(name, raw_data, self._output_dir)

    def download_example_datasets(self):
        """ Download example datasets from `openSNP <https://opensnp.org>`_.

        Per openSNP, "the data is donated into the public domain using `CC0 1.0
        <http://creativecommons.org/publicdomain/zero/1.0/>`_."

        Returns
        -------
        paths : list of str or None
            paths to example datasets

        References
        ----------
        ..[1] Greshake B, Bayer PE, Rausch H, Reda J (2014), "openSNP-A Crowdsourced Web Resource
          for Personal Genomics," PLOS ONE, 9(3): e89204,
          https://doi.org/10.1371/journal.pone.0089204
        """
        paths = self._resources.download_example_datasets()

        if None in paths:
            print("Example dataset(s) not currently available")

        return paths

    def remap_snps(self, individual, target_assembly, complement_bases=True):
        """ Remap the SNP coordinates of an individual from one assembly to another.

        This method uses the assembly map endpoint of the Ensembl REST API service (via
        ``Resources``'s ``EnsemblRestClient``) to convert SNP coordinates / positions from one
        assembly to another. After remapping, the coordinates / positions for the individual's
        SNPs will be that of the target assembly.

        If the SNPs are already mapped relative to the target assembly, remapping will not be
        performed.

        Parameters
        ----------
        target_assembly : {'NCBI36', 'GRCh37', 'GRCh38', 36, 37, 38}
            assembly to remap to
        complement_bases : bool
            complement bases when remapping SNPs to the minus strand

        Returns
        -------
        chromosomes_remapped : list of str
            chromosomes remapped; empty if None
        chromosomes_not_remapped : list of str
            chromosomes not remapped; empty if None

        Notes
        -----
        An assembly is also know as a "build." For example:

        Assembly NCBI36 = Build 36
        Assembly GRCh37 = Build 37
        Assembly GRCh38 = Build 38

        See https://www.ncbi.nlm.nih.gov/assembly for more information about assemblies and
        remapping.

        References
        ----------
        ..[1] Ensembl, Assembly Map Endpoint,
          http://rest.ensembl.org/documentation/info/assembly_map
        """
        chromosomes_remapped = []
        chromosomes_not_remapped = []

        snps = individual.snps

        if snps is None:
            print("No SNPs to remap")
            return chromosomes_remapped, chromosomes_not_remapped
        else:
            chromosomes = snps["chrom"].unique()
            chromosomes_not_remapped = list(chromosomes)

        valid_assemblies = ["NCBI36", "GRCh37", "GRCh38", 36, 37, 38]

        if target_assembly not in valid_assemblies:
            print("Invalid target assembly")
            return chromosomes_remapped, chromosomes_not_remapped

        if isinstance(target_assembly, int):
            if target_assembly == 36:
                target_assembly = "NCBI36"
            else:
                target_assembly = "GRCh" + str(target_assembly)

        if individual.build == 36:
            source_assembly = "NCBI36"
        else:
            source_assembly = "GRCh" + str(individual.build)

        if source_assembly == target_assembly:
            return chromosomes_remapped, chromosomes_not_remapped

        assembly_mapping_data = self._resources.get_assembly_mapping_data(
            source_assembly, target_assembly
        )

        if assembly_mapping_data is None:
            return chromosomes_remapped, chromosomes_not_remapped

        tasks = []

        for chrom in chromosomes:
            if chrom in assembly_mapping_data:
                chromosomes_remapped.append(chrom)
                chromosomes_not_remapped.remove(chrom)
                mappings = assembly_mapping_data[chrom]
                tasks.append(
                    {
                        "snps": snps.loc[snps["chrom"] == chrom],
                        "mappings": mappings,
                        "complement_bases": complement_bases,
                    }
                )
            else:
                print(
                    "Chromosome {} not remapped; "
                    "removing chromosome from SNPs for consistency".format(chrom)
                )
                snps = snps.drop(snps.loc[snps["chrom"] == chrom].index)

        # remap SNPs
        remapped_snps = self._parallelizer(self._remapper, tasks)
        remapped_snps = pd.concat(remapped_snps)

        # update SNP positions and genotypes
        snps.loc[remapped_snps.index, "pos"] = remapped_snps["pos"]
        snps.loc[remapped_snps.index, "genotype"] = remapped_snps["genotype"]

        individual._set_snps(snps, int(target_assembly[-2:]))

        return chromosomes_remapped, chromosomes_not_remapped

    def _remapper(self, task):
        """ Remap SNPs for a chromosome.

        Parameters
        ----------
        task : dict
            dict with `snps` to remap per `mappings`, optionally `complement_bases`

        Returns
        -------
        pandas.DataFrame
            remapped SNPs
        """
        temp = task["snps"].copy()
        mappings = task["mappings"]
        complement_bases = task["complement_bases"]

        temp["remapped"] = False

        pos_start = int(temp["pos"].describe()["min"])
        pos_end = int(temp["pos"].describe()["max"])

        for mapping in mappings["mappings"]:
            # skip if mapping is outside of range of SNP positions
            if (
                mapping["original"]["end"] <= pos_start
                or mapping["original"]["start"] >= pos_end
            ):
                continue

            orig_range_len = mapping["original"]["end"] - mapping["original"]["start"]
            mapped_range_len = mapping["mapped"]["end"] - mapping["mapped"]["start"]

            orig_region = mapping["original"]["seq_region_name"]
            mapped_region = mapping["mapped"]["seq_region_name"]

            if orig_region != mapped_region:
                print("discrepant chroms")
                continue

            if orig_range_len != mapped_range_len:
                print("discrepant coords")  # observed when mapping NCBI36 -> GRCh38
                continue

            # find the SNPs that are being remapped for this mapping
            snp_indices = temp.loc[
                ~temp["remapped"]
                & (temp["pos"] >= mapping["original"]["start"])
                & (temp["pos"] <= mapping["original"]["end"])
            ].index

            if len(snp_indices) > 0:
                # remap the SNPs
                if mapping["mapped"]["strand"] == -1:
                    # flip and (optionally) complement since we're mapping to minus strand
                    diff_from_start = (
                        temp.loc[snp_indices, "pos"] - mapping["original"]["start"]
                    )
                    temp.loc[snp_indices, "pos"] = (
                        mapping["mapped"]["end"] - diff_from_start
                    )

                    if complement_bases:
                        temp.loc[snp_indices, "genotype"] = temp.loc[
                            snp_indices, "genotype"
                        ].apply(self._complement_bases)
                else:
                    # mapping is on same (plus) strand, so just remap based on offset
                    offset = mapping["mapped"]["start"] - mapping["original"]["start"]
                    temp.loc[snp_indices, "pos"] = temp["pos"] + offset

                # mark these SNPs as remapped
                temp.loc[snp_indices, "remapped"] = True

        return temp

    def _complement_bases(self, genotype):
        if pd.isnull(genotype):
            return np.nan

        complement = ""

        for base in list(genotype):
            if base == "A":
                complement += "T"
            elif base == "G":
                complement += "C"
            elif base == "C":
                complement += "G"
            elif base == "T":
                complement += "A"
            else:
                complement += base

        return complement

    def find_discordant_snps(
        self, individual1, individual2, individual3=None, save_output=False
    ):
        """ Find discordant SNPs between two or three individuals.

        Parameters
        ----------
        individual1 : Individual
            reference individual (child if `individual2` and `individual3` are parents)
        individual2 : Individual
            comparison individual
        individual3 : Individual
            other parent if `individual1` is child and `individual2` is a parent
        save_output : bool
            specifies whether to save output to a CSV file in the output directory

        Returns
        -------
        pandas.DataFrame
            discordant SNPs and associated genetic data

        References
        ----------
        ..[1] David Pike, "Search for Discordant SNPs in Parent-Child
          Raw Data Files," David Pike's Utilities,
          http://www.math.mun.ca/~dapike/FF23utils/pair-discord.php
        ..[2] David Pike, "Search for Discordant SNPs when given data
          for child and both parents," David Pike's Utilities,
          http://www.math.mun.ca/~dapike/FF23utils/trio-discord.php
        """
        self._remap_snps_to_GRCh37([individual1, individual2, individual3])

        df = individual1.snps

        # remove nulls for reference individual
        df = df.loc[df["genotype"].notnull()]

        # add SNPs shared with `individual2`
        df = df.join(individual2.snps["genotype"], rsuffix="2")

        genotype1 = "genotype_" + individual1.get_var_name()
        genotype2 = "genotype_" + individual2.get_var_name()

        if individual3 is None:
            df = df.rename(columns={"genotype": genotype1, "genotype2": genotype2})

            # find discordant SNPs between reference and comparison individuals
            df = df.loc[
                df[genotype2].notnull()
                & (
                    (df[genotype1].str.len() == 1)
                    & (df[genotype2].str.len() == 1)
                    & (df[genotype1] != df[genotype2])
                )
                | (
                    (df[genotype1].str.len() == 2)
                    & (df[genotype2].str.len() == 2)
                    & (df[genotype1].str[0] != df[genotype2].str[0])
                    & (df[genotype1].str[0] != df[genotype2].str[1])
                    & (df[genotype1].str[1] != df[genotype2].str[0])
                    & (df[genotype1].str[1] != df[genotype2].str[1])
                )
            ]
            if save_output:
                save_df_as_csv(
                    df,
                    self._output_dir,
                    "discordant_snps_{}_{}_GRCh37.csv".format(
                        individual1.get_var_name(), individual2.get_var_name()
                    ),
                )
        else:
            # add SNPs shared with `individual3`
            df = df.join(individual3.snps["genotype"], rsuffix="3")

            genotype3 = "genotype_" + individual3.get_var_name()

            df = df.rename(
                columns={
                    "genotype": genotype1,
                    "genotype2": genotype2,
                    "genotype3": genotype3,
                }
            )

            # find discordant SNPs between child and two parents
            df = df.loc[
                (
                    df[genotype2].notnull()
                    & (
                        (df[genotype1].str.len() == 1)
                        & (df[genotype2].str.len() == 1)
                        & (df[genotype1] != df[genotype2])
                    )
                    | (
                        (df[genotype1].str.len() == 2)
                        & (df[genotype2].str.len() == 2)
                        & (df[genotype1].str[0] != df[genotype2].str[0])
                        & (df[genotype1].str[0] != df[genotype2].str[1])
                        & (df[genotype1].str[1] != df[genotype2].str[0])
                        & (df[genotype1].str[1] != df[genotype2].str[1])
                    )
                )
                | (
                    df[genotype3].notnull()
                    & (
                        (df[genotype1].str.len() == 1)
                        & (df[genotype3].str.len() == 1)
                        & (df[genotype1] != df[genotype3])
                    )
                    | (
                        (df[genotype1].str.len() == 2)
                        & (df[genotype3].str.len() == 2)
                        & (df[genotype1].str[0] != df[genotype3].str[0])
                        & (df[genotype1].str[0] != df[genotype3].str[1])
                        & (df[genotype1].str[1] != df[genotype3].str[0])
                        & (df[genotype1].str[1] != df[genotype3].str[1])
                    )
                )
                | (
                    df[genotype2].notnull()
                    & df[genotype3].notnull()
                    & (df[genotype2].str.len() == 2)
                    & (df[genotype2].str[0] == df[genotype2].str[1])
                    & (df[genotype2] == df[genotype3])
                    & (df[genotype1] != df[genotype2])
                )
            ]

            if save_output:
                save_df_as_csv(
                    df,
                    self._output_dir,
                    "discordant_snps_{}_{}_{}_GRCh37.csv".format(
                        individual1.get_var_name(),
                        individual2.get_var_name(),
                        individual3.get_var_name(),
                    ),
                )

        return df

    def find_shared_dna(
        self,
        individual1,
        individual2,
        cM_threshold=0.75,
        snp_threshold=1100,
        shared_genes=False,
        save_output=True,
    ):
        """ Find the shared DNA between two individuals.

        Computes the genetic distance in centiMorgans (cMs) between SNPs using the HapMap Phase II
        GRCh37 genetic map. Applies thresholds to determine the shared DNA. Plots shared DNA.
        Optionally determines shared genes (i.e., genes that are transcribed from the shared DNA).

        All output is saved to the output directory as `CSV` or `PNG` files.

        Parameters
        ----------
        individual1 : Individual
        individual2 : Individual
        cM_threshold : float
            minimum centiMorgans for each shared DNA segment
        snp_threshold : int
            minimum SNPs for each shared DNA segment
        shared_genes : bool
            determine shared genes
        save_output : bool
            specifies whether to save output files in the output directory

        Returns
        -------
        one_chrom_shared_dna : pandas.DataFrame
            segments of shared DNA on one chromosome
        two_chrom_shared_dna : pandas.DataFrame
            segments of shared DNA on two chromosomes
        one_chrom_shared_genes : pandas.DataFrame
            shared genes on one chromosome
        two_chrom_shared_genes : pandas.DataFrame
            shared genes on two chromosomes
        """
        one_chrom_shared_genes = pd.DataFrame()
        two_chrom_shared_genes = pd.DataFrame()

        self._remap_snps_to_GRCh37([individual1, individual2])

        df = individual1.snps

        df = df.join(individual2.snps["genotype"], rsuffix="2", how="inner")

        genotype1 = "genotype_" + individual1.get_var_name()
        genotype2 = "genotype_" + individual2.get_var_name()

        df = df.rename(columns={"genotype": genotype1, "genotype2": genotype2})

        one_x_chrom = self._is_one_individual_male([individual1, individual2])

        genetic_map = self._resources.get_genetic_map_HapMapII_GRCh37()

        tasks = []

        chroms_to_drop = []
        for chrom in df["chrom"].unique():
            if chrom not in genetic_map.keys():
                chroms_to_drop.append(chrom)
                continue

            tasks.append(
                {
                    "genetic_map": genetic_map[chrom],
                    # get positions for the current chromosome
                    "snps": pd.DataFrame(df.loc[(df["chrom"] == chrom)]["pos"]),
                }
            )

        # drop chromosomes without genetic distance data
        for chrom in chroms_to_drop:
            df = df.drop(df.loc[df["chrom"] == chrom].index)

        # determine the genetic distance between each SNP using the HapMap Phase II genetic map
        snp_distances = map(self._compute_snp_distances, tasks)
        snp_distances = pd.concat(snp_distances)
        df["cM_from_prev_snp"] = snp_distances["cM_from_prev_snp"]

        # determine where individuals share an allele on one chromosome
        df["one_chrom_match"] = np.where(
            df[genotype1].isnull()
            | df[genotype2].isnull()
            | (df[genotype1].str[0] == df[genotype2].str[0])
            | (df[genotype1].str[0] == df[genotype2].str[1])
            | (df[genotype1].str[1] == df[genotype2].str[0])
            | (df[genotype1].str[1] == df[genotype2].str[1]),
            True,
            False,
        )

        # determine where individuals share alleles on both chromosomes
        df["two_chrom_match"] = np.where(
            df[genotype1].isnull()
            | df[genotype2].isnull()
            | (
                (df[genotype1].str.len() == 2)
                & (df[genotype2].str.len() == 2)
                & (
                    (df[genotype1] == df[genotype2])
                    | (
                        (df[genotype1].str[0] == df[genotype2].str[1])
                        & (df[genotype1].str[1] == df[genotype2].str[0])
                    )
                )
            ),
            True,
            False,
        )

        # genotype columns are no longer required for calculation
        df = df.drop([genotype1, genotype2], axis=1)

        one_chrom_shared_dna = self._find_shared_dna_helper(
            df[["chrom", "pos", "cM_from_prev_snp", "one_chrom_match"]],
            cM_threshold,
            snp_threshold,
            one_x_chrom,
        )
        two_chrom_shared_dna = self._find_shared_dna_helper(
            df[["chrom", "pos", "cM_from_prev_snp", "two_chrom_match"]],
            cM_threshold,
            snp_threshold,
            one_x_chrom,
        )

        if shared_genes:
            one_chrom_shared_genes = self._compute_shared_genes(one_chrom_shared_dna)
            two_chrom_shared_genes = self._compute_shared_genes(two_chrom_shared_dna)

        if save_output:
            self._find_shared_dna_output_helper(
                individual1,
                individual2,
                one_chrom_shared_dna,
                two_chrom_shared_dna,
                one_chrom_shared_genes,
                two_chrom_shared_genes,
            )

        return (
            one_chrom_shared_dna,
            two_chrom_shared_dna,
            one_chrom_shared_genes,
            two_chrom_shared_genes,
        )

    def _find_shared_dna_helper(self, df, cM_threshold, snp_threshold, one_x_chrom):
        tasks = []

        for chrom in df["chrom"].unique():
            tasks.append(
                {
                    "df": df.loc[df["chrom"] == chrom],
                    "chrom": chrom,
                    "cM_threshold": cM_threshold,
                    "snp_threshold": snp_threshold,
                    "one_x_chrom": one_x_chrom,
                }
            )

        # compute shared DNA between individuals
        shared_dna = map(self._compute_shared_dna, tasks)
        shared_dna = self._convert_list_of_lists_to_list(shared_dna)
        return self._convert_shared_dna_list_to_df(shared_dna)

    def _find_shared_dna_output_helper(
        self,
        individual1,
        individual2,
        one_chrom_shared_dna,
        two_chrom_shared_dna,
        one_chrom_shared_genes,
        two_chrom_shared_genes,
    ):
        cytobands = self._resources.get_cytoBand_hg19()

        if create_dir(self._output_dir):
            plot_chromosomes(
                one_chrom_shared_dna,
                two_chrom_shared_dna,
                cytobands,
                os.path.join(
                    self._output_dir,
                    "shared_dna_{}_{}.png".format(
                        individual1.get_var_name(), individual2.get_var_name()
                    ),
                ),
                "{} / {} shared DNA".format(individual1.name, individual2.name),
                37,
            )

        if len(one_chrom_shared_dna) > 0:
            file = "shared_dna_one_chrom_{}_{}_GRCh37.csv".format(
                individual1.get_var_name(), individual2.get_var_name()
            )
            save_df_as_csv(
                one_chrom_shared_dna, self._output_dir, file, float_format="%.2f"
            )

        if len(two_chrom_shared_dna) > 0:
            file = "shared_dna_two_chroms_{}_{}_GRCh37.csv".format(
                individual1.get_var_name(), individual2.get_var_name()
            )
            save_df_as_csv(
                two_chrom_shared_dna, self._output_dir, file, float_format="%.2f"
            )

        if len(one_chrom_shared_genes) > 0:
            file = "shared_genes_one_chrom_{}_{}_GRCh37.csv".format(
                individual1.get_var_name(), individual2.get_var_name()
            )
            save_df_as_csv(one_chrom_shared_genes, self._output_dir, file)

        if len(two_chrom_shared_genes) > 0:
            file = "shared_genes_two_chroms_{}_{}_GRCh37.csv".format(
                individual1.get_var_name(), individual2.get_var_name()
            )
            save_df_as_csv(two_chrom_shared_genes, self._output_dir, file)

    def _convert_list_of_lists_to_list(self, l):
        # https://stackoverflow.com/a/952952
        return list(chain.from_iterable(l))

    def _convert_shared_dna_list_to_df(self, shared_dna):
        df = pd.DataFrame(shared_dna, columns=["chrom", "start", "end", "cMs", "snps"])
        df.index.name = "segment"
        df.index = df.index + 1
        return df

    def _compute_shared_genes(self, shared_dna):
        knownGenes = self._resources.get_knownGene_hg19()
        kgXref = self._resources.get_kgXref_hg19()

        # http://seqanswers.com/forums/showthread.php?t=22336
        df = knownGenes.join(kgXref)

        shared_genes_dfs = []
        shared_genes = pd.DataFrame()

        for shared_segment in shared_dna.itertuples():
            # determine genes transcribed from this shared DNA segment
            temp = df.loc[
                (df["chrom"] == shared_segment.chrom)
                & (df["txStart"] >= shared_segment.start)
                & (df["txEnd"] <= shared_segment.end)
            ].copy()

            # select subset of columns
            temp = temp[
                [
                    "geneSymbol",
                    "chrom",
                    "strand",
                    "txStart",
                    "txEnd",
                    "refseq",
                    "proteinID",
                    "description",
                ]
            ]

            if len(temp) > 0:
                shared_genes_dfs.append(temp)

        if len(shared_genes_dfs) > 0:
            shared_genes = pd.concat(shared_genes_dfs, sort=True)

        return shared_genes

    def _is_one_individual_male(self, individuals):
        for individual in individuals:
            if individual.sex == "Male":
                return True
        return False

    def _compute_snp_distances(self, task):
        """ Compute genetic distance between SNPs.

        Parameters
        ----------
        task : dict
            dict with `snps` to compute distance between using `genetic_map`

        Returns
        -------
        pandas.DataFrame
            genetic distances between SNPs
        """
        genetic_map = task["genetic_map"]
        temp = task["snps"]

        # merge genetic map for this chrom
        temp = temp.append(genetic_map, ignore_index=False, sort=True)

        # sort based on pos
        temp = temp.sort_values("pos")

        # fill recombination rates forward
        temp["rate"] = temp["rate"].fillna(method="ffill")

        # assume recombination rate of 0 for SNPs upstream of first defined rate
        temp["rate"] = temp["rate"].fillna(0)

        # get difference between positions
        pos_diffs = np.ediff1d(temp["pos"])

        # compute cMs between each pos based on probabilistic recombination rate
        # https://www.biostars.org/p/123539/
        cMs_match_segment = (temp["rate"] * np.r_[pos_diffs, 0] / 1e6).values

        # add back into temp
        temp["cMs"] = np.r_[0, cMs_match_segment][:-1]

        temp = temp.reset_index()

        # use null `map` values to find locations of SNPs
        snp_indices = temp.loc[temp["map"].isnull()].index

        # use SNP indices to determine boundaries over which to sum cMs
        start_snp_ix = snp_indices + 1
        end_snp_ix = np.r_[snp_indices, snp_indices[-1]][1:] + 1
        snp_boundaries = np.c_[start_snp_ix, end_snp_ix]

        # sum cMs between SNPs to get total cM distance between SNPs
        # http://stackoverflow.com/a/7471967
        c = np.r_[0, temp["cMs"].cumsum()][snp_boundaries]
        cM_from_prev_snp = c[:, 1] - c[:, 0]

        temp = temp.loc[temp["map"].isna()]

        # add back into temp
        temp["cM_from_prev_snp"] = np.r_[0, cM_from_prev_snp][:-1]

        # restore index
        temp = temp.set_index("index")

        return pd.DataFrame(temp["cM_from_prev_snp"])

    def _compute_shared_dna(self, task):
        df = task["df"]
        chrom = task["chrom"]
        cM_threshold = task["cM_threshold"]
        snp_threshold = task["snp_threshold"]
        one_x_chrom = task["one_x_chrom"]

        if "one_chrom_match" in df.keys():
            match_col = "one_chrom_match"
        else:
            match_col = "two_chrom_match"

        shared_dna = []

        # set two_chrom_match in non-PAR region to False if an individual is male
        if chrom == "X" and match_col == "two_chrom_match" and one_x_chrom:
            df = df.copy()
            # https://www.ncbi.nlm.nih.gov/grc/human
            df.loc[
                (df["chrom"] == "X") & (df["pos"] > 2699520) & (df["pos"] < 154931044),
                "two_chrom_match",
            ] = False

        # get consecutive strings of trues
        # http://stackoverflow.com/a/17151327
        a = df.loc[(df["chrom"] == chrom)][match_col].values
        a = np.r_[a, False]
        a_rshifted = np.roll(a, 1)
        starts = a & ~a_rshifted
        ends = ~a & a_rshifted
        a_starts = np.nonzero(starts)[0]
        a_starts = np.reshape(a_starts, (len(a_starts), 1))
        a_ends = np.nonzero(ends)[0]
        a_ends = np.reshape(a_ends, (len(a_ends), 1))

        matches = np.hstack((a_starts, a_ends))

        c = np.r_[0, df.loc[(df["chrom"] == chrom)]["cM_from_prev_snp"].cumsum()][
            matches
        ]
        cMs_match_segment = c[:, 1] - c[:, 0]

        # get matching segments where total cMs is greater than the threshold
        matches_passed = matches[np.where(cMs_match_segment > cM_threshold)]

        # get indices where a_end boundary is adjacent to a_start, perhaps indicating a
        # discrepant SNP
        adjacent_ix = np.where(
            np.roll(matches_passed[:, 0], -1) - matches_passed[:, 1] == 1
        )

        # if there are adjacent segments
        if len(adjacent_ix[0]) != 0:
            matches_stitched = np.array([0, 0])
            prev = -1
            counter = 0

            # stitch together adjacent segments
            for x in matches_passed:
                if prev != -1 and prev + 1 == x[0]:
                    matches_stitched[counter, 1] = x[1]
                else:
                    matches_stitched = np.vstack((matches_stitched, x))
                    counter += 1

                prev = x[1]

            matches_passed = matches_stitched[1:]

        snp_counts = matches_passed[:, 1] - matches_passed[:, 0]

        # apply SNP count threshold for each matching segment; we now have the shared DNA
        # segments that pass the centiMorgan and SNP thresholds
        matches_passed = matches_passed[np.where(snp_counts > snp_threshold)]

        # compute total cMs for each match segment
        c = np.r_[0, df.loc[(df["chrom"] == chrom)]["cM_from_prev_snp"].cumsum()][
            matches_passed
        ]
        cMs_match_segment = c[:, 1] - c[:, 0]

        counter = 0
        # save matches for this chromosome
        for x in matches_passed:
            shared_dna.append(
                {
                    "chrom": chrom,
                    "start": df.loc[(df["chrom"] == chrom)].iloc[x[0]].pos,
                    "end": df.loc[(df["chrom"] == chrom)].iloc[x[1] - 1].pos,
                    "cMs": cMs_match_segment[counter],
                    "snps": x[1] - x[0],
                }
            )
            counter += 1
        return shared_dna

    def _remap_snps_to_GRCh37(self, individuals):
        for i in individuals:
            if i is None:
                continue

            self.remap_snps(i, 37)
