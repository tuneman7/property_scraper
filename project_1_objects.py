import os
import sys
import json
from datetime import datetime

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

    def display_area_data_menu(self):
        os.system("cls")
        max_key = max(self.area_data_store.area_name_by_zipcode, key=lambda k: len(self.area_data_store.area_name_by_zipcode[k]))
        max_len = len(self.area_data_store.area_name_by_zipcode[max_key])
        screen_width = 75
        title = "*        U.C. Berkeley MIDS Summer 2021 W200 Project 1 -- Don Irwin       *"
        print()
        print("*"*screen_width)
        print(title.center(screen_width))
        print("*"*screen_width)
        title1 = "*             Real Estate Information by Zip Code System                  *"
        print(title1)

        print("*"*screen_width)
        print(" "*screen_width)

        int_menu = 1
        for zip_code in self.area_data_store.area_name_by_zipcode.keys():
            if(int_menu<10):
                to_print = "{}.  {} : {}".format(int_menu,zip_code,self.area_data_store.area_name_by_zipcode[zip_code])
            else:
                to_print = "{}. {} : {}".format(int_menu, zip_code,
                                                 self.area_data_store.area_name_by_zipcode[zip_code])
            # side_buffer = (len(to_print)-screen_width)/2
            to_print = " "*int(10) + to_print
            print(to_print)
            int_menu+=1
# class AreaDisplay:
#
# class AreaGraph: