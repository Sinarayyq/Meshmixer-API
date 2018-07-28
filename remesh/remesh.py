
# selection examples:
#   - list selected objects
#   - list selected facegroups
#cdef public great_function(path):

import time
import os
import sys

import win32ui

#import psutil



def WindowExists(classname):
   p = os.popen('tasklist /FI "IMAGENAME eq %s"' % classname) 
   if p.read().count(classname) :
       return True
   else:
       return False


def main():
    env_dist = os.environ
    apipath = env_dist.get('ITF')
    home_dir1 = apipath + "\\Surface_approximation\\meshmixer_API\\python"
    home_dir2 = apipath + "\\Surface_approximation\\meshmixer_API\\distrib\\python"
  
    sys.path.append(home_dir2)
    sys.path.append(home_dir1)

    fname = apipath + "\\Surface_approximation\\Input Parameters.txt"
    with open(fname, 'r') as f:  
        lines = f.readlines() 
        last_line = lines[-1]   



    #print(sys.path)

    import mmapi
    import platform
    import socket
    from mmRemote import *
    import mm
    import math
    import shutil




    # initialize connection
    remote = mmRemote()
    remote.connect()
    examples_dir = os.getcwd()
    cmd = mmapi.StoredCommands()



    path = apipath + "\\Surface_approximation\\Examples\\Intermediate"
    if os.path.isdir(path+"/remesh"):  #check if the folder exists
        shutil.rmtree(path+"/remesh")  #if it exists, delete it
    os.mkdir(path+"/remesh")           #if it's not, build it


    if not os.path.exists(path+"/stl"):
        print("No stl folder in /Surface_approxiamtion/Examples/Intermediate")
        print("We will now build it automaticly for you")
        os.mkdir(path+"/stl") 


    files = os.listdir(path+"/stl")    #read names of all stl files
    #print(files)
    if files==[]:
        print("No stl files in folder(/Surface_approxiamtion/Examples/Intermediate/stl/)")
        print("You should close this window, click the preprocess button and then remesh button")
        time.sleep(1000)
        os._exit(0)

    for file in files:
        input_file = path+"/stl"+"/"+file
        print(input_file)
        output_file1 = path+"/remesh"+"/"+file
        output_file = output_file1[:-3]
        output_file += "obj"
        #str_list = list(output_path)
        #nPos = str_list.index('.')
        #str_list.insert(nPos,'_remesh')
        #output_path = "".join(str_list)
        print(output_file)
        key = cmd.AppendSceneCommand_AppendMeshFile(input_file)
        remote.runCommand(cmd)
    

        #build remesh parameters EdgeLength
        mm.tool.begin_tool(remote,"stability")
        area = mm.tool.get_toolparam(remote,"surfaceArea")
        mm.tool.accept_tool(remote)
        #a = area
        length = math.sqrt(area/3600)
        length /= 2
        #print(sys.argv[0])
        #last_line = last_line[1:-1]
        #print(last_line)
        
        parameter = float(last_line)
        #print(parameter)
        length *= parameter
        #print(length)
        #length *= 0.0021
        #print("area:"+ area)
   
        #start remeshing
        selected_objects_all = mm.select_all(remote)
        mm.tool.begin_tool(remote,"remesh")
        mm.tool.set_toolparam(remote, "edgeLength", length)
        mm.tool.set_toolparam(remote, "boundaryMode", 2)  # 0:freeboundary; 1:fixedboundary; 2:refinedfixedboudary
        mm.tool.set_toolparam(remote, "goalType", 2)  # RelativeDensity = 0, AdaptiveDensity = 1, TargetEdgeLength = 2, LinearSubdivision = 3
        cmd.AppendCompleteToolCommand
        mm.tool.accept_tool(remote)   
        mm.scene.export_mesh(remote, output_file)  #build remeshed stl file
        #print(mm.scene.get_vertex_count(remote, selected_objects_all))
        #str_list = list(input_path)
        #nPos = str_list.index('.')
        #str_list.insert(nPos,'_remesh')
        #output_path = "".join(str_list)
        #input_path = raw_input("Enter Filename: ")
    time.sleep(5)
    remote.shutdown()




if __name__ == '__main__':
    print("Please keep this window open")    
    while not WindowExists("meshmixer.exe"):
        time.sleep(3)
        print("Wait till meshmixer.exe starts")
        
    time.sleep(2)
    #import mmapi
    print("Remeshing:")
    main()
    print("Finish remeshing.")
    print("Now you can close this window and then click iRANSAC button")
    time.sleep(1000)
    os._exit(0)

    


    
