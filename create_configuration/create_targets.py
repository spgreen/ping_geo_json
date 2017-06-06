import copy
from lib import JSON_FileManagement


class CreatePingTargets:
    # GeoJSON format
    geo_properties = {"name": "", "hostname/ip": "", "country": "", "link": ""}
    geo_geometry = {"type": "Point", "coordinates": []}
    geo_type = {"type": "Feature", "properties": '', "geometry": ''}
    test_store = []

    country_coords_dict = JSON_FileManagement.json_file_to_object("country_to_long-lat.json")

    def add_entry(self):
        """
        Creates a new ping target test entry 
        Request for user input to determine ping target properties and looks up the appropriate co-ordinates
        within the country_coords_dict using the user-submitted country name.
         
        :return: appends test to the ping_target test store 
        """

        geometry = copy.copy(self.geo_geometry)
        properties = copy.copy(self.geo_properties)
        complete_test_entry = copy.copy(self.geo_type)

        for index in properties:
            properties[index] = input("Enter %s: " % index)

        country = properties["country"]

        geometry["coordinates"] = self.coordinate_lookup(country)

        complete_test_entry["properties"] = properties
        complete_test_entry["geometry"] = geometry

        return self.test_store.append(complete_test_entry)

    def add_entry2(self, name, country, hostname_or_ip, link):
        properties = copy.copy(self.geo_properties)
        geometry = copy.copy(self.geo_geometry)
        geo_type = copy.copy(self.geo_type)

        properties["name"] = name
        properties["hostname/ip"] = hostname_or_ip
        properties["country"] = country
        properties["link"] = link

        geometry["coordinates"] = self.coordinate_lookup(country)

        geo_type["properties"] = properties
        geo_type["geometry"] = geometry

        return self.test_store.append(geo_type)

    def coordinate_lookup(self, country_name):
        """
        Looks up country co-ordinates from the country name given. 
        Please provide the common name for said county, eg 'United States' instead of 'United States of America'.
        All country name index entries are titled.
        
        The country name must be spelt correctly otherwise it will return an empty list and an error message.
        
        :param country_name: Country name
        :return: Co-ordinates list of the country in [Longitude, Latitude] format for GeoJSON Co-ordinates
        """
        country_name = country_name.title()
        try:
            return self.country_coords_dict[country_name]["lon_lat"]
        except KeyError:
            print("Error: %s is an invalid country. Returning empty co-ordinates" % country_name)
            return []

    def view_entries(self):
        """
        Displays all of the ping target entries and their respective indexes found within the ping target test store.
        :return: index + entry for each entry within the ping target test store 
        """
        return [print(index,value) for (index, value) in enumerate(self.test_store)]

    def delete_entry(self):
        """
        Delete an existing ping target entry within the ping target test store by user-specified index.
        :return: 
        """
        self.view_entries()
        try:
            number = input("Enter index to be deleted ('no' to cancel): ")
            if number.lower() == "no":
                return
            del self.test_store[int(number)]

        except ValueError:
            print("Error: Not a valid integer")

        except IndexError:
            print("Error: Not a valid index")

    def edit_entry(self):
        """
        Edit an existing ping target entry within the ping target test store by user specified index.

        :return: 
        """
        self.view_entries()

        index = input("Edit test index ('no' to cancel): ")
        if index.lower() == "no":
            return
        try:
            index = int(index)
            # separates properties geometry portions of the config to edit
            properties_to_edit = self.test_store[index]["properties"]
            geometry_to_edit = self.test_store[index]["geometry"]

        except ValueError:
            print("Error: Not a valid value")
            return
        except IndexError:
            print("Error: Not a valid index.")
            return

        hist_country = copy.copy(properties_to_edit["country"])

        # Requests user input if they wish to change a property and new input value if property is changed
        for i in properties_to_edit:
            print("Current %s value: %s" % (i, properties_to_edit[i]))
            if input("Change value for %s (yes/no)? " % i) == 'yes':
                properties_to_edit[i] = input("New value for %s? " % i)

        new_country = properties_to_edit["country"]

        if hist_country != new_country:
            geometry_to_edit["coordinates"] = self.coordinate_lookup(new_country)
        return

    def import_ping_target_conf(self, file_path):
        """
        :param file_path: 
        :return: 
        """
        try:
            target_conf = JSON_FileManagement.json_file_to_object(file_path)
        except FileNotFoundError:
            print("Error: File not found!")
            return

        if ("ping_targets" in target_conf) and (target_conf["ping_targets"]):
            [self.test_store.append(i) for i in target_conf["ping_targets"]]
        return

    def form_conf(self, file_path):
        """
        Forms the final ping_target test as a dictionary; needs to be converted to JSON
        :return: Dictionary of all ping target entries 
        """

        return JSON_FileManagement.save_file_as_json(file_path, dict(ping_targets=self.test_store))


# d=CreatePingTargets()
# #d.add_entry()
#
# aa = ["Choice", "net", "mate"]
# bb = ["Zambia", "Sri Lanka", "New Zealand"]
# cc = ["1G", "2G", "3G"]
# dd = [[30, -15],[81, 7],[174, -41]]
#
# list(map(lambda w,x,y,z: d.add_entry2(w,x,y,z), aa, bb, cc, dd))
# d.edit_entry()
# #d.delete_entry()
#
# print(d.form_conf())

d = CreatePingTargets()

select = '''
Select one of the following:
    1 = Create Entry
    2 = Edit Entry
    3 = Delete Entry
    4 = View Entries
    5 = Import Configuration
    6 = End

Enter arguement: '''

command = []


while command != "6":

    command = input(select)

    if command == '1':
        d.add_entry()
    elif command == '2':
        d.edit_entry()
    elif command == '3':
        d.delete_entry()
    elif command == '4':
        d.view_entries()
    elif command == '5':
        d.import_ping_target_conf(input("Import conf from filepath: "))
    elif command == '6':
        print("End....Forming Ping Targets")
    else:
        print("Not a valid entry")

d.form_conf(input("Enter file path: "))
