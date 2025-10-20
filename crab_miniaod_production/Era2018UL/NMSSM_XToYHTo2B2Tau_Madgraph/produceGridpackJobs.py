import os, sys
import argparse
import subprocess
import shutil
from importlib import import_module

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-card-dir', type=str, default='./input_cards',help='directory containing the madgraph input cards')
parser.add_argument('-d', '--input-genprod-dir', type=str, default='',help='gen production directory to be copied at the node');
parser.add_argument('-s', '--gridpack-script', type=str, default='genproductions/bin/MadGraph5_aMCatNLO/gridpack_generation.sh',help='genprod script to be used');
parser.add_argument('-o', '--output-dir', type=str, default='./output_dir',help='output directory where to copy the gridpack')
parser.add_argument('-x', '--mx', type=int, nargs="+", default=[], help='list of the mx values to be generated')
parser.add_argument('-y', '--my', type=int, nargs="+", default=[], help='list of the my values to be generated')
parser.add_argument('-j', '--job-dir', type=str, default='job_gridpacks', help='directory where gridpacks jobs folder will be created')
parser.add_argument('-q', '--queque', type=str, default="longlunch", help='queque for condorHT')
parser.add_argument('-e', '--command', type=str, default='none', help="possible commands are: submit and none", choices=['submit','none']);

if __name__ == '__main__':
    
    args = parser.parse_args()

    if not os.path.exists(args.job_dir) and not os.path.isdir(args.job_dir):
        os.makedirs(args.job_dir);

    cwd = os.getcwd();

    for x in args.mx:
        for y in args.my:
            print "create gridpack job for mX=",x," mY=",y;
            jdir = "NMSSM_XToYH_mX_%d_mY_%d"%(int(x),int(y))
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
                shutil.copy2(os.path.join(args.input_card_dir,fname),path)

            ## customize the cards
            with open(path+"/NMSSM_XToYH_customizecards.dat", 'r') as file :
                data = file.read()
                data = data.replace('$MX',str(x))
                data = data.replace('$MY',str(y))
            with open(path+"/NMSSM_XToYH_customizecards.dat", 'w') as file :
                file.writelines(data);

            with open(path+"/NMSSM_XToYH_proc_card.dat", 'r') as file :
                data = file.read()
                data = data.replace('$MX',str(x))
                data = data.replace('$MY',str(y))
            with open(path+"/NMSSM_XToYH_proc_card.dat", 'w') as file :
                file.writelines(data);
            
            ## rename the cards
            files = os.listdir(path)
            for fname in files:
                shutil.move(os.path.join(path,fname),os.path.join(path,fname.replace("NMSSM_XToYH",jdir)))

            ## write the job to be executed
            script_path = os.path.dirname(args.gridpack_script);
            script_name = os.path.basename(args.gridpack_script);
            job_script = open("%s/condor_job.sh"%(path),"w");
            job_script.write("#!/bin/bash\n");   
            job_script.write('rsync -ua '+args.input_genprod_dir+' ./\n');
            job_script.write('tar -xf '+args.input_genprod_dir.split("/")[-1]+'\n');
            job_script.write('cd '+script_path+'\n');            
            job_script.write('rsync -ua '+cwd+'/'+path+' ./\n');
            job_script.write('./'+os.path.basename(script_name)+' '+jdir+' '+jdir+'\n');
            job_script.write('rsync -ua *tarball.tar.xz '+args.output_dir+'\n');
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
            condor_job.write("queue\n");
            condor_job.close();

            if args.command == "submit":
                os.system("condor_submit %s/condor_job.sub"%(path));
            else:
                print("No jobs submitted cause submit option was not specified")
