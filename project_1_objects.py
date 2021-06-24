import os
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt
from os import system, name
from time import sleep
import copy
import threading
import matplotlib.dates as mdates

GLOBAL_DATA_STORE = None

class Utility:

    def __init__(self):
        self.bozo ="bozo"
        self.screen_width = 76
    # define our clear function
    def clear(self):

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


    def center_with_stars(self,input_string,screen_width):
        buffer = int((screen_width -len(input_string)-2)/2)
        input_string = "*" + " " *buffer+ input_string +" "*buffer+"*"
        if(len(input_string)<screen_width):
            input_string.replace(" *","  *")
        # print(len(input_string))    
        return input_string

    def print_header(self):
        print("*"*self.screen_width)
        print(self.center_with_stars("U.C. Berkeley MIDS Summer 2021 W200 Project 1 -- Don Irwin",self.screen_width))
        print("*"*self.screen_width)
        print(self.center_with_stars("Real Estate Market Info by Zip Code System",self.screen_width))
        print("*"*self.screen_width)

    def get_data_from_file(self,str_file_name):
        with open(str_file_name, 'r') as file:
            data = file.read()

        return data
    def get_this_dir(self):
        thisdir = os.getcwd()
        return thisdir

    def display_splash_screen(self):
        self.clear()
        splash_file = os.path.join(self.get_this_dir(),'splash_text.txt')
        print(self.get_data_from_file(splash_file))
        sleep(2)

    def displa_exit_screen(self):
        self.clear()
        splash_file = os.path.join(self.get_this_dir(),'goodbye.txt')
        print(self.get_data_from_file(splash_file))
        sleep(2)



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
    smooth_data_dir = "historical_data"
    rough_data_dir = "historical_data_original_do_not_delete"

    def __init__(self,use_rough_data=False):
        if use_rough_data:
            self.data_directory = AreaDataStore.rough_data_dir
        else:
            self.data_directory = AreaDataStore.smooth_data_dir
        self.area_data_objects_by_zipcode = {}
        self.area_name_by_zipcode = {}
        self.util = Utility()
        self.load_area_data_objects()
        self.beginning_day_id = "20210318"
        self.ending_day_id = "20210606"

    #remove later
    def smooth_data(self):
        copy_of_area_objects_by_zipcode = copy.deepcopy(self.area_data_objects_by_zipcode)
        last_median_price = 0
        last_list_count = 0
        last_price_per_square_ft = 0
        for zip_code in self.area_data_objects_by_zipcode.keys():
            next_zipcode = True
            day_ids_in_smoothing_step = []
            for day_id in self.area_data_objects_by_zipcode[zip_code].keys():
                print(zip_code,day_id,self.area_data_objects_by_zipcode[zip_code][day_id].median_list_price)
                try:
                    i_median_price = int(self.area_data_objects_by_zipcode[zip_code][day_id].median_list_price.replace(",",""))
                except:
                    i_median_price = 0
                try:
                    i_list_count = int(self.area_data_objects_by_zipcode[zip_code][day_id].active_listings)
                except:
                    i_list_count = 0
                try:
                    i_price_per_square_ft = int(self.area_data_objects_by_zipcode[zip_code][day_id].median_price_per_sqft)
                except:
                    i_price_per_square_ft = 0
                print("listing count =", i_list_count,zip_code,day_id)
                if last_median_price !=0 and last_median_price != i_median_price:
                    #print(day_ids_in_smoothing_step)
                    #we have a change mark the day_id where the change occured
                    count_in_smoothing_step = len(day_ids_in_smoothing_step)
                    price_delta = (i_median_price-last_median_price)

                    listing_delta = (int(i_list_count)-int(last_list_count))
                    square_feet_delta = (int(i_price_per_square_ft)-int(last_price_per_square_ft))

                    if count_in_smoothing_step ==0:
                        median_price_smoothing_step = price_delta
                        listing_count_smoothing_step = listing_delta
                        price_per_square_ft_smoothing_step = square_feet_delta
                    else:
                        median_price_smoothing_step = int(round(price_delta/count_in_smoothing_step))
                        listing_count_smoothing_step = int(round(listing_delta/count_in_smoothing_step))
                        price_per_square_ft_smoothing_step = int(round(square_feet_delta/count_in_smoothing_step))

                    if i_median_price<last_median_price:
                        median_price_smoothing_step = int(round(median_price_smoothing_step*(-1)))
                    if i_price_per_square_ft<last_price_per_square_ft:
                        price_per_square_ft_smoothing_step = int(round(price_per_square_ft_smoothing_step*(-1)))

                    if i_list_count<last_list_count:
                        listing_count_smoothing_step = int(round(listing_count_smoothing_step*(-1)))




                    #now do the smoothing
                    for day_id_to_smooth in day_ids_in_smoothing_step:
                        my_object = copy_of_area_objects_by_zipcode[zip_code][day_id_to_smooth]
                        print(zip_code,day_id_to_smooth,my_object.median_list_price,median_price_smoothing_step,last_median_price,i_median_price,price_delta,count_in_smoothing_step)
                        original_price = my_object.median_list_price
                        try:
                             my_object.median_list_price = "{:,}".format((int(my_object.median_list_price.replace(",","")) + median_price_smoothing_step))
                        except:
                            my_object.median_list_price = my_object.median_list_price

                        try:
                            my_object.median_price_per_sqft = int(my_object.median_price_per_sqft.replace(",","")) + price_per_square_ft_smoothing_step
                        except:
                            my_object.median_price_per_sqft + my_object.median_price_per_sqft

                        try:
                            my_object.active_listings = int(my_object.active_listings) + listing_count_smoothing_step
                        except:
                            my_object.active_listings = my_object.active_listings

                        copy_of_area_objects_by_zipcode[zip_code][day_id_to_smooth] = my_object

                        print("smoothed price=",copy_of_area_objects_by_zipcode[zip_code][day_id_to_smooth].median_list_price,"original price=",original_price)

                    # #now clear out the day_ids to smooth
                    day_ids_in_smoothing_step.clear()

                else:
                    day_ids_in_smoothing_step.append(self.area_data_objects_by_zipcode[zip_code][day_id].extract_day_id)

                last_median_price = i_median_price
                last_price_per_square_ft = i_price_per_square_ft
                last_list_count = i_list_count

        self.save_smoothed_objects(copy_of_area_objects_by_zipcode)


    def save_smoothed_objects(self,copy_of_area_objects_by_zipcode):

        thisdir = os.getcwd()

        for zipcode in copy_of_area_objects_by_zipcode.keys():
            for day_id in copy_of_area_objects_by_zipcode[zipcode].keys():
                json_object = copy_of_area_objects_by_zipcode[zipcode][day_id]

                fileToSave = os.path.join( thisdir, 'historical_data_smoothed',  json_object.extract_day_id , '{}_extract_{}.json'.format(json_object.zipcode,json_object.extract_day_id))

                daydirectory = thisdir + '\\historical_data_scrubbed\\' + json_object.extract_day_id + '\\'
                daydirectory = os.path.join(thisdir,'historical_data_smoothed',  json_object.extract_day_id )

                if not os.path.exists(daydirectory):
                    os.makedirs(daydirectory)
                print(fileToSave)
                with open(fileToSave,"w") as outfile:
                    json.dump(json_object.__dict__,outfile,indent=4,sort_keys=True)



    #remove later
    def scrub_and_save_file(self,json_object):
        if(len(json_object.median_list_price)==3):
                json_object.median_list_price = json_object.median_list_price + ",000"
        thisdir = os.getcwd()
        fileToSave = thisdir + '\\historical_data_scrubbed\\' + json_object.extract_day_id + '\\{}_extract_{}.json'.format(json_object.zipcode,json_object.extract_day_id)

        fileToSave = os.path.join( thisdir, 'historical_data_scrubbed',  json_object.extract_day_id , '{}_extract_{}.json'.format(json_object.zipcode,json_object.extract_day_id))

        daydirectory = thisdir + '\\historical_data_scrubbed\\' + json_object.extract_day_id + '\\'
        daydirectory = os.path.join(thisdir,'historical_data_scrubbed',  json_object.extract_day_id )

        if not os.path.exists(daydirectory):
            os.makedirs(daydirectory)

        with open(fileToSave,"w") as outfile:
            json.dump(json_object.__dict__,outfile,indent=4,sort_keys=True)


    def load_area_data_objects(self):
        this_dir = os.getcwd()
        historical_data_dir = this_dir + '\\historical_data\\'
        historical_data_dir = os.path.join(this_dir, self.data_directory)

        print(this_dir)
        day_id_dirs = [day_id_directory for day_id_directory in os.listdir(historical_data_dir) ]

        l_area_data_by_zipcode = []
        zip_code_set = set()

        for day_id in day_id_dirs:
            try:
                my_day_id = int(day_id)
            except:
                continue
            # print("day_id=",day_id)
            if not (int(day_id)<int(self.beginning_day_id)) and not (int(day_id)>int(self.ending_day_id)):
                day_id_directory = historical_data_dir + day_id
                day_id_directory = os.path.join(historical_data_dir,day_id)
                json_files = [full_directory for full_directory in os.listdir(day_id_directory) ]
                for json_file in json_files:
                    zip_code = json_file.split('_')[0]
                    file_name = day_id_directory + '\\' + json_file
                    file_name = os.path.join(day_id_directory,json_file)
                    file_data = self.util.get_data_from_file(file_name)
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
        l_return = [self.area_data_objects_by_zipcode[zip_code][key] for key in sorted(self.area_data_objects_by_zipcode[zip_code].keys())]
        return l_return

