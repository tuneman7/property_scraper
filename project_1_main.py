import project_1_objects
from project_1_objects import AreaDataStore
from project_1_objects import AreaDataMenu
from project_1_objects import AreaDisplay
from project_1_objects import AreaGraph
from project_1_objects import  AreaInformationByZipcode

def main():

    # area_data_store = AreaDataStore()
    # l_areas_by_zipcode = area_data_store.get_area_info_by_zipcode('90068')
    # for object in l_areas_by_zipcode:
    #     print(object.zipcode,object.extract_day_id)
    # # print(area_data_store.area_data_objects_by_zipcode)
    area_data_menu = AreaDataMenu()
    zip_code_to_display = area_data_menu.get_main_menu_input()
    area_display = AreaDisplay(zip_code_to_display)


    # area_display.plot_the_dealio()

main()
