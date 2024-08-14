import os
import subprocess

PATH = os.path.abspath(os.curdir)  # thange this path if you want to inspect another directory
REQUIREMENTS_FILENAME = "general_requirement.txt"
SEARCH_FILENAME = "requirements.txt"

def find(name: str="requirements.txt", path: str=os.curdir):
    '''
    Traverse files and directories for given path to look for 
    individual requirements.txt.
    Return the list of relative paths to requirements.txt files.
    
    '''
    dirs = [path]
    paths_requirements = []
    while dirs != []:
        for root, dirs, files in os.walk(path):
            if name in files:
                paths_requirements.append(os.path.join(root, name))
            
    return paths_requirements
        
def join_requirements(path_req_general, 
                      paths_req_general: list=[]):
    '''
    Append the general requirements.txt file in giver directory 
    with all the requirements from all the files found.
    The general file is appended in place, nothing is returned.
    
    '''
    file_req_general = open(path_req_general, "r")
    write_req_general = open(path_req_general, "a")
    try:
        existing_reqs = file_req_general.readlines()
        for i in range(len(existing_reqs)):
            existing_reqs[i] = existing_reqs[i].strip()
    except:
        print("empty")
        existing_reqs = []
        
    for path in paths_req_general:
        with open(path, "r") as file:
            for line in file.readlines():
                line = line.strip()
                if line not in existing_reqs: 
                    write_req_general.write(f"{line}\n")
                    print(f"'{line}'")
                    existing_reqs.append(line)
                    print(f"{line} requirement added to the list")
                else: print(f"{line} requirement already exists -> skipping")
                
def install_requirements(path_req_general: str=os.path.join(os.curdir, "general_requirement.txt")):
    '''
    Execute the installation of all the requirements from 
    general requirements.txt file using pip install command in cmd.
    
    '''
    p1 = subprocess.Popen(["pip", "install", "-r", path_req_general])
    exit_codes = p1.wait()
    return exit_codes

def main():
    '''
    This programm installs all the packages from 
    all the requirements.txt files found in every directory in PATH.
    
    '''

    # opening/creating the requirements file to append it
    path_req_general = os.path.join(os.path.abspath(os.curdir), REQUIREMENTS_FILENAME)
    file_req_general = open(path_req_general, "a")

    paths_requirements_list = find(SEARCH_FILENAME, PATH)
    join_requirements(path_req_general, paths_requirements_list)
    exit_codes = install_requirements(path_req_general)
    # os.remove(path_req_general)
    
    
if __name__ == "__main__":
    main()