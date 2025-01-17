import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path:str ) -> dict: # returning type dictionary coz in schmea all columns are in dictionary type
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def write_yaml_file(file_path:str,content:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as fileobj:
            yaml.dump(content,fileobj)


    except Exception as e:
        raise NetworkSecurityException(e,sys)
def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numpy array data to file
    file_path: str location of file to save
    array:np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb")  as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def save_object(file_path:str,obj:object):
    try:
         os.makedirs(os.path.dirname(file_path),exist_ok=True)
         with open(file_path,"wb") as fileobj:
          pickle.dump(obj,fileobj) # you can also use dill.dump , both are for same use

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

   