class AreaDataMenu:

    def __init__(self):
        self.util = Utility()
        self.util.display_splash_screen()
        # self.display_area_data_menu()
        self.first_time_display=True

        data_store_selection = self.display_data_source_menu()
        if data_store_selection == '1':
            global_data_store = AreaDataStore()
        else:
            use_rough_data = True
            global_data_store = AreaDataStore(use_rough_data)

        global GLOBAL_DATA_STORE
        GLOBAL_DATA_STORE = global_data_store
        self.area_data_store = GLOBAL_DATA_STORE
        self.display_area_data_menu()



    def display_data_source_menu(self):
        self.util.clear()
        self.util.print_header()
        self.util.center_with_stars("DATA SOURCE MENU",76)
        print("*"*self.util.screen_width)
        print(" "*self.util.screen_width)

        self.menu_dict = {}
        self.menu_dict['1']="Smoothed Data (default)"
        self.menu_dict['2']="Original Rough Data"


        for option in self.menu_dict.keys():
            if(int(option)<10):
                to_print = "{}.  : {}".format(option,self.menu_dict[option])
            else:
                to_print = "{}. : {}".format(option,self.menu_dict[option])
            # side_buffer = (len(to_print)-screen_width)/2
            to_print = " "*int(20) + to_print
            print(to_print)

        print(" "*self.util.screen_width)
        print(" "*self.util.screen_width)

        print("*"*self.util.screen_width)
        print(self.util.center_with_stars("Select what data you would like to use.",self.util.screen_width))

        print("*"*self.util.screen_width)
        print(" "*self.util.screen_width)

        data_type_selection = input("Please make your selection:")
        while data_type_selection not in self.menu_dict.keys():
            print("The value you selected {} is not a valid input.".format(data_type_selection))
            data_type_selection = input("Please make your selection:")

        return data_type_selection

    def display_area_data_menu(self,error_of_input=False,input_value=None):
        self.util.clear()
        max_key = max(self.area_data_store.area_name_by_zipcode, key=lambda k: len(self.area_data_store.area_name_by_zipcode[k]))
        max_len = len(self.area_data_store.area_name_by_zipcode[max_key])
        screen_width = 76
        self.util.print_header()
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
                    # print("Quitting -- goodbye.")
                    self.util.displa_exit_screen()
                    sys.exit()
                else:
                    good_input = True
                    return menu_dict[my_input]

