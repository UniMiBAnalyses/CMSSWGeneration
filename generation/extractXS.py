import glob
import re
import sys
import json
import math
if len(sys.argv)<2:
    print("Specify output folder")
    sys.exit(1)

folder = "output/" + sys.argv[1]
roots = sorted(glob.glob(folder + "/root/*.root"))
XSs = []
XSerrs = []
ids = []
for root in roots:
    # Zjj_ewk_dim6_all_18_big_corr_2_11815156_999.root
    id = root.split("/")[-1].split(".")[0].split("_")[-1]
    
    #Zjj_ewk_dim6_all_18_big_corr_2.out_999
    name = sys.argv[1]+".out_"+id
    with open(folder+"/log/"+name) as file:
        lines = file.readlines()
        for line in lines:
            #INFO: Original cross-section: 28.01509 +- 0.256076 pb (cross-section from sum of weights: 28.015095)
            if "Original cross-section" in line:
                splitted = line.split(" ")
                XSs.append(float(splitted[3]))
                XSerrs.append(float(splitted[5]))
                ids.append(id)
                break
xs = sum(x / (e*e) for x, e in zip(XSs, XSerrs))
sumW = sum(1./(e*e) for e in XSerrs) 
xs /= sumW
err = 1./math.sqrt(sumW)

d = {'xs': xs, 'err': err, 'ids': ids}
with open(folder + "/XS.json", "w") as file:
   json.dump(d, file, indent=4) 


print("{} +/- {} for {} files".format(xs, err, len(XSs)))
                

