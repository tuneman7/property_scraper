import os
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt
from os import system, name
from time import sleep

class Utility:

    def __init__(self):
        self.bozo ="bozo"

    # define our clear function
    def clear(self):

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


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
        self.util = Utility()

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
        historical_data_dir = os.path.join(this_dir, 'historical_data')

        print(this_dir)
        day_id_dirs = [day_id_directory for day_id_directory in os.listdir(historical_data_dir) ]

        l_area_data_by_zipcode = []
        zip_code_set = set()

        for day_id in day_id_dirs:
            if not (int(day_id)<int(AreaDataStore.beginning_day_id)) and not (int(day_id)>int(AreaDataStore.ending_day_id)):
                day_id_directory = historical_data_dir + day_id
                day_id_directory = os.path.join(historical_data_dir,day_id)
                json_files = [full_directory for full_directory in os.listdir(day_id_directory) ]
                for json_file in json_files:
                    zip_code = json_file.split('_')[0]
                    file_name = day_id_directory + '\\' + json_file
                    file_name = os.path.join(day_id_directory,json_file)
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
        # self.display_area_data_menu()
        self.util = Utility()

    def display_area_data_menu(self,error_of_input=False,input_value=None):
        self.util.clear()
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

        # if error_of_input:
        #     self.get_main_menu_input(error_of_input,input_value)
        # else:

        # if error_of_input:
        #     self.get_main_menu_input(error_of_input,input_value)
        # else:
        #     return_value = self.get_main_menu_input(False,None)
        #     if return_value is not None:
        #         return return_value

    def get_main_menu_input(self,error_of_input=False,input_value=None):

        menu_dict = {str(list(self.area_data_store.area_name_by_zipcode).index(zip_code)+1):zip_code for zip_code in self.area_data_store.area_name_by_zipcode.keys()}
        menu_dict['quit']=""
        if error_of_input:
            print("The input your provided '{}' is not a valid menu choice.".format(input_value))

        good_input=False
        while not good_input:
            my_input = input("Please make your selection:").lower()
            if my_input not in menu_dict.keys():
                self.display_area_data_menu()
                print("The input your provided '{}' is not a valid menu choice.".format(my_input))
                continue
            else:
                if my_input == "quit":
                    print("Quitting -- goodbye.")
                    sys.exit()
                else:
                    good_input = True
                    return menu_dict[my_input]





class AreaDisplay:


    def __init__(self,input_zip_code):
        self.area_data_store = AreaDataStore()
        self.zip_code = input_zip_code
        self.util = Utility()

    def display_area_data_menu(self,input_is_valid=True,input_value=""):
        self.util.clear()
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

        self.menu_dict = {}
        self.menu_dict['1']="Graph Median Home Price"
        self.menu_dict['2']="Graph Listings in Market"
        self.menu_dict['3']="Graph Price Per Squre Foot"
        self.menu_dict['4']="Graph All"


        for option in self.menu_dict.keys():
            if(int(option)<10):
                to_print = "{}.  : {}".format(option,self.menu_dict[option])
            else:
                to_print = "{}. : {}".format(option,self.menu_dict[option])
            # side_buffer = (len(to_print)-screen_width)/2
            to_print = " "*int(20) + to_print
            print(to_print)

        print(" "*screen_width)
        print(" "*screen_width)

        print("*"*screen_width)
        print(self.center_with_stars("Please enter the number of the graph to view.",screen_width))
        print(self.center_with_stars("Or enter 'return' to return to the Home Menu.",screen_width))

        print("*"*screen_width)
        print(" "*screen_width)

        # if not input_is_valid:
        #     self.get_area_menu_input(input_is_valid,input_value,menu_dict)
        # else:
        #     return_value = self.get_area_menu_input(input_is_valid, None, menu_dict)
        #     if return_value is not None:
        #         return return_value



    def center_with_stars(self,input_string,screen_width):
        buffer = int((screen_width -len(input_string)-2)/2)
        input_string = "*" + " " *buffer+ input_string +" "*buffer+"*"
        if(len(input_string)<screen_width):
            input_string.replace(" *","  *")
        # print(len(input_string))    
        return input_string
        

    def get_area_menu_input(self):

        self.menu_dict['return']='return'

        good_input=False
        while not good_input:
            good_input = True
            my_input = input("Please make your selection:").lower()
            if my_input not in self.menu_dict.keys():
                self.display_area_data_menu()
                print("The input your provided '{}' is not a valid menu choice.".format(my_input))
                continue
            else:
                return my_input, self.menu_dict[my_input]

    def display_graph_based_on_input(self,input_tuple,zip_code):
        graph_option = int(input_tuple[0])
        graph_description = input_tuple[1]
        graph_title = graph_description.replace("Graph","Graph of") + " For\n" + self.area_data_store.area_name_by_zipcode[zip_code]
        x_axis_values = [object.extract_dt.split(",")[0] for object in self.area_data_store.get_area_info_by_zipcode(zip_code)]
        y_label = ""
        if graph_option == 1:
            y_axis_values = [int(object.median_list_price.replace(",", "")) for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            y_label = "Median Listing Price in Millions"

        if graph_option == 2:

            y_axis_values = [int(object.active_listings.replace(",", "")) for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            y_label = "Active Listings in Zipcode"


        if graph_option == 3:
            y_axis_values = [int(object.median_price_per_sqft.replace(",", "")) for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            y_label = "Median Price Per Sq Ft in Dollars"


        if graph_option != 4:
            area_graph = AreaGraph()
            area_graph.plot_single_area_stats(x_axis_values,y_axis_values,"Day",y_label,graph_title)




class AreaGraph:

    def __init__(self):
        self.area_data_store = AreaDataStore()
        self.util = Utility()


    def plot_single_area_stats(self,x_axis_values,y_axis_values,x_label,y_label,graph_label):

        plt.plot(x_axis_values,y_axis_values)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(graph_label)
        plt.xticks(x_axis_values[::10],rotation=45)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.show()


    def plot_the_dealio(self):
        print("in plot the dealio")

        y_axis_values = [int(object.median_price_per_sqft.replace(",","")) for object in self.area_data_store.get_area_info_by_zipcode("90023")]
        x_axis_values = [object.extract_day_id for object in self.area_data_store.get_area_info_by_zipcode("90023")]

        plt.plot(x_axis_values,y_axis_values)

        plt.xlabel("Day")
        plt.ylabel("Active Listing Count")
        plt.title("Dealio")
        plt.xticks(x_axis_values[::10],rotation=45)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.show()


