import os
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt

class AreaInformationByZipcode:

    def __init__(self,**kwargs):
        allowed_keys = {'zipcode', 'search_uri', 'description'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __init__(self, json_string):
        self.__dict__ = json.loads(json_string)

    def print_internal_directory(self):
        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))


class AreaDataStore:

    beginning_day_id = "20210318"
    ending_day_id = "20210606"


    def __init__(self):

        self.area_data_objects_by_zipcode = {}
        self.area_name_by_zipcode = {}
        self.load_area_data_objects()

    #remove later
    def scrub_and_save_file(self,json_object):
        if(len(json_object.median_list_price)==3):
                json_object.median_list_price = json_object.median_list_price + ",000"
        thisdir = os.getcwd()
        fileToSave = thisdir + '\\historical_data_scrubbed\\' + json_object.extract_day_id + '\\{}_extract_{}.json'.format(json_object.zipcode,json_object.extract_day_id)
        daydirectory = thisdir + '\\historical_data_scrubbed\\' + json_object.extract_day_id + '\\'
        if not os.path.exists(daydirectory):
            os.makedirs(daydirectory)

        with open(fileToSave,"w") as outfile:
            json.dump(json_object.__dict__,outfile,indent=4,sort_keys=True)


    def load_area_data_objects(self):
        this_dir = os.getcwd()
        historical_data_dir = this_dir + '\\historical_data\\'
        print(this_dir)
        day_id_dirs = [day_id_directory for day_id_directory in os.listdir(historical_data_dir) ]

        l_area_data_by_zipcode = []
        zip_code_set = set()

        for day_id in day_id_dirs:
            if not (int(day_id)<int(AreaDataStore.beginning_day_id)) and not (int(day_id)>int(AreaDataStore.ending_day_id)):
                day_id_directory = historical_data_dir + day_id
                json_files = [full_directory for full_directory in os.listdir(day_id_directory) ]
                for json_file in json_files:
                    zip_code = json_file.split('_')[0]
                    file_name = day_id_directory + '\\' + json_file
                    file_data = self.get_data_from_file(file_name)
                    zip_code_by_day_id_data_object = AreaInformationByZipcode(file_data)
                    # self.scrub_and_save_file(zip_code_by_day_id_data_object)
                    # print("zipcode = ", zip_code_by_day_id_data_object.zipcode, zip_code_by_day_id_data_object.extract_day_id)
                    l_area_data_by_zipcode.append((zip_code_by_day_id_data_object))
                    zip_code_set.add(zip_code)

        for zip_code in zip_code_set:
            dict_day_data_in_zipcode = {}
            for zip_code_area_object in l_area_data_by_zipcode:
                if zip_code_area_object.zipcode ==zip_code:
                    # print(zip_code, zip_code_area_object.zipcode, zip_code_area_object.extract_day_id)
                    dict_day_data_in_zipcode[zip_code_area_object.extract_day_id] = zip_code_area_object
                    self.area_name_by_zipcode[zip_code] = zip_code_area_object.description
            self.area_data_objects_by_zipcode[zip_code] = dict_day_data_in_zipcode

            # print(self.area_data_objects_by_zipcode[zip_code])
        # print(self.area_data_objects_by_zipcode.keys())
        # for key in self.area_data_objects_by_zipcode['90017'].keys():
        #     print(key)
        #     object = self.area_data_objects_by_zipcode['90017'][key]
        #     object.print_internal_directory()

    def get_area_info_by_zipcode(self,zip_code):
        l_return = [self.area_data_objects_by_zipcode[zip_code][key] for key in self.area_data_objects_by_zipcode[zip_code].keys()]
        return l_return


    def get_data_from_file(self,str_file_name):
        with open(str_file_name, 'r') as file:
            data = file.read()

        return data


