import os
import sys
import glob
import argparse
import subprocess
import shutil
import json
import tqdm
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dataset', type=str, default='',help='Name of the input dataset')
parser.add_argument('-o', '--output-file', type=str, default='',help='Name of the output file list')
parser.add_argument('-n', '--nthreads', type=int, default=8,help='Number of threads to make queries')
args = parser.parse_args()

## prepare rucio and in case not present alert the user
try:
    from rucio.client import Client
except ModuleNotFoundError:
    print("Please setup Rucio first via: source /cvmfs/cms.cern.ch/rucio/setup-py3.sh; export RUCIO_ACCOUNT=`whoami`")
    exit()

## make sure you did cmsenv
if not os.getenv("CMSSW_BASE"):
    print('Please setup CMSSW env before running this script ... do cmsenv');
    exit()

## taken from https://gitlab.cern.ch/crab3/CRABServer/-/blob/master/scripts/Utils/CheckDiskAvailability.py
def get_crab_blacklist():
    # let's makle a list of sites where CRAB will not run
    usableSitesUrl = 'https://cmssst.web.cern.ch/cmssst/analysis/usableSites.json'
    result = subprocess.run(f"curl -s {usableSitesUrl}", shell=True, stdout=subprocess.PIPE)
    usableSites = json.loads(result.stdout.decode('utf-8'))
    blackListedSites=[]
    for site in usableSites:
        if 'value' in site and site['value'] == 'not_usable':
            blackListedSites.append(site['name'])
    return(blackListedSites)

## crab black listed sites
blackListedSites = get_crab_blacklist()
print("Blacklisted sites in crab to be excluded: ",blackListedSites)

## DBS file list query
print("Query DBS for file list");
result = subprocess.run("dasgoclient --query 'file dataset="+args.dataset+" status=VALID'",shell=True, stdout=subprocess.PIPE,encoding='utf-8')
if result.returncode != 0:
    print("Error returned by dasgoclient query --> exit")
    exit()    

number_of_files, num_bad_queries, number_of_files_on_disk, number_of_files_on_disk_blacklist, number_of_valid_files = 0, 0, 0, 0, 0
list_of_input_files = result.stdout.splitlines()
number_of_files = len(list_of_input_files);
## divide files in blocks of args.nthreads
input_file_partitioned = [list_of_input_files[i:i + args.nthreads] for i in range(0,number_of_files,args.nthreads)]

## Use rucio to find files on disk
print("Query rucio for disk location of each files")

## subprocess for each file
import concurrent.futures
def run_command(input_file):
    cmd = "rucio list-file-replicas cms:"+input_file
    result = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    return result, input_file

list_valid_files = [];
for i,fsublist in enumerate(tqdm.tqdm(input_file_partitioned)):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_command,ifile) for ifile in fsublist]
        for future in concurrent.futures.as_completed(futures):
            result, file_name = future.result()
            if result.returncode != 0:
                print("Error returned by rucio list file replicas for file: "+file_name)
                num_bad_queries = num_bad_queries+1;
            for j,res in enumerate(result.stdout.splitlines()):
                if "Tape" in res: continue;
                elif "Disk" in res:
                    number_of_files_on_disk = number_of_files_on_disk+1;
                    if any(key in res for key in blackListedSites):
                        number_of_files_on_disk_blacklist = number_of_files_on_disk_blacklist+1;
                    else:
                        number_of_valid_files = number_of_valid_files+1;
                        list_valid_files.append(file_name);

print("Number of files in the dataset = ",number_of_files);
print("Number of bad queries = ",num_bad_queries);
print("Number of files on Disk = ",number_of_files_on_disk);
print("Number of files on Disk but in blacklist = ",number_of_files_on_disk_blacklist);
print("Number of Valid files = ",number_of_valid_files);

## remove possible duplicates
final_list = list(dict.fromkeys(list_valid_files))

with open(args.output_file, "w") as file:
    for line in final_list:
        file.write(line + "\n")        
