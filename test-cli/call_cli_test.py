import subprocess

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

#http://localhost:8000/interoperability/api/PassesPerStation/GF00/20230101/20230104
passesperstation_cli_call = ['se2101', 'passesperstation', '--station', 'GF00', '--datefrom', '20230101', '--dateto', '20230104']
passesperstation_cli_call_expected = "{ Station: 'GF00',  StationOperator: 'GF',  RequestTimestamp: '2022-02-24 14:34:23',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 10,  PassesList:   [ { PassIndex: 0,       PassID: '1000000015',       PassTimeStamp: '2023-01-01 12:23:00',       VevicleID: 'PF04UCA93312',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 3.1 },     { PassIndex: 1,       PassID: '1000000016',       PassTimeStamp: '2023-01-01 12:45:00',       VevicleID: 'IO09FGE68100',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.8 },     { PassIndex: 2,       PassID: '1000000030',       PassTimeStamp: '2023-01-02 03:30:00',       VevicleID: 'JE65QJK64802',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.8 },     { PassIndex: 3,       PassID: '1000000033',       PassTimeStamp: '2023-01-02 04:28:00',       VevicleID: 'QO68DIC93032',       TagProvider: 'MR',       PassType: 'visitor',       PassCharge: 13 },     { PassIndex: 4,       PassID: '1000000034',       PassTimeStamp: '2023-01-02 05:50:00',       VevicleID: 'DO24BCW15511',       TagProvider: 'KO',       PassType: 'visitor',       PassCharge: 13 },     { PassIndex: 5,       PassID: '1000000051',       PassTimeStamp: '2023-01-02 21:13:00',       VevicleID: 'BY85QGR11636',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.5 },     { PassIndex: 6,       PassID: '1000000056',       PassTimeStamp: '2023-01-03 01:40:00',       VevicleID: 'IO09FGE68100',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.8 },     { PassIndex: 7,       PassID: '1000000069',       PassTimeStamp: '2023-01-03 09:23:00',       VevicleID: 'CK97FAU13897',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.5 },     { PassIndex: 8,       PassID: '1000000071',       PassTimeStamp: '2023-01-03 12:20:00',       VevicleID: 'YX66XYW62640',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 3.1 },     { PassIndex: 9,       PassID: '1000000078',       PassTimeStamp: '2023-01-03 19:31:00',       VevicleID: 'MP14WFM40909',       TagProvider: 'GF',       PassType: 'home',       PassCharge: 2.8 } ] }"

#http://localhost:8000/interoperability/api/PassesCost/AO/OO/20230101/20230104
passescost_cli_call = ['se2101', 'passescost', '--op1', 'AO', '--op2', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
passescost_cli_call_expected = "{ op1_ID: 'AO',  op2_ID: 'OO',  RequestTimestamp: '2022-02-24 15:12:14',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 1,  PassesCost: 2 }"

#http://127.0.0.1:8000/interoperability/api/PassesAnalysis/KO/OO/20230101/20230104
passesanalysis_cli_call = ['se2101', 'passesanalysis', '--op1', 'KO', '--op2', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
passesanalysis_cli_call_expected = "{ op1_ID: 'KO',  op2_ID: 'OO',  RequestTimestamp: '2022-02-24 15:21:52',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 1,  PassesList:   [ { PassIndex: 0,       PassID: '1000000086',       StationID: 'WY00MLL63827',       TimeStamp: '2023-01-03 23:11:00',       VevicleID: 'WY00MLL63827',       Charge: 2.8 } ] }"

#http://localhost:8000/interoperability/api/ChargesBy/OO/20230101/20230104
chargesby_cli_call = ['se2101', 'chargesby', '--op1', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
chargesby_cli_call_expected = "{ op_ID: 'OO',  RequestTimestamp: '2022-02-24 15:27:50',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  PPOList:   [ { VisitingOperator: 'KO', NumberOfPasses: 1, PassesCost: 2.8 },     { VisitingOperator: 'AO', NumberOfPasses: 1, PassesCost: 2 },     { VisitingOperator: 'GF', NumberOfPasses: 1, PassesCost: 2.5 } ] }"

reset_passes_cli_call = ['se2101', 'resetpasses']
reset_passes_cli_call_expected = "{ status: 'OK' }"

reset_stations_cli_call = ['se2101', 'resetstations']
reset_stations_cli_call_expected = "{ status: 'OK' }"

reset_vehicles_cli_call = ['se2101', 'resetvehicles']
reset_vehicles_cli_call_expected = "{ status: 'OK' }"

healthcheck_cli_call = ['se2101', 'healthcheck']
healthcheck_cli_call_expected = "{ status: 'OK',  dbconnection: 'BM25PHF40639ekjejuwn34553JSQ0002840' }"


def passes_per_station_cli_test():
    process = subprocess.run(passesperstation_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response[0:42] + response[85:-1] == passesperstation_cli_call_expected[0:42] + passesperstation_cli_call_expected[85:-1]:
        print(bcolors.OKGREEN + '.Testcase 1 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 1 failed ' + bcolors.ENDC + 'X')

def passes_cost_cli_test():
    process = subprocess.run(passescost_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response[0:30] + response[72:-1] == passescost_cli_call_expected[0:30] + passescost_cli_call_expected[72:-1]:
        print(bcolors.OKGREEN + '.Testcase 2 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 2 failed ' + bcolors.ENDC + 'X')

def passes_analysis_cli_test():
    process = subprocess.run(passesanalysis_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response[0:30] + response[72:-1] == passesanalysis_cli_call_expected[0:30] + passesanalysis_cli_call_expected[72:-1]:
        print(bcolors.OKGREEN + '.Testcase 3 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 3 failed ' + bcolors.ENDC + 'X')

def charges_by_cli_test():
    process = subprocess.run(chargesby_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response[0:14] + response[56:-1] == chargesby_cli_call_expected[0:14] + chargesby_cli_call_expected[56:-1]:
        print(bcolors.OKGREEN + '.Testcase 4 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 4 failed ' + bcolors.ENDC + 'X')

def reset_passes_cli_test():
    process = subprocess.run(reset_passes_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response == reset_passes_cli_call_expected:
        print(bcolors.OKGREEN + '.Testcase 5 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 5 failed ' + bcolors.ENDC + 'X')

def reset_stations_cli_test():
    process = subprocess.run(reset_stations_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response == reset_stations_cli_call_expected:
        print(bcolors.OKGREEN + '.Testcase 6 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 6 failed ' + bcolors.ENDC + 'X')

def reset_vehicles_cli_test():
    process = subprocess.run(reset_vehicles_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response == reset_vehicles_cli_call_expected:
        print(bcolors.OKGREEN + '.Testcase 7 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 7 failed ' + bcolors.ENDC + 'X')

def healthcheck_cli_test():
    process = subprocess.run(healthcheck_cli_call, capture_output=True)
    response = process.stdout.decode('ascii').replace('\n', '')
    if response == healthcheck_cli_call_expected:
        print(bcolors.OKGREEN + '.Testcase 8 passed ' + bcolors.ENDC + u'\N{check mark}')
    else:
        print(bcolors.FAIL + '.Testcase 8 failed ' + bcolors.ENDC + 'X')