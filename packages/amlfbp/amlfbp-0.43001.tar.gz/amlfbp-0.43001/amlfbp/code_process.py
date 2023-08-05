import logging

def autodetect_framework(script):
    # script : path to the script of which we want to detect the framework

    with open(script,"rb") as file :
        data=file.read().decode("utf8").lower()
    if "torch" in data:
        return "PyTorch"
    elif "tensorflow" in data:
        return "TensorFlow"
    elif "chainer" in data:
        return "Chainer"
    else : 
        return "Estimator"

def check_data_url(url):
    #function that converts the url of a blob data into the storage name and the folder path
    #also checks a few possible url defaults
    if url.split(":")[0]!="https":
        return None, "not an url"
    elif "." in url.split("/")[len(url.split("/"))-1]:
        return None, "not a folder"
    elif "blob.windows.core" not in url:
        return None, "not in a blob. Only blob storage is supported for online data"
    else :
        try :
            fullpath=url.replace("https://","")
            storage_account=fullpath.split("/")[0].split(".")[0]
            storage_path=fullpath.replace(fullpath.split("/")[0],"")
            return storage_account,storage_path
        except:
            return None, "unknown data path error. \"data\" should look like https://mystorage.blob.core.windows.net/myfolder"


def get_dependencies(myscript):
    # lists the needed packages from a given file. does not get second level dependencies
    to_ignore=["time","","__future__","random","__future__","sys","re","collections","distutils","os","urllib","urllib2","gzip","argparse","logging"]
    to_replace={"sklearn":"scikit-learn","torch":"torchvision","pytorch":"torchvision","optparse":"optparse_gui"}
    dependencies=[]
    with open(myscript,"rb") as file :
        data=file.read().decode("utf8").lower()
    if data is None :
        print("failure",data)
        return []
    lines=data.replace("\r","").split("\n")
    for line in lines :
        if ("import " in line) and (line is not None) and ("#" not in line) :
            words=[k.split(".")[0] for k in line.split(" ") if len(k)>1]
            dependencies.append(words[1])
    result=[]
    for dependency in dependencies :
       
        if dependency in to_replace.keys() :
            if not(to_replace[dependency] in result) :
                result.append(to_replace[dependency])
        else :
            if (not (dependency in to_ignore)) and (not(dependency in result)):            
                result.append(dependency)
        
    return result
