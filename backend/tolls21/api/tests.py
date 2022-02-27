import json
from django.test import TestCase
import csv
from api.models import driver, provider, vehicle, station, pass_event
from datetime import date, datetime
from django.utils.timezone import make_aware
import os
from django.contrib.auth.models import User
import requests
import subprocess

provider_names = ["aodos", "gefyra", "egnatia", "kentriki_odos", "moreas", "nea_odos", "olympia_odos"]
provider_abbr = ["AO", "GF", "EG", "KO", "MR", "NE", "OO"]
fullnames = ['Carlisle Bridgeman', 'Yashvi Waldner', 'Cing Abeyta', 'Rori Nolen', 'Belinda Stearns', 'Jaila Homer', 'Kaavya Hobart', 'Roslyn Mcdonnell', 'Leeana Hathcock', 'Shulem Pagel', 'Swara Wooldridge', 'Tiffany Archer', 'Nellie Boles', 'Alexi Hoyer', 'Lisette Bernardo', 'Blair Reyna', 'Jaymes Kingery', 'Illyana Raygoza', 'Fox Lo', 'Jaida Roper', 'Roman Nichols', 'Bernard Robert', 'Karlei Fasano', 'Jaina Quinlan', 'Daegan Markus', 'Ivyana Pendley', 'Kolton Dodson', 'Karolina Sage', 'Blakeleigh Kao', 'Julieth Thornhill', 'Brantlee Yee', 'Kalie Karl', 'Tirzah Pine', 'Makai Rosen', 'Gwynn Lafave', 'Haden Riedel', 'Henley Cosgrove', 'Reyansh Ocampo', 'Omega Bixby', 'Kiyan Brockman', 'Derek Daniel', 'Zadok Kessinger', 'Levy Barner', 'Mihika Rothwell', 'Avi Humble', 'Lainee Kamp', 'Dereck Noriega', 'Brihanna Wester', 'Rubin Cespedes', 'Sia Whelan', 'Sunshine Milne', 'Lion Minard', 'Tamya Gurrola', 'Lysander Gaeta', 'Arien Chafin', 'Alexandre Harter', 'Kailea Hinckley', 'Jeancarlo Mcanally', 'Raelyn Stafford', 'Brittany Booker', 'Francisca Cannady', 'Kylah Rader', 'Finlay Flagg', 'Mirielle Wethington', 'Aaditya Agustin', 'Alexxa Schuman', 'Yehuda Hare', 'Adelynne Tillery', 'Brentlee Worthy', 'Kenzleigh Logue', 'Reyna Battle', 'Mohamed Spence', 'Jaelyn Mckibben', 'Dwight Shay', 'Fayth Scanlan', 'Keilly Konrad', 'Rayleigh Lorenzo', 'Blessin Jepson', 'Eduard Maines', 'Railynn Brodie', 'Stryker Horowitz', 'Shaelyn Wilhite', 'Tanvi Sanborn', 'Jalil Callender', 'Analeah Scholl', 'Kalin Paynter', 'Aseel Fritts', 'Calix Mcelveen', 'Lloyd Malcolm', 'Tytus Tilton', 'Blessyn Mertens', 'Kale Moya', 'Bryar Wick', 'Braden Fry', 'Kenzy Maupin', 'Paxson Lesher', 'Rowdy Troutman', 'Cory Gary', 'Ivy Alvarado', 'Azalea Whitfield']
phones = [9465033583, 6893799017, 9403383928, 6870995375, 9441657173, 6899355016, 9407028030, 6954968427, 6889611443, 6852385489, 6885674558, 6856125474, 6858444220, 6995757282, 6983321241, 6889179453, 9482162940, 6874642614, 6874726698, 6896964208, 6854505607, 9490901323, 6887882555, 6951892024, 6851012502, 9413084944, 9411809542, 9468640211, 6890689268, 9443225053, 6930098655, 9426725149, 9489688398, 6985804596, 9423880800, 9481828515, 6852316164, 6871469450, 6885197490, 6886329785, 6852887853, 6889191968, 6973118718, 6876402036, 6874180833, 6856068214, 6923573821, 6898761571, 6968492033, 6873008140, 9451481267, 6877281944, 6879533298, 6858089632, 6853814765, 6932704272, 9403589323, 6851649491, 6893121684, 6891550396, 6875774469, 6873182100, 6879323261, 9431255662, 9489803783, 6871081631, 6940741811, 9408438939, 6883751101, 6899176792, 6986093738, 9489593533, 6871873237, 6874757516, 6874132146, 6851150062, 6890106801, 9487601718, 9446348829, 9433823611, 6871148979, 6885038695, 6883027476, 6916357625, 6896857265, 9487425272, 6850107654, 6890699751, 6872931814, 6937579392, 9494491906, 6980763558, 6874929573, 6930237261, 6897649424, 6885254386, 6880412484, 6853879397, 9442917346, 6996846810]
ssns = [689183116, 693412937, 690186447, 949080327, 689313147, 946200081, 691256895, 685861907, 948834476, 688624337, 693158599, 698057800, 689934643, 949797868, 697505654, 696734450, 685386694, 698475294, 685192756, 692145030, 941752892, 685007140, 942021886, 948302368, 687381542, 945739680, 688037635, 940190483, 691210720, 693162456, 689560194, 949142778, 694122512, 691365452, 688618285, 685533996, 690272881, 685993474, 691971386, 696689195, 948297317, 697383877, 689837748, 688367368, 949135996, 943329130, 691934039, 698986918, 944417428, 687347281, 699856008, 944153322, 941124585, 688859720, 691887857, 944899717, 949722793, 694629460, 944759796, 947662649, 697846490, 947665471, 940734353, 699839001, 689704982, 947321627, 687020466, 685356222, 689123461, 689947890, 694894880, 942669971, 685440178, 946404915, 691303730, 694446512, 685534772, 689887852, 699943405, 943456786, 948406344, 694159997, 691341375, 689957363, 945097370, 685478355, 689701913, 694182941, 945322000, 948139094, 946978022, 687395404, 948452010, 942618528, 685253335, 685223067, 699400644, 698464376, 693227493, 688343127]
birth_dates = [(1977, 5, 14), (2000, 3, 5), (1973, 5, 11), (1996, 12, 18), (1990, 4, 23), (1978, 4, 27), (1996, 1, 26), (1995, 2, 7), (2000, 5, 13), (2000, 2, 13), (1984, 4, 11), (1995, 11, 19), (1987, 12, 22), (1979, 1, 7), (1991, 2, 13), (1988, 1, 22), (1979, 6, 26), (1992, 2, 12), (1996, 9, 20), (1989, 5, 20), (1992, 3, 10), (1996, 11, 1), (1975, 9, 5), (1971, 11, 15), (1975, 9, 24), (1994, 10, 18), (1994, 9, 10), (1971, 5, 9), (1972, 11, 18), (1995, 1, 7), (1980, 12, 23), (1982, 5, 19), (1983, 1, 3), (1999, 2, 27), (1995, 9, 1), (1978, 12, 17), (1997, 1, 8), (1988, 11, 28), (1974, 5, 5), (1973, 11, 14), (1970, 7, 8), (1977, 5, 15), (1980, 1, 6), (1980, 9, 14), (1977, 6, 8), (1997, 5, 29), (1996, 1, 19), (1986, 9, 16), (1993, 11, 9), (1993, 12, 1), (1983, 10, 8), (1994, 9, 18), (1985, 1, 13), (1979, 2, 12), (1992, 10, 24), (1982, 10, 15), (1987, 11, 12), (1994, 7, 28), (1984, 11, 15), (1990, 7, 24), (1986, 11, 12), (1980, 6, 9), (1971, 2, 22), (1994, 1, 6), (1997, 3, 19), (1970, 12, 1), (1983, 10, 1), (1977, 5, 13), (1977, 9, 19), (1988, 3, 17), (1995, 4, 4), (1990, 2, 9), (1981, 7, 6), (1998, 3, 14), (1981, 11, 25), (1987, 1, 20), (1995, 11, 29), (1976, 4, 10), (1987, 2, 15), (1977, 8, 17), (1996, 9, 11), (1985, 5, 14), (1980, 2, 7), (1982, 5, 14), (1997, 5, 26), (1979, 11, 26), (1972, 2, 25), (1997, 10, 23), (1985, 8, 5), (1998, 4, 26), (1982, 4, 27), (1995, 9, 27), (1977, 10, 20), (1997, 7, 23), (1996, 3, 6), (1972, 4, 21), (1990, 5, 18), (1972, 9, 9), (1974, 7, 12), (1991, 5, 24)]


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

