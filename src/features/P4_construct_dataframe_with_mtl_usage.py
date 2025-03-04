#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime

import copy
import pandas as pd
import os


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i: i + n]


####################################################################################
def generateDataframeByCategory(df, df_file, logging, directory_path, lts):
    """Takes a dataframe where a package has 1+ categories, and generates a new
    dataframe with unique package-category combinations, hence reflecting
    the multiplicity of categories by package
    """

    logging.info("Creating dataframe split by category")
    multicat_criteria = df["categories"].map(lambda x: len(x) > 1)

    catdf = df.copy()
    for idx in catdf.index:
        if len(catdf.loc[idx]["categories"]) == 1:
            theCat = catdf.loc[idx]["categories"][0]
            catdf.at[idx, "categories"] = theCat

    additionalrows = []

    for idx in catdf[multicat_criteria].index:
        currentRow = copy.deepcopy(df.loc[idx])
        for cat in currentRow["categories"]:
            newRow = copy.deepcopy(currentRow)
            newRow["categories"] = cat
            additionalrows.append(newRow)

    catdf = catdf.drop(catdf[multicat_criteria].index)
    catdf = catdf.append(additionalrows)
    catdf = catdf.sort_index()
    catdf.columns = [
        "category" if x == "categories" else x for x in catdf.columns.tolist()
    ]
    catdf["category"] = catdf["category"].apply(str)

    df_path = directory_path + "/%s-by-category.df" % lts 
    catdf.to_pickle(df_path)
    logging.info("Done creating dataframe split by category")

    return df_path

####################################################################################


def generate_monad_usage_dataframe(df_file, logging, directory_path, lts):
    """Takes a dataframe with the information of imported modules, and yields
    a new dataframe with the usage information of each monad in the mtl_modules list.
    """

    df = pd.read_pickle(df_file)

    listToProcess = df.index.tolist()
    nthreads = 4
    step = int(max(1, len(listToProcess) / nthreads))

    packagesMonadUsage = {}

    logging.info("Starting work at %s" % str(datetime.now()))

    for chunk in chunks(listToProcess, step):
        flatPkgImportedModules = [
            (idx, df.loc[idx]["imported-modules"]) for idx in chunk
        ]
        for pkg, imods in flatPkgImportedModules:
            pkgMonadUsage = {}
            for mtl_mod in mtl_modules:
                if mtl_mod in imods:
                    pkgMonadUsage[mtl_mod] = 1
                    logging.debug(mtl_mod)
                else:
                    pkgMonadUsage[mtl_mod] = 0

            for transformer_mod in transfromers_modules:
                if transformer_mod in imods:
                    pkgMonadUsage[transformer_mod] = 1
                else:
                    pkgMonadUsage[transformer_mod] = 0

            for other_mod in other_modules:
                if other_mod in imods:
                    pkgMonadUsage[other_mod] = 1
                else:
                    pkgMonadUsage[other_mod] = 0
            packagesMonadUsage[pkg] = pkgMonadUsage

    #####################################################################
    logging.info("Computing monad usage")

    # Add columns to dataframe

    moduleMonadUsageSeries = {}

    ### For MTL modules ##########################################################
    for mtl_mod in mtl_modules:
        moduleMonadUsageSeries[mtl_mod] = []
        for idx in listToProcess:
            moduleMonadUsageSeries[mtl_mod].append(
                packagesMonadUsage[idx][mtl_mod])
        df[mtl_mod] = pd.Series(
            moduleMonadUsageSeries[mtl_mod], index=df.index)
    ### For transformers modules ##########################################################
    for transformer_mod in transfromers_modules:
        moduleMonadUsageSeries[transformer_mod] = []
        for idx in listToProcess:
            moduleMonadUsageSeries[transformer_mod].append(
                packagesMonadUsage[idx][transformer_mod])
        df[transformer_mod] = pd.Series(
            moduleMonadUsageSeries[transformer_mod], index=df.index)
    ### For other non-MTL modules ##########################################################
    for other_mod in other_modules:
        moduleMonadUsageSeries[other_mod] = []
        for idx in listToProcess:
            moduleMonadUsageSeries[other_mod].append(
                packagesMonadUsage[idx][other_mod])
        df[other_mod] = pd.Series(
            moduleMonadUsageSeries[other_mod], index=df.index)

    df_path = directory_path + "/%s.df" % lts 
    df.to_pickle(df_path)
    generateDataframeByCategory(df, df_file, logging, directory_path, lts)
    logging.info("Finishing work at %s" % str(datetime.now()))


################################################################################

##################################################################
# These are all the modules provided by the mtl library
# which will be matched against the imports of every package.
##

# https://wiki.haskell.org/All_About_Monads
##

mtl_modules = [
    "Control.Monad.Cont",
    "Control.Monad.Cont.Class",
    "Control.Monad.Error",
    "Control.Monad.Error.Class",
    "Control.Monad.Except",
    "Control.Monad.Identity",
    "Control.Monad.List",
    "Control.Monad.RWS",
    "Control.Monad.RWS.Class",
    "Control.Monad.RWS.Lazy",
    "Control.Monad.RWS.Strict",
    "Control.Monad.Reader",
    "Control.Monad.Reader.Class",
    "Control.Monad.State",
    "Control.Monad.State.Class",
    "Control.Monad.State.Lazy",
    "Control.Monad.State.Strict",
    "Control.Monad.Trans",
    "Control.Monad.Writer",
    "Control.Monad.Writer.Class",
    "Control.Monad.Writer.Lazy",
    "Control.Monad.Writer.Strict",
    "Control.Monad.Trans",
    "Control.Monad.Trans.Class",
]
transfromers_modules = [
    "Control.Monad.Trans.Accum",
    "Control.Monad.Trans.Class",
    "Control.Monad.Trans.Cont",
    "Control.Monad.Trans.Except",
    "Control.Monad.Trans.Identity",
    "Control.Monad.Trans.Maybe",
    "Control.Monad.Trans.RWS",
    "Control.Monad.Trans.RWS.CPS",
    "Control.Monad.Trans.RWS.Lazy",
    "Control.Monad.Trans.RWS.Strict",
    "Control.Monad.Trans.Reader",
    "Control.Monad.Trans.Select",
    "Control.Monad.Trans.State",
    "Control.Monad.Trans.State.Lazy",
    "Control.Monad.Trans.State.Strict",
    "Control.Monad.Trans.Writer",
    "Control.Monad.Trans.Writer.CPS",
    "Control.Monad.Trans.Writer.Lazy",
    "Control.Monad.Trans.Writer.Strict"
]
other_modules = [
    "Control.Monad", 
    "System.IO",
    "Control.Monad.Trans.Control",
    "Control.Monad.Free",
    "Control.Monad.Free.Ap",
    "Control.Monad.Free.Church",
    "Control.Monad.Free.Class",
    "Control.Monad.Free.TH"
]
