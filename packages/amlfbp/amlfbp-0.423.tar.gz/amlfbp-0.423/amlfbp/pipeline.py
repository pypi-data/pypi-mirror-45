from azureml.core import run
import azureml.core
from azureml.core import Experiment
from azureml.core import Workspace
import logging
from code_process import *


def do_stuff(args):
    #try :
    if True :
        experiment_name,project_folder,script,framework,cluster_name,storage_account,storage_key,storage_path,data=args["experiment_name"],args["project_folder"],args["script"],args["framework"],args["cluster_name"],args["storage_account"],args["storage_key"],args["storage_path"],args["data"]
        import shutil
        logging.info(args)
        if script is None :
            script=input(" training file : ")
            args["script"]=script
        else:
            logging.info("launching the training of : ",script)
        import os
        #transforming script into the filename and the dirname
        script=os.path.abspath(script)
        args["script"],args["project_folder"]=os.path.basename(script),os.path.dirname(script)



        if project_folder is None :
            import os
            project_folder=os.path.dirname(os.path.abspath(script))
            print("working in undeclared folder",project_folder)
        else :
            if project_folder!=os.path.dirname(os.path.abspath(script)):
                logging.warning("working directory is not where the script is referenced, if external files are needed bugs are possible")
            logging.info("working in folder ",project_folder)
            logging.info("beware : by")
            os.makedirs(project_folder, exist_ok=True)
            print("checkfile",script)
            if not os.path.isfile(script) :
                shutil.copy(script, project_folder)

        logging.info("starting to do stuf...")
        from azureml.core.compute import ComputeTarget, AmlCompute

        ### LOADING THE WORKSPACE ###
        try :
            ws = Workspace.from_config()
            logging.info("workspace already created, loading the workspace")
            if cluster_name is None :
                logging.info("hey let's select a random cluster ! (no cluster specified)")
                cluster_name = [k for k in ws.compute_targets.keys()][0]
                logging.info("it worked ! we selected : ",cluster_name)
            cluster = ComputeTarget(workspace=ws, name=cluster_name)
        except :            
            
            from config import config
            ws,cluster_name=config(args)
            print("debug",ws,cluster_name)
            cluster = ComputeTarget(workspace=ws, name=cluster_name)        
    
        ### LOADING THE EXPERIMENT ###
        if experiment_name is None :
            experiment_name=input(" experiment name (>4 characters) : ")
            args["experiment_name"]=experiment_name
        else : 
            logging.info("working on experiment : ", experiment_name )

        if experiment_name not in ws.experiments.keys() :
            stay=input("This experiment does not exist, do you want to create the experiment "+str(experiment_name)+"? (Y/N)")
            while stay not in ["Y","N"]:
                stay=input("value must be \"Y\" or \"N\", please enter valid value : ")
            if stay=="N" :
                logging.info("exiting..")
                return ""
            elif stay=="Y":
                logging.info("creating experiment... OK that part doesn't work yet...")
                from azureml.core import Experiment
                experiment = Experiment(workspace=ws, name=experiment_name)
                logging.info("experiment created ! ",experiment_name)
        else :
            from azureml.core import Experiment
            experiment = Experiment(workspace = ws, name = experiment_name)
        
    

        ### LOADING THE TRAIN FILE ###
        import os
    
        
        ### LINKING THE DATA ###
        from azureml.core import Datastore

        if data is None or data=="" :
            data=input("please enter the url to your data (full url with blob and container), or pass if your script has no data : ")
            args["data"]=data
            if data !="":
                a,b=check_data_url(data)
                while a is None :
                    logging.error("data url error",b)
                    data=input("error in your blob url : (press \"N\" to cancel)",b)
                    if data=="N":
                        break
                    else:
                        a,b=check_data_url(data)
                if a is not None :
                    storage_account,storage_path=a,b
                    args["storage_account"],args["storage_path"]=storage_account,storage_path
        
                if storage_path is None :
                    storage_path=input("please enter relative path to the container of your data : ")
                    args["storage_path"]=storage_path
            
                if storage_key is None :
                    storage_key=input("please enter the Access key to access your data : ")
                    args["storage_key"]=storage_key
                
                ds = Datastore.register_azure_blob_container(workspace=ws, 
                                                        datastore_name='autogenerated', 
                                                        container_name=storage_path,
                                                        account_name=storage_account, 
                                                        account_key=storage_key,
                                                        create_if_not_exists=True,
                                                        overwrite=True)

                script_params = {
                '--data_folder': ds.as_mount()
                }
            else : 
                script_params={}
    
        ### DOING THE TRAINING
        packages=get_dependencies(os.path.join(project_folder,script))
        print("packages : ",packages)
        
        if framework is None:
            framework = autodetect_framework(script).lower()
            logging.info("autodetected framework : ",framework)
        else :
            framework=framework.lower()
            logging.info("you specified the framework : ",framework)
        
        if framework=="pytorch": 
            logging.info("detected PyTorch as backend Framework, will work accordingly")  
            from azureml.train.dnn import PyTorch
            estimator=PyTorch(source_directory=project_folder,
                                script_params=script_params,
                                compute_target=cluster,
                                entry_script=script,
                                pip_packages=packages
                            )
        elif framework=="tensorflow" :
            logging.info("detected Tensorflow as backend Framework, will work accordingly")  
            from azureml.train.dnn import TensorFlow
            estimator=TensorFlow(
                            source_directory=project_folder,
                            script_params=script_params,
                            compute_target=cluster,
                            entry_script=script,
                            conda_packages=packages
                            )
        elif framework == "chainer":
            logging.info("detected Chainer as backend Framework, will work accordingly. The implementation is buggy, though.")  
            from azureml.train.dnn import Chainer
            estimator=Chainer(
                            source_directory=project_folder,
                            script_params=script_params,
                            compute_target=cluster,
                            entry_script=script,
                            pip_packages=packages
                            )           
        else : 
            logging.warning("WARNING : didn't detect PyTorch, Tensorflow, or Chainer. If you are working with those, please input it as --framework (pytorch/tensorflow/chainer)")  
            from azureml.train.estimator import Estimator
            print("parameters of the training : ",project_folder,script_params,os.path.basename(script))
            estimator = Estimator(
                            source_directory=project_folder,
                            script_params=script_params,
                            compute_target=cluster,
                            entry_script=os.path.basename(script),
                            conda_packages=packages
                          
            )
     
        run = experiment.submit(estimator)
        run
        # Shows output of the run on stdout.
        run.wait_for_completion(show_output=True)
        logging.info("metric",run.get_metrics())
      #  run.download_files( prefix="./outputs/",output_paths=os.path.join('/amlfbp_outputs/'))
        return args
    else :
    #except Exception as err :
        logging.error(err)
        response=""
        while response not in ["Y","N"]:
            response=input("amlfbp failed, do you want to keep the config? (Y/N) ")
        if response=="Y":
            return args
        else :
            return None

