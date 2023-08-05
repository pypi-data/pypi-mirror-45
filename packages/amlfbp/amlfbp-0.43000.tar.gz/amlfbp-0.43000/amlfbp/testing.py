import os
from pipeline import do_stuff

for root, dirs, files in os.walk("../my_tests/sample_scripts/pytorch", topdown=False):
    for name in files :

        if (".py" in name) :
                try :
                        script=os.path.join(root, name)
                        print("working on ",script)
                        do_stuff({"script":script,"experiment_name":"default","project_folder":None,"framework":None,"cluster_name":"basic","storage_account":None,"storage_key":None,"storage_path":None,"data":None})
                except Exception as err :
                        print(err)