class GraphDataObject:

    def __init__(self):
        self.x_axis_values = None
        self.y_axis_values = None
        self.label = None

class AreaDisplay:


    def __init__(self,input_zip_code):
        global GLOBAL_DATA_STORE
        self.area_data_store = GLOBAL_DATA_STORE
        # self.area_data_store = AreaDataStore()
        self.zip_code = input_zip_code
        self.util = Utility()

    def display_area_data_menu(self,input_is_valid=True,input_value=""):
        self.util.clear()
        max_key = max(self.area_data_store.area_name_by_zipcode, key=lambda k: len(self.area_data_store.area_name_by_zipcode[k]))
        max_len = len(self.area_data_store.area_name_by_zipcode[max_key])
        screen_width = 76

        self.util.print_header()

        print(self.util.center_with_stars("AREA DETAILS MENU ".format(self.zip_code),screen_width))
 
        print(self.util.center_with_stars("You have selected zip code {}".format(self.zip_code),screen_width))
        print(self.util.center_with_stars("Area Name: {}".format(self.area_data_store.area_name_by_zipcode[self.zip_code]),screen_width))

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

        self.menu_dict['return']='return'
        self.menu_dict['quit']='quit'

        print(" "*screen_width)
        print(" "*screen_width)

        print("*"*screen_width)
        print(self.util.center_with_stars("Please enter the number of the graph to view.",screen_width))
        print(self.util.center_with_stars("Enter 'return' to return to the Home Menu, 'quit' to exit.",screen_width))

        print("*"*screen_width)
        print(" "*screen_width)

        # if not input_is_valid:
        #     self.get_area_menu_input(input_is_valid,input_value,menu_dict)
        # else:
        #     return_value = self.get_area_menu_input(input_is_valid, None, menu_dict)
        #     if return_value is not None:
        #         return return_value

    def get_area_menu_input(self):


        good_input=False
        while not good_input:
            good_input = True
            my_input = input("Please make your selection:").lower()
            if my_input not in self.menu_dict.keys():
                self.display_area_data_menu()
                print("The input your provided '{}' is not a valid menu choice.".format(my_input))
                good_input = False
                continue

        if my_input == 'quit':
            self.util.displa_exit_screen()
            sys.exit()


        return my_input, self.menu_dict[my_input]

    def display_graph_based_on_input(self,input_tuple,zip_code):
        graph_option = int(input_tuple[0])
        graph_description = input_tuple[1]
        graph_title = graph_description.replace("Graph","Graph of") + \
                      " For\n" + self.area_data_store.area_name_by_zipcode[zip_code] + \
                      ", Zipcode: {}".format(zip_code)
        # datetime(object.extract_dt.split(",")[0]).date()
        x_axis_values = [datetime.strptime(object.extract_dt.split(",")[0],'%m/%d/%Y').date()  for object in self.area_data_store.get_area_info_by_zipcode(zip_code)]
        y_label = ""
        if graph_option == 1:
            y_axis_values = [int(object.median_list_price.replace(",", "")) if len(object.median_list_price.replace(",", ""))>0 else 0  for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            if max(y_axis_values)>1000000:
                y_label = "Median Listing Price in Millions"
            else:
                y_label = "Median Listing Price in Dollars"


        if graph_option == 2:

            y_axis_values = [int(object.active_listings) for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            y_label = "Active Listings in Zipcode"


        if graph_option == 3:
            y_axis_values = [int(object.median_price_per_sqft)  for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            y_label = "Median Price Per Sq Ft in Dollars"

        #Simple single lined graphs.
        if graph_option != 4:
            area_graph = AreaGraph()
            area_graph.plot_single_area_stats(x_axis_values,y_axis_values,"Day",y_label,graph_title)

        #Multi_line_graph
        if graph_option == 4:
            lgo = []
            mpgdo = GraphDataObject()
            mpgdo.label = "Median Price"
            mpgdo.x_axis_values = x_axis_values
            mpgdo.y_axis_values = [int(object.median_list_price.replace(",", "")) if len(object.median_list_price.replace(",", ""))>0 else 0  for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            lgo.append(mpgdo)
            algdo = GraphDataObject()
            algdo.label = "Active Listings"
            algdo.x_axis_values = x_axis_values
            algdo.y_axis_values = [int(object.active_listings)*200 for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            lgo.append(algdo)
            ppsqftgdo = GraphDataObject()
            ppsqftgdo.label = "Sqft Price"
            ppsqftgdo.x_axis_values = x_axis_values
            ppsqftgdo.y_axis_values = [int(object.median_price_per_sqft)*1000  for object in
                             self.area_data_store.get_area_info_by_zipcode(zip_code)]
            lgo.append(ppsqftgdo)

            area_graph = AreaGraph()
            area_graph.plot_multi_line_graph(lgo)
            graph_title = "Multi Line Graph" + \
                          " For\n" + self.area_data_store.area_name_by_zipcode[zip_code] + \
                          ", Zipcode: {}".format(zip_code)


class AreaGraph:

    def __init__(self):
        global GLOBAL_DATA_STORE
        self.area_data_store = GLOBAL_DATA_STORE
        self.util = Utility()

    def plot_multi_line_graph(self,list_graph_data_objects):

        x_axis_values = None

        for graph_object in list_graph_data_objects:
            plt.plot(graph_object.x_axis_values,graph_object.y_axis_values,label=graph_object.label)
            x_axis_values = graph_object.x_axis_values
        plt.xlabel("Day")
        plt.ylabel("Value")
        plt.title("Test")
        # plt.xticks(x_axis_values[::10],rotation=45)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

        plt.gcf().subplots_adjust(bottom=0.20)
        plt.gcf().subplots_adjust(left=0.25)
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()


    def plot_single_area_stats(self,x_axis_values,y_axis_values,x_label,y_label,graph_label):

        # print(x_axis_values)
        # dealio = input("input")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

        plt.plot(x_axis_values,y_axis_values)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(graph_label)
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.gcf().subplots_adjust(bottom=0.20)
        plt.gcf().subplots_adjust(left=0.25)
        plt.gcf().autofmt_xdate()

        plt.show()


    def plot_the_dealio(self):
        print("in plot the dealio")

        y_axis_values = [int(object.median_price_per_sqft.replace(",","")) for object in self.area_data_store.get_area_info_by_zipcode("90023")]
        x_axis_values = [object.extract_day_id for object in self.area_data_store.get_area_info_by_zipcode("90023")]

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())

        plt.plot(x_axis_values,y_axis_values)

        plt.xlabel("Day")
        plt.ylabel("Active Listing Count")
        plt.title("Dealio")
        plt.xticks(x_axis_values[::5],rotation=45)
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.show()


