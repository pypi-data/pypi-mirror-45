from azureml.core import run
import azureml.core
from azureml.core import Experiment
from azureml.core import Workspace
import logging
from code_process import *
from config import config

def do_stuff(args):
    ## FUNCTION THAT DOES THE TRAINING GIVEN THE ARGS AND USING THE HELPERS/CODE_PROCESS
    #try :
    if True :
        experiment_name,project_folder,script,framework,cluster_name,storage_account,storage_key,storage_path,data,dependencies,vm_size,max_nodes,script_params=args["experiment_name"],args["project_folder"],args["script"],args["framework"],args["cluster_name"],args["storage_account"],args["storage_key"],args["storage_path"],args["data"],args["dependencies"],args["vm_size"],args["max_nodes"],args["script_params"]
        import shutil
        import os
        logging.info(args)

        ### LOADING THE TRAIN FILE ###
        if script is None :
            script=input(" training file : ")
            args["script"]=script
        else:
            logging.info("launching the training of : "+str(script))
        
        #transforming script into the filename and the dirname
        script=os.path.abspath(script)
        args["script"],args["project_folder"]=os.path.basename(script),os.path.dirname(script)


        # LOADING/CREATING THE PROJECT FOLDER
        if project_folder is None :
            project_folder=args["project_folder"]
            print("working in undeclared folder",project_folder)
        else :
            if project_folder!=os.path.dirname(os.path.abspath(script)):
                logging.warning("working directory is not where the script is referenced, will copy it here")
                shutil.copy(script, project_folder)
            else :
                os.makedirs(project_folder, exist_ok=True)
    
            logging.info("working in folder "+str(project_folder))

        
        ### LOADING THE WORKSPACE ###

        logging.info("starting aml settings..")
        from azureml.core.compute import ComputeTarget, AmlCompute
        try :
            ws = Workspace.from_config()
            logging.info("workspace already created, loading the workspace")
            if cluster_name is None :
                logging.info("hey let's select a random cluster ! (no cluster specified)")
                cluster_name = [k for k in ws.compute_targets.keys()][0]
                logging.info("it worked ! we selected : "+str(cluster_name))
            try:
                cluster = ComputeTarget(workspace=ws, name=cluster_name)
            except ComputeTargetException:
                compute_config = AmlCompute.provisioning_configuration(vm_size=vm_size,max_nodes=max_nodes)
                cluster = ComputeTarget.create(ws, cluster_name, compute_config)

        except Exception as err :            
            logging.exception(err)
            
            ws,cluster_name=config(args)
            cluster = ComputeTarget(workspace=ws, name=cluster_name)        
    
        ### LOADING THE EXPERIMENT ###
        from azureml.core import Experiment
        if experiment_name is None :
            experiment_name=input(" experiment name (>4 characters) : ")
            args["experiment_name"]=experiment_name
        else : 
            logging.info("working on experiment : "+str(experiment_name ))

        if experiment_name not in ws.experiments.keys() :
            logging.info("this experiment did not exist before, we are creating it")
        experiment = Experiment(workspace = ws, name = experiment_name)
        
        ### LINKING THE DATA ###
        #TODO if the data is local, then upload it to a blob
        from azureml.core import Datastore
        if data is None or data=="" :
            data=input("please enter the url to your data (full url with blob and container), or pass if your script has no data : ")
            args["data"]=data
            if data !="":
                a,b=check_data_url(data)
                while a is None :
                    logging.error("data url error"+str(b))
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

                script_params["--data_folder"]=ds.as_mount()
               
    
        ### DOING THE TRAINING based on the framework
        if dependencies is None :
            packages=get_dependencies(os.path.join(project_folder,script))
        logging.info("dependencies to install : "+str(packages))
        
        if framework is None:
            framework = autodetect_framework(script).lower()
            logging.info("autodetected framework : "+str(framework))
        else :
            framework=framework.lower()
            logging.info("you specified the framework : "+str(framework))
        
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
            logging.warning("didn't detect PyTorch, Tensorflow, or Chainer. If you are working with those, please input it as --framework (pytorch/tensorflow/chainer)")  
            from azureml.train.estimator import Estimator
            print("parameters of the training : ",project_folder,os.path.basename(script))
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
        logging.info("metric"+str(run.get_metrics()))
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

