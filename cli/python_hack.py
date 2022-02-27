import requests
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def uploadCSV(argv_file):
    try:
        url = 'http://127.0.0.1:9103/backend/uploadCSV'
        file = {'file': open(argv_file)}
        r = requests.post(url, files=file)
        if r.status_code == 200:
            print("{ status: " + bcolors.OKGREEN + "'OK'" + bcolors.ENDC + " }")
            print('The file was uploaded and the database was successfully populated with the new data!')
        else:
            print(bcolors.FAIL + "Error: " + bcolors.ENDC + "Something went wrong")
    except:
        print(bcolors.WARNING + "Error: " + bcolors.ENDC + "Wrong input or server is down")

if sys.argv[1] == "upload":
    uploadCSV(sys.argv[2])


