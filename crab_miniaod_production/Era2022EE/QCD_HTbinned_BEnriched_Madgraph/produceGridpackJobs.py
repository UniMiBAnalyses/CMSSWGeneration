import os, sys
import argparse
import subprocess
import shutil
from importlib import import_module

def parse_tuple(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-card-dir', type=str, default='./input_cards',help='directory containing the madgraph input cards')
parser.add_argument('-d', '--input-genprod-dir', type=str, default='',help='gen production directory to be copied at the node');
parser.add_argument('-s', '--gridpack-script', type=str, default='genproductions/bin/MadGraph5_aMCatNLO/gridpack_generation.sh',help='genprod script to be used');
parser.add_argument('-o', '--output-dir', type=str, default='./output_dir',help='output directory where to copy the gridpack')
parser.add_argument('-n', '--njet', type=int, nargs="+", default=[], help='list of the njet values to be generated')
parser.add_argument('-b', '--nbjet', type=int, nargs="+", default=[], help='list of the nbjet values to be generated')
parser.add_argument('-t', '--htbin', type=parse_tuple, nargs="+", default=[], help='list of the htmin and htmax values as a tuple')
parser.add_argument('-j', '--job-dir', type=str, default='job_gridpacks', help='directory where gridpacks jobs folder will be created')
parser.add_argument('-c', '--ncpu', type=int, default=1, help="requested number of cpus")
parser.add_argument('-q', '--queque', type=str, default="tomorrow", help='queque for condorHT')
parser.add_argument('-p', '--proxy', type=str, default='', help='location of proxy file')
parser.add_argument('-g', '--options-for-gridpack', type=str, default='', help='additional options to give to the gridpack script')
parser.add_argument('-e', '--command', type=str, default='none', help="possible commands are: submit, card, and none", choices=['submit','card','none']);

if __name__ == '__main__':
    
    args = parser.parse_args()

    if not os.path.exists(args.job_dir) and not os.path.isdir(args.job_dir):
        os.makedirs(args.job_dir);

    cwd = os.getcwd();
    if args.njet and args.nbjet:
        sys.exit("You cannot provide njet binning and nbjet binning simultaneously --> exit");
    elif args.njet and not args.nbjet:
        jet_binning = args.njet;
    elif not args.njet and args.nbjet:
        jet_binning = args.nbjet;
    else:
        sys.exit("You should provid either the njet or nbjet binning --> exit");
        
    for njet in jet_binning:
        for ht in args.htbin:
            if args.njet:
                print ("create gridpack job for njet=",njet," htbin=",ht);
                jetbin = "%djet"%(int(njet));
            else:
                print ("create gridpack job for nbjet=",njet," htbin=",ht);
                jetbin = "%dbjet"%(int(njet));
                
            htbin  = "HT_%d_%d"%(int(ht[0]),int(ht[1]));
            jdir = "QCD_bEnriched_"+jetbin+"_"+htbin;
            path = os.path.join(args.job_dir,jdir);
            if (os.path.exists(path) and os.path.isdir(path)):
                shutil.rmtree(path);
            if (os.path.exists(path) and not os.path.isdir(path)):
                shutil.rmtree(path);
            if not (os.path.exists(path) and os.path.isdir(path)):
                os.makedirs(path);

            ## copy cards for the job
            files = os.listdir(args.input_card_dir)
            for fname in files:
                if jetbin in fname:
                    shutil.copy2(os.path.join(args.input_card_dir,fname),path)

            with open(path+"/QCD_bEnriched_"+jetbin+"_HT_X_Y_proc_card.dat", 'r') as file :
                data = file.read()
                data = data.replace('$X',str(int(ht[0])))
                data = data.replace('$Y',str(int(ht[1])))
            with open(path+"/QCD_bEnriched_"+jetbin+"_HT_X_Y_proc_card.dat", 'w') as file:
                file.writelines(data);

            with open(path+"/QCD_bEnriched_"+jetbin+"_HT_X_Y_run_card.dat", 'r') as file :
                data = file.read()
                data = data.replace('$X',str(int(ht[0])))
                data = data.replace('$Y',str(int(ht[1])))
            with open(path+"/QCD_bEnriched_"+jetbin+"_HT_X_Y_run_card.dat", 'w') as file:
                file.writelines(data);

            ## rename the cards
            files = os.listdir(path)
            for fname in files:
                shutil.move(os.path.join(path,fname),os.path.join(path,fname.replace("QCD_bEnriched_"+jetbin+"_HT_X_Y",jdir)))

            if args.command == "card":
                continue;

            if args.proxy:
                shutil.copy(args.proxy,"./");
            ## write the job to be executed
            script_path = os.path.dirname(args.gridpack_script);
            script_name = os.path.basename(args.gridpack_script);
            job_script = open("%s/condor_job.sh"%(path),"w");
            job_script.write("#!/bin/bash\n");   
            if args.proxy:                
                job_script.write('export X509_USER_PROXY=$1\n');
            job_script.write('rsync -ua '+args.input_genprod_dir+' ./\n');
            job_script.write('tar -xf '+args.input_genprod_dir.split("/")[-1]+'\n');
            job_script.write('cd '+script_path+'\n');            
            job_script.write('rsync -ua '+cwd+'/'+path+' ./\n');
            if args.options_for_gridpack:
                job_script.write('./'+os.path.basename(script_name)+' '+jdir+' '+jdir+' '+args.options_for_gridpack+'\n');
            else:
                job_script.write('./'+os.path.basename(script_name)+' '+jdir+' '+jdir+'\n');
            job_script.write('mkdir -p '+args.output_dir+'\n');
            job_script.write('rsync -ua *tarball.tar.xz '+args.output_dir+'/\n');
            job_script.close();
            os.system("chmod +x %s/condor_job.sh"%(path));

            ## submit condor job
            condor_job = open("%s/condor_job.sub"%(path),"w");
            condor_job.write("executable = %s/condor_job.sh\n"%(path));
            condor_job.write("should_transfer_files = YES\n");
            condor_job.write("log = %s/condor_job.log\n"%(path));
            condor_job.write("output = %s/condor_job.out\n"%(path));
            condor_job.write("error = %s/condor_job.err\n"%(path));
            condor_job.write("when_to_transfer_output = ON_EXIT\n");
            condor_job.write("on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n");
            condor_job.write("universe = vanilla\n");
            condor_job.write("transfer_output_files = \"\"\n");
            condor_job.write("+JobFlavour = \""+args.queque+"\"\n");
            condor_job.write("request_cpus = "+str(args.ncpu)+"\n");
            if args.proxy:
                condor_job.write("Proxy_path = "+os.getcwd()+"/"+args.proxy.split("/")[-1]+"\n");
                condor_job.write("transfer_input_files = $(Proxy_path)\n");
                condor_job.write("arguments = "+args.proxy.split("/")[-1]+"\n");
            condor_job.write("queue\n");
            condor_job.close();

            if args.command == "submit":
                os.system("condor_submit %s/condor_job.sub"%(path));
            else:
                print("No jobs submitted cause submit option was not specified")