init_ran_already = False

def init():
    global init_ran_already
    if not init_ran_already:
        screen_clear()
        print(bcolors.OKCYAN + 'The testing process has started!' + bcolors.ENDC + '\n')
        init_ran_already = True

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def populate_users():
    for name in provider_names:
        if not User.objects.filter(username = name).exists():
            user = User.objects.create_user(username = name, password='test123')
            user.is_superuser = True
            user.is_staff = True
            user.save()

def populate_providers():
    populate_users()
    for name, abbr in zip(provider_names, provider_abbr):
        provider.objects.create(
            user_id = User.objects.get(username = name),
            provider_id = abbr,
            fullname = name
        )

def populate_stations():
    file = open('../../sample_data/sampledata01_stations.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        stationID       = strings[0]
        stationProvider = strings[1]
        stationName     = strings[2]
        station.objects.create(
            station_id = stationID,
            station_name = stationName,
            provider = provider.objects.get(fullname = stationProvider)
        )

def populate_vehicles():
    file = open('../../sample_data/sampledata01_vehicles_100.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        vehicleID = strings[0]
        tagID = strings[1]
        providerAbbr = strings[3]
        licenseYear = strings[4]
        vehicle.objects.create(
            vehicle_id = vehicleID,
            tag_id = tagID,
            provider = provider.objects.get(provider_id = providerAbbr),
            license_year = int(licenseYear)
        )

def populate_drivers():
    file = open('../../sample_data/sampledata01_vehicles_100.csv')
    reader = csv.reader(file)
    next(reader)
    for row, my_name, my_phone, my_date, my_ssn in zip(reader, fullnames, phones, birth_dates, ssns):
        strings = row[0].split(";")
        vehicleID = strings[0]
        driver.objects.get_or_create(
            first_name  = my_name.split(" ")[0],
            last_name   = my_name.split(" ")[1],
            phoneNo     = my_phone,
            birth_date  = date(my_date[0], my_date[1], my_date[2]),
            ssn         = my_ssn,
            vehicle     = vehicle.objects.get(vehicle_id=vehicleID)
        )

def populate_pass_events():
    file = open('../../sample_data/test.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        date = strings[1].split()[0].split("/")
        time = strings[1].split()[1].split(":")
        pass_event.objects.create(
            pass_id = strings[0],
            timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
            vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
            stationRef = station.objects.get(station_id=strings[2]),
            charge = float(strings[4])
        )

def populate_everything():
    populate_providers()
    populate_stations()
    populate_vehicles()
    populate_drivers()
    populate_pass_events()


class BackendTestCases(TestCase):
    def setUp(self):
        init()
        print(bcolors.OKCYAN + 'Now running backend tests' + bcolors.ENDC)
        populate_everything()

    def test_testcases(self):
        self.providers_true()
        self.providers_false()
        self.stations_true()
        self.stations_false()
        self.vehicles_true()
        self.vehicles_false()
        self.drivers_true()
        self.drivers_false()
        self.pass_events_true()
        self.pass_events_false()

    def providers_true(self):
        check = True
        for name, abbr in zip(provider_names, provider_abbr):
            try:
                object = provider.objects.get(provider_id = abbr)
                self.assertEqual(object.fullname, name)
            except:
                check = False
                break
        if check:
            print(bcolors.OKGREEN + '.Testcase 1 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 1 failed ' + bcolors.ENDC + 'X')

    # This testcase should fail so the testcase passes if it fails
    def providers_false(self):
        check = True
        try:
            object = provider.objects.get(provider_id = 'fail')
            self.assertEqual(object.fullname, 'fail')
        except:
            check = False
        if not check:
            print(bcolors.OKGREEN + '.Testcase 2 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 2 failed ' + bcolors.ENDC + 'X')

    def stations_true(self):
        check = True
        file = open('../../sample_data/sampledata01_stations.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            stationID       = strings[0]
            stationProvider = strings[1]
            try:
                object = station.objects.get(station_id = stationID)
                self.assertEqual(object.provider, provider.objects.get(fullname = stationProvider))
            except:
                check = False
                break
        if check:
            print(bcolors.OKGREEN + '.Testcase 3 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 3 failed ' + bcolors.ENDC + 'X')

    # This testcase should fail so the testcase passes if it fails
    def stations_false(self):
        check = True
        file = open('../../sample_data/sampledata01_stations.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            stationID       = strings[0]
            stationProvider = strings[1]
            try:
                object = station.objects.get(station_id = stationID)
                self.assertEqual(object.provider, provider.objects.get(fullname = 'fail'))
            except:
                check = False
                break
        if not check:
            print(bcolors.OKGREEN + '.Testcase 4 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 4 failed ' + bcolors.ENDC + 'X')

    def vehicles_true(self):
        check = True
        file = open('../../sample_data/sampledata01_vehicles_100.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            vehicleID = strings[0]
            tagID = strings[1]
            providerAbbr = strings[3]
            licenseYear = strings[4]
            try:
                object = vehicle.objects.get(
                    vehicle_id = vehicleID,
                    tag_id = tagID,
                    provider = provider.objects.get(provider_id = providerAbbr),
                    license_year = int(licenseYear)
                )
                self.assertEqual(object.provider, provider.objects.get(provider_id = providerAbbr))
            except:
                check = False
                break
        if check:
            print(bcolors.OKGREEN + '.Testcase 5 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 5 failed ' + bcolors.ENDC + 'X')

    # This testcase should fail so the testcase passes if it fails
    def vehicles_false(self):
        check = True
        file = open('../../sample_data/sampledata01_vehicles_100.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            vehicleID = strings[0]
            tagID = strings[1]
            providerAbbr = strings[3]
            licenseYear = strings[4]
            try:
                object = vehicle.objects.get(
                    vehicle_id = vehicleID,
                    tag_id = tagID,
                    provider = provider.objects.get(provider_id = providerAbbr),
                    license_year = int(licenseYear)
                )
                self.assertEqual(object.provider, provider.objects.get(provider_id = 'fail'))
            except:
                check = False
                break
        if not check:
            print(bcolors.OKGREEN + '.Testcase 6 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 6 failed ' + bcolors.ENDC + 'X')

    def drivers_true(self):
        check = True
        file = open('../../sample_data/sampledata01_vehicles_100.csv')
        reader = csv.reader(file)
        next(reader)
        for row, my_name, my_phone, my_date, my_ssn in zip(reader, fullnames, phones, birth_dates, ssns):
            strings = row[0].split(";")
            vehicleID = strings[0]
            try:
                object = driver.objects.get(
                    first_name  = my_name.split(" ")[0],
                    last_name   = my_name.split(" ")[1],
                    phoneNo     = my_phone,
                    birth_date  = date(my_date[0], my_date[1], my_date[2]),
                    ssn         = my_ssn,
                    vehicle     = vehicle.objects.get(vehicle_id=vehicleID)
                )
                self.assertEqual(object.vehicle, vehicle.objects.get(vehicle_id=vehicleID))
            except:
                check = False
                break
        if check:
            print(bcolors.OKGREEN + '.Testcase 7 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 7 failed ' + bcolors.ENDC + 'X')

    # This testcase should fail so the testcase passes if it fails
    def drivers_false(self):
        check = True
        file = open('../../sample_data/sampledata01_vehicles_100.csv')
        reader = csv.reader(file)
        next(reader)
        for row, my_name, my_phone, my_date, my_ssn in zip(reader, fullnames, phones, birth_dates, ssns):
            strings = row[0].split(";")
            vehicleID = strings[0]
            try:
                object = driver.objects.get(
                    first_name  = my_name.split(" ")[0],
                    last_name   = my_name.split(" ")[1],
                    phoneNo     = my_phone,
                    birth_date  = date(my_date[0], my_date[1], my_date[2]),
                    ssn         = my_ssn,
                    vehicle     = vehicle.objects.get(vehicle_id=vehicleID)
                )
                self.assertEqual(object.vehicle, vehicle.objects.get(vehivle = vehicle.objects.get(vehicle_id = 'fail')))
            except:
                check = False
                break
        if not check:
            print(bcolors.OKGREEN + '.Testcase 8 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 8 failed ' + bcolors.ENDC + 'X')

    def pass_events_true(self):
        check = True
        file = open('../../sample_data/test.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            date = strings[1].split()[0].split("/")
            time = strings[1].split()[1].split(":")
            try:
                object = pass_event.objects.get(
                    pass_id = strings[0],
                    timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
                    vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
                    stationRef = station.objects.get(station_id=strings[2]),
                    charge = float(strings[4])
                )
                self.assertEqual(object.vehicleRef, vehicle.objects.get(vehicle_id=strings[3]))
                self.assertEqual(object.stationRef, station.objects.get(station_id=strings[2]))
            except:
                check = False
                break
        if check:
            print(bcolors.OKGREEN + '.Testcase 9 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 9 failed ' + bcolors.ENDC + 'X')

    # This testcase should fail so the testcase passes if it fails
    def pass_events_false(self):
        check = True
        file = open('../../sample_data/test.csv')
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            strings = row[0].split(";")
            date = strings[1].split()[0].split("/")
            time = strings[1].split()[1].split(":")
            try:
                object = pass_event.objects.get(
                    pass_id = strings[0],
                    timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
                    vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
                    stationRef = station.objects.get(station_id=strings[2]),
                    charge = float(strings[4])
                )
                self.assertEqual(object.vehicleRef, vehicle.objects.get(vehicle_id='fail'))
                self.assertEqual(object.stationRef, station.objects.get(station_id='fail'))
            except:
                check = False
                break
        if not check:
            print(bcolors.OKGREEN + '.Testcase 10 passed ' + bcolors.ENDC + u'\N{check mark}' + '\n')
        else:
            print(bcolors.FAIL + '.Testcase 10 failed ' + bcolors.ENDC + 'X' + '\n')


testcase2 = {'op1_ID': 'KO', 'op2_ID': 'OO', 'PeriodFrom': '2023-01-01 00:00:00', 'PeriodTo': '2023-01-04 00:00:00', 'NumberOfPasses': 1, 'PassesList': [{'PassIndex': 0, 'PassID': '1000000086', 'StationID': 'WY00MLL63827', 'TimeStamp': '2023-01-03 23:11:00', 'VevicleID': 'WY00MLL63827', 'Charge': 2.8}]}
testcase3 = {'Station': 'GF00', 'StationOperator': 'GF', 'PeriodFrom': '2023-01-01 00:00:00', 'PeriodTo': '2023-01-04 00:00:00', 'NumberOfPasses': 10, 'PassesList': [{'PassIndex': 0, 'PassID': '1000000015', 'PassTimeStamp': '2023-01-01 12:23:00', 'VevicleID': 'PF04UCA93312', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 3.1}, {'PassIndex': 1, 'PassID': '1000000016', 'PassTimeStamp': '2023-01-01 12:45:00', 'VevicleID': 'IO09FGE68100', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.8}, {'PassIndex': 2, 'PassID': '1000000030', 'PassTimeStamp': '2023-01-02 03:30:00', 'VevicleID': 'JE65QJK64802', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.8}, {'PassIndex': 3, 'PassID': '1000000033', 'PassTimeStamp': '2023-01-02 04:28:00', 'VevicleID': 'QO68DIC93032', 'TagProvider': 'MR', 'PassType': 'visitor', 'PassCharge': 13.0}, {'PassIndex': 4, 'PassID': '1000000034', 'PassTimeStamp': '2023-01-02 05:50:00', 'VevicleID': 'DO24BCW15511', 'TagProvider': 'KO', 'PassType': 'visitor', 'PassCharge': 13.0}, {'PassIndex': 5, 'PassID': '1000000051', 'PassTimeStamp': '2023-01-02 21:13:00', 'VevicleID': 'BY85QGR11636', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.5}, {'PassIndex': 6, 'PassID': '1000000056', 'PassTimeStamp': '2023-01-03 01:40:00', 'VevicleID': 'IO09FGE68100', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.8}, {'PassIndex': 7, 'PassID': '1000000069', 'PassTimeStamp': '2023-01-03 09:23:00', 'VevicleID': 'CK97FAU13897', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.5}, {'PassIndex': 8, 'PassID': '1000000071', 'PassTimeStamp': '2023-01-03 12:20:00', 'VevicleID': 'YX66XYW62640', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 3.1}, {'PassIndex': 9, 'PassID': '1000000078', 'PassTimeStamp': '2023-01-03 19:31:00', 'VevicleID': 'MP14WFM40909', 'TagProvider': 'GF', 'PassType': 'home', 'PassCharge': 2.8}]}
testcase4 = {'op_ID': 'OO', 'PeriodFrom': '2023-01-01 00:00:00', 'PeriodTo': '2023-01-04 00:00:00', 'PPOList': [{'VisitingOperator': 'KO', 'NumberOfPasses': 1, 'PassesCost': 2.8}, {'VisitingOperator': 'AO', 'NumberOfPasses': 1, 'PassesCost': 2.0}, {'VisitingOperator': 'GF', 'NumberOfPasses': 1, 'PassesCost': 2.5}]}
testcase5 = {'op1_ID': 'GF', 'op2_ID': 'OO', 'PeriodFrom': '2023-01-01 00:00:00', 'PeriodTo': '2023-01-04 00:00:00', 'NumberOfPasses': 1, 'PassesCost': 2.5}
ok_status = {"status":"OK"}
healthcheck_ok_status = {'status': 'OK', 'dbconnection': 'BM25PHF40639ekjejuwn34553JSQ0002840'}

class APITestCases(TestCase):
    def setUp(self):
        init()
        print(bcolors.OKCYAN + 'Now running REST API tests' + bcolors.ENDC)

    def test_testcases(self):
        self.uploadCSV_test()
        self.passes_analysis_test()
        self.passes_per_station_test()
        self.charges_by_test()
        self.passes_cost_test()
        self.reset_passes_test()
        self.reset_vehicles_test()
        self.reset_stations_test()
        self.deleteCSV_test()
        self.healthcheck_test()

    def uploadCSV_test(self):
        url = 'http://127.0.0.1:9103/backend/uploadCSV'
        file = {'file': open('../../sample_data/test.csv', 'rb')}
        r = requests.post(url, files=file)
        if r.status_code == 200:
            print(bcolors.OKGREEN + '.Testcase 1 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 1 failed ' + bcolors.ENDC + 'X')

    def passes_analysis_test(self):
        r = requests.get('http://127.0.0.1:9103/interoperability/api/PassesAnalysis/KO/OO/20230101/20230104')
        save = r.json()
        save.pop('RequestTimestamp', None)
        #print(r.status_code)
        #print(save)
        if r.status_code == 200 and testcase2 == save:
            print(bcolors.OKGREEN + '.Testcase 2 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 2 failed ' + bcolors.ENDC + 'X')

    def passes_per_station_test(self):
        r = requests.get('http://localhost:9103/interoperability/api/PassesPerStation/GF00/20230101/20230104')
        save = r.json()
        save.pop('RequestTimestamp', None)
        #print(save)
        if r.status_code == 200 and testcase3 == save:
            print(bcolors.OKGREEN + '.Testcase 3 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 3 failed ' + bcolors.ENDC + 'X')

    def charges_by_test(self):
        r = requests.get('http://localhost:9103/interoperability/api/ChargesBy/OO/20230101/20230104')
        save = r.json()
        save.pop('RequestTimestamp', None)
        #print(save)
        #print(r.status_code)
        if r.status_code == 200 and testcase4 == save:
            print(bcolors.OKGREEN + '.Testcase 4 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 4 failed ' + bcolors.ENDC + 'X')

    def passes_cost_test(self):
        r = requests.get('http://localhost:9103/interoperability/api/PassesCost/GF/OO/20230101/20230104')
        save = r.json()
        save.pop('RequestTimestamp', None)
        #print(save)
        if r.status_code == 200 and testcase5 == save:
            print(bcolors.OKGREEN + '.Testcase 5 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 5 failed ' + bcolors.ENDC + 'X')

    def reset_passes_test(self):
        r = requests.post('http://127.0.0.1:9103/interoperability/api/admin/resetpasses')
        if r.status_code == 200 and r.json() == ok_status:
            print(bcolors.OKGREEN + '.Testcase 6 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 6 failed ' + bcolors.ENDC + 'X')

    def reset_vehicles_test(self):
        r = requests.post('http://127.0.0.1:9103/interoperability/api/admin/resetvehicles')
        if r.status_code == 200 and r.json() == ok_status:
            print(bcolors.OKGREEN + '.Testcase 7 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 7 failed ' + bcolors.ENDC + 'X')

    def reset_stations_test(self):
        r = requests.post('http://127.0.0.1:9103/interoperability/api/admin/resetstations')
        if r.status_code == 200 and r.json() == ok_status:
            print(bcolors.OKGREEN + '.Testcase 8 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 8 failed ' + bcolors.ENDC + 'X')

    def deleteCSV_test(self):
        r = requests.post('http://127.0.0.1:9103/backend/deleteCSV')
        if r.status_code == 200 and r.json() == ok_status:
            print(bcolors.OKGREEN + '.Testcase 9 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 9 failed ' + bcolors.ENDC + 'X')

    def healthcheck_test(self):
        r = requests.get('http://localhost:9103/interoperability/api/admin/healthcheck')
        save = r.json()
        #print(save)
        if r.status_code == 200 and healthcheck_ok_status == save:
            print(bcolors.OKGREEN + '.Testcase 10 passed ' + bcolors.ENDC + u'\N{check mark}' + '\n')
        else:
            print(bcolors.FAIL + '.Testcase 10 failed ' + bcolors.ENDC + 'X' + '\n')


#http://localhost:9103/interoperability/api/PassesPerStation/GF00/20230101/20230104
passesperstation_cli_call = ['se2101', 'passesperstation', '--station', 'GF00', '--datefrom', '20230101', '--dateto', '20230104']
passesperstation_cli_call_expected = "{  Station: 'GF00',  StationOperator: 'GF',  RequestTimestamp: '2022-02-26 21:27:24',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 10,  PassesList: [    {      PassIndex: 0,      PassID: '1000000015',      PassTimeStamp: '2023-01-01 12:23:00',      VevicleID: 'PF04UCA93312',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 3.1    },    {      PassIndex: 1,      PassID: '1000000016',      PassTimeStamp: '2023-01-01 12:45:00',      VevicleID: 'IO09FGE68100',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.8    },    {      PassIndex: 2,      PassID: '1000000030',      PassTimeStamp: '2023-01-02 03:30:00',      VevicleID: 'JE65QJK64802',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.8    },    {      PassIndex: 3,      PassID: '1000000033',      PassTimeStamp: '2023-01-02 04:28:00',      VevicleID: 'QO68DIC93032',      TagProvider: 'MR',      PassType: 'visitor',      PassCharge: 13    },    {      PassIndex: 4,      PassID: '1000000034',      PassTimeStamp: '2023-01-02 05:50:00',      VevicleID: 'DO24BCW15511',      TagProvider: 'KO',      PassType: 'visitor',      PassCharge: 13    },    {      PassIndex: 5,      PassID: '1000000051',      PassTimeStamp: '2023-01-02 21:13:00',      VevicleID: 'BY85QGR11636',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.5    },    {      PassIndex: 6,      PassID: '1000000056',      PassTimeStamp: '2023-01-03 01:40:00',      VevicleID: 'IO09FGE68100',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.8    },    {      PassIndex: 7,      PassID: '1000000069',      PassTimeStamp: '2023-01-03 09:23:00',      VevicleID: 'CK97FAU13897',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.5    },    {      PassIndex: 8,      PassID: '1000000071',      PassTimeStamp: '2023-01-03 12:20:00',      VevicleID: 'YX66XYW62640',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 3.1    },    {      PassIndex: 9,      PassID: '1000000078',      PassTimeStamp: '2023-01-03 19:31:00',      VevicleID: 'MP14WFM40909',      TagProvider: 'GF',      PassType: 'home',      PassCharge: 2.8    }  ]}"
#http://localhost:9103/interoperability/api/PassesCost/AO/OO/20230101/20230104
passescost_cli_call = ['se2101', 'passescost', '--op1', 'AO', '--op2', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
passescost_cli_call_expected = "{  op1_ID: 'AO',  op2_ID: 'OO',  RequestTimestamp: '2022-02-26 21:27:25',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 1,  PassesCost: 2}"

#http://127.0.0.1:9103/interoperability/api/PassesAnalysis/KO/OO/20230101/20230104
passesanalysis_cli_call = ['se2101', 'passesanalysis', '--op1', 'KO', '--op2', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
passesanalysis_cli_call_expected = "{  op1_ID: 'KO',  op2_ID: 'OO',  RequestTimestamp: '2022-02-26 21:26:07',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  NumberOfPasses: 1,  PassesList: [    {      PassIndex: 0,      PassID: '1000000086',      StationID: 'WY00MLL63827',      TimeStamp: '2023-01-03 23:11:00',      VevicleID: 'WY00MLL63827',      Charge: 2.8    }  ]}"

#http://localhost:9103/interoperability/api/ChargesBy/OO/20230101/20230104
chargesby_cli_call = ['se2101', 'chargesby', '--op1', 'OO', '--datefrom', '20230101', '--dateto', '20230104']
chargesby_cli_call_expected = "{  op_ID: 'OO',  RequestTimestamp: '2022-02-26 21:24:33',  PeriodFrom: '2023-01-01 00:00:00',  PeriodTo: '2023-01-04 00:00:00',  PPOList: [    { VisitingOperator: 'KO', NumberOfPasses: 1, PassesCost: 2.8 },    { VisitingOperator: 'AO', NumberOfPasses: 1, PassesCost: 2 },    { VisitingOperator: 'GF', NumberOfPasses: 1, PassesCost: 2.5 }  ]}"


reset_passes_cli_call = ['se2101', 'resetpasses']
reset_passes_cli_call_expected = "{ status: 'OK' }"

reset_stations_cli_call = ['se2101', 'resetstations']
reset_stations_cli_call_expected = "{ status: 'OK' }"

reset_vehicles_cli_call = ['se2101', 'resetvehicles']
reset_vehicles_cli_call_expected = "{ status: 'OK' }"

healthcheck_cli_call = ['se2101', 'healthcheck']
healthcheck_cli_call_expected = "{ status: 'OK', dbconnection: 'BM25PHF40639ekjejuwn34553JSQ0002840' }"


class CLITestCases(TestCase):
    def setUp(self):
        init()
        print(bcolors.OKCYAN + 'Now running CLI tests' + bcolors.ENDC)

    def test_testcases(self):
        url = 'http://127.0.0.1:9103/backend/uploadCSV'
        file = {'file': open('../../sample_data/test.csv', 'rb')}
        requests.post(url, files=file)

        self.passes_per_station_cli_test()
        self.passes_cost_cli_test()
        self.passes_analysis_cli_test()
        self.charges_by_cli_test()
        self.reset_passes_cli_test()
        self.reset_stations_cli_test()
        self.reset_vehicles_cli_test()
        self.healthcheck_cli_test()

        requests.post('http://127.0.0.1:9103/backend/deleteCSV')

    def passes_per_station_cli_test(self):
        process = subprocess.run(passesperstation_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response[0:42] + response[85:-1] == passesperstation_cli_call_expected[0:42] + passesperstation_cli_call_expected[85:-1]:
            print(bcolors.OKGREEN + '.Testcase 1 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 1 failed ' + bcolors.ENDC + 'X')

    def passes_cost_cli_test(self):
        process = subprocess.run(passescost_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response[0:30] + response[72:-1] == passescost_cli_call_expected[0:30] + passescost_cli_call_expected[72:-1]:
            print(bcolors.OKGREEN + '.Testcase 2 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 2 failed ' + bcolors.ENDC + 'X')

    def passes_analysis_cli_test(self):
        process = subprocess.run(passesanalysis_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')

        if response[0:30] + response[72:-1] == passesanalysis_cli_call_expected[0:30] + passesanalysis_cli_call_expected[72:-1]:
            print(bcolors.OKGREEN + '.Testcase 3 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 3 failed ' + bcolors.ENDC + 'X')

    def charges_by_cli_test(self):
        process = subprocess.run(chargesby_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response[0:14] + response[56:-1] == chargesby_cli_call_expected[0:14] + chargesby_cli_call_expected[56:-1]:
            print(bcolors.OKGREEN + '.Testcase 4 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 4 failed ' + bcolors.ENDC + 'X')

    def reset_passes_cli_test(self):
        process = subprocess.run(reset_passes_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')

        if response == reset_passes_cli_call_expected:
            print(bcolors.OKGREEN + '.Testcase 5 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 5 failed ' + bcolors.ENDC + 'X')

    def reset_stations_cli_test(self):
        process = subprocess.run(reset_stations_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response == reset_stations_cli_call_expected:
            print(bcolors.OKGREEN + '.Testcase 6 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 6 failed ' + bcolors.ENDC + 'X')

    def reset_vehicles_cli_test(self):
        process = subprocess.run(reset_vehicles_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response == reset_vehicles_cli_call_expected:
            print(bcolors.OKGREEN + '.Testcase 7 passed ' + bcolors.ENDC + u'\N{check mark}')
        else:
            print(bcolors.FAIL + '.Testcase 7 failed ' + bcolors.ENDC + 'X')

    def healthcheck_cli_test(self):
        process = subprocess.run(healthcheck_cli_call, capture_output=True)
        response = process.stdout.decode('ascii').replace('\n', '')
        if response == healthcheck_cli_call_expected:
            print(bcolors.OKGREEN + '.Testcase 8 passed ' + bcolors.ENDC + u'\N{check mark}' + '\n')
        else:
            print(bcolors.FAIL + '.Testcase 8 failed ' + bcolors.ENDC + 'X' + '\n')