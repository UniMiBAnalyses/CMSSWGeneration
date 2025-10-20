import os, sys
import argparse
import subprocess
import shutil
from importlib import import_module

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-gridpack-dir', type=str, default='',help='directory containing the madgraph gridpacks reachable via gfal-ls')
parser.add_argument('-o', '--output-list-name', type=str, default='',help='name of the output list with gridpacks names')
parser.add_argument('-g', '--gfal-base-path', type=str, default='davs://eoscms.cern.ch:443/eos/cms/',help='gfal base path to access to a SE')
parser.add_argument('-xmin', '--mxmin', type=int, default=300,help='minimum value of mX')
parser.add_argument('-xmax', '--mxmax', type=int, default=2500,help='maximum value of mX')
parser.add_argument('-ymin', '--mymin', type=int, default=90,help='minimum value of mY')
parser.add_argument('-ymax', '--mymax', type=int, default=150,help='maximum value of mY')

if __name__ == '__main__':

    args = parser.parse_args()

    if '=' in args.input_gridpack_dir:
        args.input_gridpack_dir = args.input_gridpack_dir.split('=')[-1];
    
    gfal_query = subprocess.Popen("gfal-ls "+args.gfal_base_path+"/"+args.input_gridpack_dir,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE);
    gfal_query.wait();
    if gfal_query.returncode != 0:
        print "gfal query return code = ",gfal_query.returncode
        sys.exit(1)
    
    gridpack_files = gfal_query.stdout.read().decode().splitlines();

    gridpack_filtered_files = [];
    for gridpack in gridpack_files:

        gridpack_split = gridpack.split("_");

        if "MX" in gridpack_split:
            mx_index = gridpack_split.index("MX");
        elif "mX" in gridpack_split:
            mx_index = gridpack_split.index("mX");
        else:
            mx_index = gridpack_split.index("mx");
        mx_val = int(gridpack_split[mx_index+1]);

        if "MY" in gridpack_split:
            my_index = gridpack_split.index("MY");
        elif "mY" in gridpack_split:
            my_index = gridpack_split.index("mY");
        else:
            my_index = gridpack_split.index("my");
        my_val = int(gridpack_split[my_index+1]);
    
        ## filter away
        if mx_val < args.mxmin or mx_val >= args.mxmax: 
            continue;
        if my_val < args.mymin or my_val >= args.mymax: 
            continue;
            
        gridpack_filtered_files.append(str(gridpack));

    ## produce the list
    with open(args.output_list_name,"w") as f:
        for gridpack in gridpack_filtered_files:
            f.write(gridpack+"\n");
        f.close();

    ## produce the list with file destination to be copied at the node
    copy_file_list = args.output_list_name.replace(".","_copy.");
    with open(copy_file_list,"w") as f:
        for gridpack in gridpack_filtered_files:
            f.write(args.gfal_base_path+"/"+args.input_gridpack_dir+"/"+gridpack+"\n");
        f.close();        

    ## lauch copy command
    gfal_copy = subprocess.Popen("gfal-copy --force --from-file "+copy_file_list+" ./",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);    
    gfal_copy.wait();
    output,error = gfal_copy.communicate()
    if gfal_copy.returncode != 0:
        print "gfal copy return code = ",gfal_copy.returncode
        sys.exit(1)
    else:
        sys.exit(0)
