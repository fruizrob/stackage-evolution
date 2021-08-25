import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("df", help="Dataframe file with package imports")
parser.add_argument("pkgs_path", help="Directory of packages")
parser.add_argument("lts", help="lts, example: 16.11")

args = parser.parse_args()
df = pd.read_pickle(args.df)
pkgs_path = args.pkgs_path
lts = args.lts

for index, pkg in df.iterrows():
    provided_modules_found = pkg["provided-modules-found"]
    new_list = []
    for (module, path) in provided_modules_found: 
        path = path.replace("//", "/")
        path = path.replace(lts, lts.replace(".", "-"))
        path = path.replace("./StackageDownload", pkgs_path)
        new_list.append((module, path))
    
    df.at[index, "provided-modules-found"] = new_list

    main_modules_found = pkg["main-modules-found"]
    new_list = []
    for path in main_modules_found: 
        path = path.replace("./StackageDownload", pkgs_path)
        path = path.replace(lts, lts.replace(".", "-"))
        new_list.append(path)
        
    df.at[index, "main-modules-found"] = new_list

    cabal_file = pkg["cabal-file"].replace("/Users/fruiz/Desktop/github/papers-stackage/pipelines/scripts/StackageDownload", pkgs_path)
    cabal_file = cabal_file.replace(lts, lts.replace(".", "-"))
    df.at[index, "cabal-file"] = cabal_file


df.to_pickle(args.df)