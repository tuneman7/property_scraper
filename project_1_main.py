import project_1_objects
from project_1_objects import AreaDataStore
from project_1_objects import AreaDataMenu
from project_1_objects import AreaDisplay
from project_1_objects import AreaGraph
from project_1_objects import  AreaInformationByZipcode

def main():

    area_data_store = AreaDataStore()
    # area_data_store.smooth_data()
    # l_areas_by_zipcode = area_data_store.get_area_info_by_zipcode('90068')
    # for object in l_areas_by_zipcode:
    #     print(object.zipcode,object.extract_day_id)
    # # print(area_data_store.area_data_objects_by_zipcode)



    # area_graph = AreaGraph()
    # area_graph.plot_the_dealio()

    #
    stil_running = True
    while stil_running:

        area_data_menu = AreaDataMenu()
        area_data_menu.display_area_data_menu()
        zip_code_to_display = area_data_menu.get_main_menu_input()
        area_display_object = AreaDisplay(zip_code_to_display)

        return_to_main_menu = False
        while not return_to_main_menu:
            area_display_object.display_area_data_menu()
            area_display_option = area_display_object.get_area_menu_input()

            if area_display_option[0] == 'return':
                return_to_main_menu = True
                break
            else:
                # print(area_display_option)
                area_display_object.display_graph_based_on_input(area_display_option,zip_code_to_display)



main()
