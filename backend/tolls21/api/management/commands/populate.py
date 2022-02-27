from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv
from api.models import driver, provider, vehicle, station, pass_event
from datetime import date, datetime
from django.utils.timezone import make_aware
import os

debug = True

provider_names = ["aodos", "gefyra", "egnatia", "kentriki_odos", "moreas", "nea_odos", "olympia_odos"]
provider_abbr = ["AO", "GF", "EG", "KO", "MR", "NE", "OO"]

def populate_providers():
    print("Populating providers table...")
    for name, abbr in zip(provider_names, provider_abbr):
        obj, created = provider.objects.get_or_create(
            user_id = User.objects.get(username = name),
            provider_id = abbr,
            fullname = name
        )
        if debug:
            if created: print(f"Table entry {obj} created!")
            else: print(f"Table entry {obj} already exists!")
    print("Done populating providers table!\n")


def populate_stations():
    print("Populating stations table from 'sampledata01_stations.csv'...")
    file = open('../../sample_data/sampledata01_stations.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        stationID       = strings[0]
        stationProvider = strings[1]
        stationName     = strings[2]
        obj, created = station.objects.get_or_create(
            station_id = stationID,
            station_name = stationName,
            provider = provider.objects.get(fullname = stationProvider)
        )
        if debug:
            if created: print(f"Table entry {obj} created!")
            else: print(f"Table entry {obj} already exists!")
    print("Done populating stations table!\n")


def populate_vehicles():
    print("Populating vehicles table from 'sampledata01_vehicles_100.csv'...")
    file = open('../../sample_data/sampledata01_vehicles_100.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        vehicleID = strings[0]
        tagID = strings[1]
        providerAbbr = strings[3]
        licenseYear = strings[4]
        obj, created = vehicle.objects.get_or_create(
            vehicle_id = vehicleID,
            tag_id = tagID,
            provider = provider.objects.get(provider_id = providerAbbr),
            license_year = int(licenseYear)
        )
        if debug:
            if created: print(f"Table entry {obj} created!")
            else: print(f"Table entry {obj} already exists!")
    print("Done populating vehicles table!\n")


fullnames = ['Carlisle Bridgeman', 'Yashvi Waldner', 'Cing Abeyta', 'Rori Nolen', 'Belinda Stearns', 'Jaila Homer', 'Kaavya Hobart', 'Roslyn Mcdonnell', 'Leeana Hathcock', 'Shulem Pagel', 'Swara Wooldridge', 'Tiffany Archer', 'Nellie Boles', 'Alexi Hoyer', 'Lisette Bernardo', 'Blair Reyna', 'Jaymes Kingery', 'Illyana Raygoza', 'Fox Lo', 'Jaida Roper', 'Roman Nichols', 'Bernard Robert', 'Karlei Fasano', 'Jaina Quinlan', 'Daegan Markus', 'Ivyana Pendley', 'Kolton Dodson', 'Karolina Sage', 'Blakeleigh Kao', 'Julieth Thornhill', 'Brantlee Yee', 'Kalie Karl', 'Tirzah Pine', 'Makai Rosen', 'Gwynn Lafave', 'Haden Riedel', 'Henley Cosgrove', 'Reyansh Ocampo', 'Omega Bixby', 'Kiyan Brockman', 'Derek Daniel', 'Zadok Kessinger', 'Levy Barner', 'Mihika Rothwell', 'Avi Humble', 'Lainee Kamp', 'Dereck Noriega', 'Brihanna Wester', 'Rubin Cespedes', 'Sia Whelan', 'Sunshine Milne', 'Lion Minard', 'Tamya Gurrola', 'Lysander Gaeta', 'Arien Chafin', 'Alexandre Harter', 'Kailea Hinckley', 'Jeancarlo Mcanally', 'Raelyn Stafford', 'Brittany Booker', 'Francisca Cannady', 'Kylah Rader', 'Finlay Flagg', 'Mirielle Wethington', 'Aaditya Agustin', 'Alexxa Schuman', 'Yehuda Hare', 'Adelynne Tillery', 'Brentlee Worthy', 'Kenzleigh Logue', 'Reyna Battle', 'Mohamed Spence', 'Jaelyn Mckibben', 'Dwight Shay', 'Fayth Scanlan', 'Keilly Konrad', 'Rayleigh Lorenzo', 'Blessin Jepson', 'Eduard Maines', 'Railynn Brodie', 'Stryker Horowitz', 'Shaelyn Wilhite', 'Tanvi Sanborn', 'Jalil Callender', 'Analeah Scholl', 'Kalin Paynter', 'Aseel Fritts', 'Calix Mcelveen', 'Lloyd Malcolm', 'Tytus Tilton', 'Blessyn Mertens', 'Kale Moya', 'Bryar Wick', 'Braden Fry', 'Kenzy Maupin', 'Paxson Lesher', 'Rowdy Troutman', 'Cory Gary', 'Ivy Alvarado', 'Azalea Whitfield']
phones = [9465033583, 6893799017, 9403383928, 6870995375, 9441657173, 6899355016, 9407028030, 6954968427, 6889611443, 6852385489, 6885674558, 6856125474, 6858444220, 6995757282, 6983321241, 6889179453, 9482162940, 6874642614, 6874726698, 6896964208, 6854505607, 9490901323, 6887882555, 6951892024, 6851012502, 9413084944, 9411809542, 9468640211, 6890689268, 9443225053, 6930098655, 9426725149, 9489688398, 6985804596, 9423880800, 9481828515, 6852316164, 6871469450, 6885197490, 6886329785, 6852887853, 6889191968, 6973118718, 6876402036, 6874180833, 6856068214, 6923573821, 6898761571, 6968492033, 6873008140, 9451481267, 6877281944, 6879533298, 6858089632, 6853814765, 6932704272, 9403589323, 6851649491, 6893121684, 6891550396, 6875774469, 6873182100, 6879323261, 9431255662, 9489803783, 6871081631, 6940741811, 9408438939, 6883751101, 6899176792, 6986093738, 9489593533, 6871873237, 6874757516, 6874132146, 6851150062, 6890106801, 9487601718, 9446348829, 9433823611, 6871148979, 6885038695, 6883027476, 6916357625, 6896857265, 9487425272, 6850107654, 6890699751, 6872931814, 6937579392, 9494491906, 6980763558, 6874929573, 6930237261, 6897649424, 6885254386, 6880412484, 6853879397, 9442917346, 6996846810]
ssns = [689183116, 693412937, 690186447, 949080327, 689313147, 946200081, 691256895, 685861907, 948834476, 688624337, 693158599, 698057800, 689934643, 949797868, 697505654, 696734450, 685386694, 698475294, 685192756, 692145030, 941752892, 685007140, 942021886, 948302368, 687381542, 945739680, 688037635, 940190483, 691210720, 693162456, 689560194, 949142778, 694122512, 691365452, 688618285, 685533996, 690272881, 685993474, 691971386, 696689195, 948297317, 697383877, 689837748, 688367368, 949135996, 943329130, 691934039, 698986918, 944417428, 687347281, 699856008, 944153322, 941124585, 688859720, 691887857, 944899717, 949722793, 694629460, 944759796, 947662649, 697846490, 947665471, 940734353, 699839001, 689704982, 947321627, 687020466, 685356222, 689123461, 689947890, 694894880, 942669971, 685440178, 946404915, 691303730, 694446512, 685534772, 689887852, 699943405, 943456786, 948406344, 694159997, 691341375, 689957363, 945097370, 685478355, 689701913, 694182941, 945322000, 948139094, 946978022, 687395404, 948452010, 942618528, 685253335, 685223067, 699400644, 698464376, 693227493, 688343127]
birth_dates = [(1977, 5, 14), (2000, 3, 5), (1973, 5, 11), (1996, 12, 18), (1990, 4, 23), (1978, 4, 27), (1996, 1, 26), (1995, 2, 7), (2000, 5, 13), (2000, 2, 13), (1984, 4, 11), (1995, 11, 19), (1987, 12, 22), (1979, 1, 7), (1991, 2, 13), (1988, 1, 22), (1979, 6, 26), (1992, 2, 12), (1996, 9, 20), (1989, 5, 20), (1992, 3, 10), (1996, 11, 1), (1975, 9, 5), (1971, 11, 15), (1975, 9, 24), (1994, 10, 18), (1994, 9, 10), (1971, 5, 9), (1972, 11, 18), (1995, 1, 7), (1980, 12, 23), (1982, 5, 19), (1983, 1, 3), (1999, 2, 27), (1995, 9, 1), (1978, 12, 17), (1997, 1, 8), (1988, 11, 28), (1974, 5, 5), (1973, 11, 14), (1970, 7, 8), (1977, 5, 15), (1980, 1, 6), (1980, 9, 14), (1977, 6, 8), (1997, 5, 29), (1996, 1, 19), (1986, 9, 16), (1993, 11, 9), (1993, 12, 1), (1983, 10, 8), (1994, 9, 18), (1985, 1, 13), (1979, 2, 12), (1992, 10, 24), (1982, 10, 15), (1987, 11, 12), (1994, 7, 28), (1984, 11, 15), (1990, 7, 24), (1986, 11, 12), (1980, 6, 9), (1971, 2, 22), (1994, 1, 6), (1997, 3, 19), (1970, 12, 1), (1983, 10, 1), (1977, 5, 13), (1977, 9, 19), (1988, 3, 17), (1995, 4, 4), (1990, 2, 9), (1981, 7, 6), (1998, 3, 14), (1981, 11, 25), (1987, 1, 20), (1995, 11, 29), (1976, 4, 10), (1987, 2, 15), (1977, 8, 17), (1996, 9, 11), (1985, 5, 14), (1980, 2, 7), (1982, 5, 14), (1997, 5, 26), (1979, 11, 26), (1972, 2, 25), (1997, 10, 23), (1985, 8, 5), (1998, 4, 26), (1982, 4, 27), (1995, 9, 27), (1977, 10, 20), (1997, 7, 23), (1996, 3, 6), (1972, 4, 21), (1990, 5, 18), (1972, 9, 9), (1974, 7, 12), (1991, 5, 24)]

def populate_drivers():
    print("Populating drivers table with randomly generated data lists")
    file = open('../../sample_data/sampledata01_vehicles_100.csv')
    reader = csv.reader(file)
    next(reader)
    for row, my_name, my_phone, my_date, my_ssn in zip(reader, fullnames, phones, birth_dates, ssns):
        strings = row[0].split(";")
        vehicleID = strings[0]
        obj, created = driver.objects.get_or_create(
            first_name  = my_name.split(" ")[0],
            last_name   = my_name.split(" ")[1],
            phoneNo     = my_phone,
            birth_date  = date(my_date[0], my_date[1], my_date[2]),
            ssn         = my_ssn,
            vehicle     = vehicle.objects.get(vehicle_id=vehicleID)
        )
        if debug:
            if created: print(f"Table entry {obj} created!")
            else: print(f"Table entry {obj} already exists!")
    print("Done populating drivers table!\n")

def populate_pass_events():
    print("Populating pass events from sampledata01_passes100_8000.csv")
    file = open('../../sample_data/sampledata01_passes100_8000.csv')
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        strings = row[0].split(";")
        date = strings[1].split()[0].split("/")
        time = strings[1].split()[1].split(":")
        obj, created = pass_event.objects.get_or_create(
            pass_id = strings[0],
            timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
            vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
            stationRef = station.objects.get(station_id=strings[2]),
            charge = float(strings[4])
        )
        if debug:
            if created: print(f"Table entry {obj} created!")
            else: print(f"Table entry {obj} already exists!")
    print("Done populating pass events table!\n")

def populate_users():
    print("Populating users")
    for name in provider_names:
        if not User.objects.filter(username = name).exists():
            user = User.objects.create_user(username = name, password='test123')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"User {user} created!")
        else:
            print(f"User {name} already exists!")
    print("Done populating users")

def populate_everything():
    populate_users()
    populate_providers()
    populate_stations()
    populate_vehicles()
    populate_drivers()
    populate_pass_events()

# The screen clear function
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def print_menu():
    print(
    """These operations are currently available:
1) Populate everything
2) Populate users
3) Populate providers
4) Populate stations
5) Populate vehicles
6) Populate drivers
7) Populate pass events
8) Manual addition of one entry
9) Exit""")

def command_interface():
    screen_clear()
    print("Welcome to the database populator programm!!")
    print_menu()
    while True:
        val = int(input("Select an option and press enter(1-9): "))
        if val == 1:
            populate_everything()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()   
        elif val == 2:
            populate_users()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()
        elif val == 3:
            populate_providers()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()
        elif val == 4:
            populate_stations()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()
        elif val == 5:
            populate_vehicles()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()
        elif val == 6:
            populate_drivers()
            input("Press enter to return to the main menu...")
            screen_clear()
            print_menu()
        elif val == 7:
            populate_pass_events()
            input("Press enter to continue...")
            screen_clear()
            print_menu()
        elif val == 8:
            print("Not implemented yet!")
            input("Press enter to continue...")
            screen_clear()
            print_menu()
        elif val == 9:
            print("Exiting!")
            break
        else:
            print("Invalid Command! Try again.")
            input("Press enter to continue...")
            screen_clear()
            print_menu()


class Command(BaseCommand):
    help = "A cli program that helps you populate the database!"

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fast', action='store_true', help='Populates the database faster by not printing!')

    def handle(self, *args, **options):
        flag = options['fast']

        if flag:
            global debug
            debug = False

        command_interface()