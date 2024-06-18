import glob
import subprocess
from sys import argv
import sys
from random import randint
def findLatestSubmit(folder):
    submit = glob.glob("output/{}/submit*.jdl".format(folder))
    submitIds = list(map(lambda k: k.split("/")[-1].split(".")[0].split("submit")[1], submit))
    if len(submitIds)==1:
        return 1
    ids = sorted(list(filter(lambda k: k!='', submitIds)))
    ids = sorted(list(map(lambda k: int(k), ids)))
    print(ids[-1]+1)
    return ids[-1]+1

if len(argv)<2:
    print("Should specify output folder for which to resubmit jobs")
    sys.exit(1) 

folder = argv[1]

done = glob.glob("output/{}/root/*.root".format(folder))
#output/Zjj_ewk_dim6_all_17_big/root/Zjj_ewk_dim6_all_17_big_11764394_882.root
done = list(map(lambda k: k.split("/")[-1].split(".")[0].split("_")[-1], done))
finished = glob.glob("output/{}/log/*out*".format(folder))
#output/Zjj_ewk_dim6_all_17_big/log/Zjj_ewk_dim6_all_17_big.out_0
finished = list(map(lambda k: k.split("/")[-1].split(".")[-1].split("_")[-1], finished))
missing = list(set(finished).difference(set(done)))
print(missing)
print(len(missing))

with open("output/{}/submit.jdl".format(folder)) as file:
    txt = file.read()
newTxt = txt.replace("$(Step)", "$(mystep)")
newTxt =  list(filter(lambda k: "queue" not in k.lower(), newTxt.split('\n')))
newTxt.append("Queue proc, mystep from (")
newTxt.append('\n'.join(['\t{}, {}'.format(folder, n) for n in missing]))
newTxt.append(")")
newTxt = '\n'.join(newTxt)
submitId = findLatestSubmit(folder)
with open("output/{}/submit{}.jdl".format(folder, submitId), "w") as file:
    file.write(newTxt)

txt = "#!/bin/bash\n"
for miss in missing:
    txt += "rm log/*_{}\n".format(miss)
txt += "condor_submit submit{}.jdl\n".format(submitId)
with open("output/{}/resubmit.sh".format(folder),"w") as file:
    file.write(txt)
p = subprocess.Popen("chmod +x output/{}/resubmit.sh".format(folder), shell=True)
p.wait()
