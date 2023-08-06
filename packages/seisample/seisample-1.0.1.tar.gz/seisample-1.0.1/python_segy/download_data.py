# -*- coding: UTF-8 -*-

import urllib3
import os
import shutil
import gzip
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def Download_data(root,datasets="Hess_VTI"):
    '''
    download the .segy file from the internet
    Args:
        root: the .segy file exists or will be saved to if download is set to True.
        datasets : name of the dataset if download is set to True.

    '''

    if datasets=="Hess_VTI":

        download_list=[
            "https://s3.amazonaws.com/open.source.geoscience/open_data/hessvti/timodel_c11.segy.gz",
            "https://s3.amazonaws.com/open.source.geoscience/open_data/hessvti/timodel_c13.segy.gz", 
            "https://s3.amazonaws.com/open.source.geoscience/open_data/hessvti/timodel_c33.segy.gz", 
            "https://s3.amazonaws.com/open.source.geoscience/open_data/hessvti/timodel_c44.segy.gz"
                ]


    if datasets=="BP_1994":

        download_list=[
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_0201_0329.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_0331_0599.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_0601_0869.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_0871_1139.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_1141_1409.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_1411_1679.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7m_shots_1681_1949.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpstatics94/7o_5m_final_vtap.segy.gz" 
                ]

    if datasets=="BP_2004":

        download_list=[
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots0001_0200.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots0201_0400.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots0401_0600.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots0601_0800.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots0801_1000.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots1001_1200.segy.gz" ,
            "http://s3.amazonaws.com/open.source.geoscience/open_data/bpvelanal2004/shots1201_1348.segy.gz" 
                ]



    for i in range(len(download_list)):
        url = download_list[i]        
        
        gz_filename = url.split("/")[-1]
        
        filename = gz_filename.replace(".gz","")
        
        gz_file_path = os.path.join(root, gz_filename)
        
        file_path = os.path.join(root, filename)
        #download and unzip
        if not os.path.exists(file_path):
            if not os.path.exists(gz_file_path):
                print('[%d/%d] downloading %s to %s'
                      % (i+1,len(download_list),download_list[i],file_path))
                
                r = requests.get(url, stream=True, verify=False)
                total_size = int(r.headers['Content-Length'])
                temp_size = 0
                with open(gz_file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            temp_size += len(chunk)
                            f.write(chunk)
                            f.flush()
                            #############downloading progress###############
                            done = int(50 * temp_size / total_size)
                            sys.stdout.write("\r[%s%s] %d%%" % ('#' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                            sys.stdout.flush()
                print()                            
                    
                with gzip.open(gz_file_path, 'rb') as read, open(file_path, 'wb') as write:
                    shutil.copyfileobj(read, write)
            else:

                print('%s already exists' % (filename))
                with gzip.open(gz_file_path, 'rb') as read, open(file_path, 'wb') as write:
                    shutil.copyfileobj(read, write)
        else:
            print('%s already exists' % (filename))
    print("download finished")
