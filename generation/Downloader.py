# python Downloader.py -y 2017 -s lhe premix miniAOD nanoAOD


import requests
import argparse 
import subprocess
import os
import json 
import glob
import sys
import re

def download(path, link, run=True):
    r = requests.get(link, verify=False)
    if r.status_code!=200:
        print("Bad response from server")
        sys.exit(1)
    lines = r.text.split("\n")
    try:
        begin_voms = lines.index(list(filter(lambda k: 'voms-proxy-init' in k, lines))[0])+1
    except IndexError:
        print("voms_proxy_init_line NOT found in {}, trying with export SCRAM_ARCH as begin.".format(link))
        print("If there was a download of something before the SCRAM ARCH, it will be missing and something is likely to fail")
        begin_voms = None
    
    begin_scram = lines.index(list(filter(lambda k: 'export SCRAM_ARCH' in k, lines))[0])
    scram = lines[begin_scram].split("=")[-1]
        
    ##index used to get the end of the file and the name of the sh file
    indices = [i for i, line in enumerate(lines) if 'EndOfTestFile' in line]
    index = max(indices)

    end = index +1
    print("OOOOOO: ", lines[index-1])
    shFileName = lines[index-1].split(".sh")[0].split(" ")[-1] + ".sh\n"
    print("Oooooo: ", shFileName)
    # end = None
    lines = lines[begin_voms:end] if begin_voms is not None else lines[begin_scram:end]
    lines = list(map(lambda k: k+'\n', lines))

    ## these lines are needed since the executable files in link dumps everything in a test.sh which is then execute
    ## and I had to put the end of the file in "EndOfTestFile" since otherwise the test is executed in a singularity 
    ## which is likely to fail in cmsconnect
    lines += "chmod +x {} \n".format(shFileName)
    lines += "sed -i 's/mv \.\.\/\.\.\/Configuration/cp -r \.\.\/\.\.\/Configuration/g' {}".format(shFileName)
    lines += "./{} \n".format(shFileName)

    if not os.path.isdir(path):
        os.makedirs(path)
    fileName = "script.sh" 
    pathToFile = path + "/" + fileName
    with open(pathToFile, "w") as file:
        file.writelines(lines)

    process = subprocess.Popen("chmod +x {}".format(pathToFile),shell=True)
    process.wait()
    if run:
        process = subprocess.Popen("cd {}; ./{}; cd -".format(path, fileName),shell=True)
        process.wait()
        fs = glob.glob(path+"/*.py")
        print()
        if len(fs)==0:
            print("No .py generateed")
            sys.exit(1)
        elif len(fs)==1:
            name = fs[0].split("/")[-1]
            process = subprocess.Popen("cd {}; cp {} ../; cd -".format(path, name),shell=True)
            process.wait()

        else:
            name = list(map(lambda k: k.split("/")[-1], fs))
            for n in name:
                process = subprocess.Popen("cd {}; cp {} ../; cd -".format(path, n),shell=True)
                process.wait()

        fs = glob.glob(path+"/CMSSW*")
        if len(fs)==1:
            name = {"release": fs[0].split("/")[-1], "filename": name}
        print("\n\nDeleting folder\n\n")
        process = subprocess.Popen("rm -r {}".format(path),shell=True)
        process.wait()
        return scram,name
    return scram,""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--year", help="Year" , required=True)
    parser.add_argument("-s","--steps", help="Step to download", nargs="+", required=False, default=["lhe", "sim", "digipremix", "hlt", "reco", "miniAOD", "nanoAOD"])
    parser.add_argument("-f","--fix", help="If true fixes input and output file names of year specified, you should first have created files for the entire flow" , nargs='?', type=int, const=0, default=0)


    args = parser.parse_args()

    with open("Steps.json") as file:
        Steps = json.load(file) 

    if args.fix==1:
         
        totalSteps = Steps[args.year]['steps']
        files = glob.glob("data/input_{}/*.py".format(args.year))
        stepFiles = []
        for step in totalSteps:
            a = sorted(list(filter(lambda k: step.lower() in k.lower(), files)))
            stepFiles.extend(a)
        previousFilename = ""
        for f in stepFiles:
            ## fix the numberOfThreads to 1, then in Generate it will be possible to go multithread. to do:
            # fixThreads(f)
            
            ## modify number of events hardcoded:
            with open(f, 'r') as file:
                filedata = file.read()
            filedata = re.sub(r'input\s*=\s*cms\.untracked\.int32\(\d+\)', 'input = cms.untracked.int32(-1)', filedata)
            filedata = re.sub(r'nevts:\d+', 'nevts:-1', filedata)
            with open(f, 'w') as file:
                file.write(filedata)

            if previousFilename!= "":
                # replace for this file the input file name with previousFilename
                print("Should write {} as input for {}".format(previousFilename, f))
                with open(f) as file:
                    txt = file.read()
                    pattern = re.compile('(process.source = cms.Source\("PoolSource",[\n\t ]*fileNames = cms.untracked.vstring\()([^)]*)\)')
                    r = re.sub(pattern, r"\1{})".format(previousFilename), txt)
                with open(f, "w") as file:
                    file.write(r)


            # read f and extract output filename
            with open(f) as file:
                txt = file.read()
                pattern = re.compile('.*cms\.OutputModule\("PoolOutputModule",[\n\t a-zA-Z0-9()\',=.\-:_*]*fileName[^=]*=[^=]*cms.untracked.string\(([^)]*)\)')
                a = pattern.search(txt)
                if a:
                    previousFilename = a.group(1)
            if "nanoaod" in f.lower():
                with open(f,"r") as file:
                    txt= file.read()
                    pattern = re.compile("PoolOutputModule")
                    r = re.sub(pattern, "NanoAODOutputModule", txt)
                    pattern2 = re.compile("NANOEDMAODSIMoutput")
                    r2 = re.sub(pattern2, "NANOAODSIMoutput", r)
                with open(f, "w") as file:
                    file.write(r2)

    else:

        totalYears = Steps.keys()
        if args.year not in totalYears:
            print("Year not valid")
            print("Valid years are: {}".format(", ".join(totalYears)))
            sys.exit(1)
        totalSteps = Steps[args.year]["steps"]
        if len(list(filter(lambda k: k not in totalSteps, args.steps)))>0:
            print("Steps not valid")
            print("Valid steps are: {}".format(", ".join(totalSteps)))
            sys.exit(1)
        print("\n\nSteps to be performed for year {}".format(args.year))
        for step in args.steps:
            print(step)
        print("\n\n")
        for step in args.steps:
            print("\n\nNow dowloading config for step: {} and year: {}\n\n".format(step, args.year))
            scram,name = download("data/input_{}/{}".format(args.year, step),Steps[args.year][step]['link'])
            print(name)
            if isinstance(name, str) or isinstance(name, list):
                Steps[args.year][step]['filename'] = name
            else:
                Steps[args.year][step]['filename'] = name["filename"]
                Steps[args.year][step]['release'] = name["release"]
            Steps[args.year][step]['SCRAM_ARCH'] = scram 
            

        
        with open("Steps.json", "w") as file:
            json.dump(Steps,file,indent=4, sort_keys=True)
