from project_1_objects import AreaDataMenu
from project_1_objects import AreaDisplay
from project_1_objects import Utility

def main():

    #This will exit us out if we're not cool

    area_data_menu = AreaDataMenu()
    area_data_menu.do_dependency_check()
    area_data_menu.display_splash_screen()
    stil_running = True
    while stil_running:

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