class AreaDataMenu:

    def __init__(self):
        self.area_data_store = AreaDataStore()
        self.display_area_data_menu()

    def display_area_data_menu(self,error_of_input=False,input_value=None):
        os.system("cls")
        max_key = max(self.area_data_store.area_name_by_zipcode, key=lambda k: len(self.area_data_store.area_name_by_zipcode[k]))
        max_len = len(self.area_data_store.area_name_by_zipcode[max_key])
        screen_width = 76
        title = "*        U.C. Berkeley MIDS Summer 2021 W200 Project 1 -- Don Irwin       *"
        print()
        print("*"*screen_width)
        print(title.center(screen_width))
        print("*"*screen_width)
        title1 = "*             Real Estate Market Info by Zip Code System                  *"
        print(title1)

        print("*"*screen_width)
        print("*"*screen_width)
        title1 = "*                            HOME MENU                                    *"
        print(title1)

        print("*"*screen_width)
        print(" "*screen_width)

        print(" "*screen_width)

        int_menu = 1
        for zip_code in self.area_data_store.area_name_by_zipcode.keys():
            if(int_menu<10):
                to_print = "{}.  {} : {}".format(int_menu,zip_code,self.area_data_store.area_name_by_zipcode[zip_code])
            else:
                to_print = "{}. {} : {}".format(int_menu, zip_code,
                                                 self.area_data_store.area_name_by_zipcode[zip_code])
            # side_buffer = (len(to_print)-screen_width)/2
            to_print = " "*int(5) + to_print
            print(to_print)
            int_menu+=1
        print(" "*screen_width)

        print("*"*screen_width)
        title1 = "*  Enter a number corresponding to the zipcode you wish to view or 'quit' *"
        print(title1)

        print("*"*screen_width)
        print(" "*screen_width)
        if error_of_input:
            self.get_main_menu_input(error_of_input,input_value)

    def get_main_menu_input(self,error_of_input=False,input_value=None):

        menu_dict = {str(list(self.area_data_store.area_name_by_zipcode).index(zip_code)+1):zip_code for zip_code in self.area_data_store.area_name_by_zipcode.keys()}
        menu_dict['quit']=""
        if error_of_input:
            print("The input your provided '{}' is not a valid menu choice.".format(input_value))

        good_input=False
        while not good_input:
            good_input = True
            my_input = input("Please make your selection:").lower()
            if my_input not in menu_dict.keys():
                self.display_area_data_menu(True,my_input)

        if my_input == "quit":
            print("Quitting -- goodbye.")
            sys.exit()
        else:
            return menu_dict[my_input]




class AreaDisplay:


    def __init__(self,input_zip_code):
        self.area_data_store = AreaDataStore()
        self.zip_code = input_zip_code
        print("self.zip_code = ",self.zip_code)
        self.display_area_data_menu()
        
    def display_area_data_menu(self):
        os.system("cls")
        max_key = max(self.area_data_store.area_name_by_zipcode, key=lambda k: len(self.area_data_store.area_name_by_zipcode[k]))
        max_len = len(self.area_data_store.area_name_by_zipcode[max_key])
        screen_width = 76
        
        print("*"*screen_width)
        print(self.center_with_stars("U.C. Berkeley MIDS Summer 2021 W200 Project 1 -- Don Irwin",screen_width))
        print("*"*screen_width)
        print(self.center_with_stars("Real Estate Market Info by Zip Code System",screen_width))
        print("*"*screen_width)

        print(self.center_with_stars("AREA DETAILS MENU ".format(self.zip_code),screen_width))
 
        print(self.center_with_stars("You have selected zip code {}".format(self.zip_code),screen_width))
        print(self.center_with_stars("Area Name: {}".format(self.area_data_store.area_name_by_zipcode[self.zip_code]),screen_width))

        print("*"*screen_width)
        print(" "*screen_width)
        print(" "*screen_width)

        menu_dict = {}
        menu_dict['1']="Graph Median Home Price"
        menu_dict['2']="Graph Listings in Market"
        menu_dict['3']="Graph Daily Price Reductions"
        menu_dict['4']="Graph Price Per Squre Foot"
        menu_dict['5']="Graph All"


        for option in menu_dict.keys():
            if(int(option)<10):
                to_print = "{}.  : {}".format(option,menu_dict[option])
            else:
                to_print = "{}. : {}".format(option,menu_dict[option])
            # side_buffer = (len(to_print)-screen_width)/2
            to_print = " "*int(20) + to_print
            print(to_print)

        print(" "*screen_width)
        print("*"*screen_width)

        # print(" "*screen_width)
        #
        # print("*"*screen_width)
        # title1 = "*  Enter a number corresponding to the zipcode you wish to view or 'quit' *"
        # print(title1)
        #
        # print("*"*screen_width)
        # print(" "*screen_width)
        # if error_of_input:
        #     self.get_main_menu_input(error_of_input,input_value)

    def center_with_stars(self,input_string,screen_width):
        buffer = int((screen_width -len(input_string)-2)/2)
        input_string = "*" + " " *buffer+ input_string +" "*buffer+"*"
        if(len(input_string)<screen_width):
            input_string.replace(" *","  *")
        # print(len(input_string))    
        return input_string
        

    def get_area_menu_input(self,error_of_input=False,input_value=None):


        
        if error_of_input:
            print("The input your provided '{}' is not a valid menu choice.".format(input_value))

        good_input=False
        while not good_input:
            good_input = True
            my_input = input("Please make your selection:").lower()
            if my_input not in menu_dict.keys():
                self.display_area_data_menu(True,my_input)

        if my_input == "quit":
            print("Quitting -- goodbye.")
            sys.exit()
        else:
            return menu_dict[my_input]





class AreaGraph:

    def __init__(self):
        self.area_data_store = AreaDataStore()


    def plot_the_dealio(self):


        y_axis_values = [int(object.median_price_per_sqft.replace(",","")) for object in self.area_data_store.get_area_info_by_zipcode("90023")]
        x_axis_values = [object.extract_day_id for object in self.area_data_store.get_area_info_by_zipcode("90023")]

        plt.plot(x_axis_values,y_axis_values)

        plt.xlabel("Day")
        plt.ylabel("Active Listing Count")
        plt.title("Dealio")
        plt.xticks(rotation=90)
        plt.show()

