from urllib import request, error
from datetime import datetime
import shutil
import errno
import json
import os


# Prints error message to user when caught
def err_log(error):
    date = str(datetime.utcnow())
    errmsg = '[' + date + '] ' + str(error) + ' occurred.'
    print(errmsg)


# Creates directory, ignores 'already exists' errors
def create_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            err_log(e)
            raise


# Creates a URL based on user given criteria and page number
def url_builder(criteria, pages=0):
    url = 'https://www.xeno-canto.org/api/2/recordings?query='
    url_list = []
    for val in criteria:
        url += val + '%20'
    if pages != 0:
        for i in range(1, pages + 1):
            url_temp = url + '&page=' + str(i)
            url_temp = url_temp.replace(' ', '')
            url_list.append(url_temp)
        return url_list
    else:
        return url


# Retrieve JSON based on search criteria
def get_json(search):
    json_list = []

    # Check response with search criteria to determine number of response pages
    url = url_builder(search)
    try:
        r = request.urlopen(url)
    except error.HTTPError as e:
        err_log(e)
        raise
    data = json.loads(r.read().decode('UTF-8'))
    num_pages = data["numPages"]

    # Creating folder structure from search criteria
    name = url[50:-1]
    for re in (('%20', '_'), ('%2', ''), (':', '|')):
        name = name.replace(*re)
    folder = os.getcwd() + '/queries/' + name
    create_dir(folder)
    temp_txt = folder + '/temp.txt'

    # Parsing through and saving each page
    url_list = url_builder(search, pages=int(num_pages))
    page = 1
    for url in url_list:
        try:
            r = request.urlopen(url)
        except error.HTTPError as e:
            err_log(e)
            continue
        data = json.loads(r.read().decode('UTF-8'))
        txt = open(temp_txt, 'w+')
        json.dump(data, txt)
        txt.close()
        file_name = folder + '/page' + str(page) + '.json'
        os.rename(temp_txt, file_name)
        json_list.append(file_name)
        page += 1

    # Returns a string list of paths for downloaded files
    return json_list


# Retrieves recording based on list of downloaded JSON file paths
def get_mp3(paths):
    # Creating folder structure and reserving temp path
    folder = os.getcwd() + '/recordings/'
    mp3_list = []
    create_dir(folder)
    temp_mp3 = folder + 'temp.mp3'

    # Parsing all JSON files for download links and executing them
    for file in paths:
        json_file = open(file)
        data = json.load(json_file)
        json_file.close()

        for i in range(0, int(data["numRecordings"])):
            rec_path = (str(folder) +
                        data["recordings"][i]["en"].replace(' ', '') +
                        '_' + data["recordings"][i]["id"] + '.mp3')

            if (os.path.exists(rec_path)) is False:
                url = 'https:' + data["recordings"][i]["file"]
                try:
                    r = request.urlopen(url)
                except error.HTTPError as e:
                    err_log(e)
                    continue
                mp3_data = r.read()
                mp3 = open(temp_mp3, 'wb')
                mp3.write(mp3_data)
                mp3.close
                os.rename(temp_mp3, rec_path)
                mp3_list.append(rec_path)
                
    # Returns string list of downloaded recording file paths
    return mp3_list


# Combines get_json and get_mp3 for convenience
def get_rec(search):
    json_list = get_json(search)
    mp3_list = get_mp3(json_list)

    # Returns string lists of get_json and get_mp3 respectively
    return [json_list, mp3_list]


# Scan directory for track id and write if found                               
def scan_dir(directory, id_list, write_list):
    dir_temp = directory.replace(' ', '_')
    ilist = os.scandir(dir_temp)                                  
    for item in ilist:                                                        
                                                                               
        # Scan if item is a directory                                          
        if item.is_dir():                                                   
            scan_dir(item.path, id_list, write_list)                                                
        else:                                                                  
            odata = open(item.path)                                            
            jdata = json.load(odata)                                           

            for id_num in id_list:                                                                   
                for j in range(0, len(jdata["recordings"])):                        
                    if id_num == jdata["recordings"][j]["id"]:
                        track_id = jdata["recordings"][j]["id"]
                        species_j = jdata["recordings"][j]["gen"] + ' ' + jdata["recordings"][j]["sp"]
                        if jdata["recordings"][j]["ssp"] != '':
                            species_j += ' ' + jdata["recordings"][j]["ssp"]
                        species_j = species_j.replace('"', '')
                        write_list.append('{"id":' + track_id + ', "species":"' + species_j + '"}')
    return write_list

# Generate a metadata file for given library path
# TODO: Ensure consistent naming for gen, sp, and ssp tags
def gen_meta(path=os.getcwd() + '/recordings/'):
    id_list = list()
    write_list = list()
    scan_list = os.scandir(path)                                               
                                                                               
    for scans in scan_list:                                                    
        filename = scans.name                                                  
        split_one = filename.split('_')
        split_two = split_one[1].split('.')
        ident = split_two[0]
        id_list.append(ident)                                                  
                                                                               
    # Scan queries path for track ids                              
    scan_string = scan_dir(os.getcwd() + '/queries/', id_list, write_list)
    meta_data = open('temp.txt', 'w+')
    meta_data.write('[' + ','.join(scan_string) + ']')
    meta_data.close()
    os.rename('temp.txt', 'metadata.json')


# TODO: Sort metadata by tag
