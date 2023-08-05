import mcutils as mc
import os

def password_validation(input_string):
    if(input_string == input_string.lower()):
        return True
    return False



def manage_dirs():
    dir_manager = mc.Directory_Manager([os.getcwd()])
    dir_manager.filter_format(['txt'])
    dir_manager.print_files_info()
    dir_manager.add_file_to_selection('yes.tx')
    input("Yield")
    selected_files = dir_manager.selected_files
    for file in selected_files:
        file.print_info()
    input("Yield")

# password01 = mc.get_input(format = "Password >> ", return_type=str, valid_options=['>=4'])
# password02 = mc.get_input(format = "Re-Password >> ",validation_function=password_validation)

credits = mc.Credits(["Matias Canepa", "Vicente Correa", "Ignacio Figueroa"],
                     company_name="A Chili Mountain",
                     email_address="macanepa@miuandes.cl",
                     github_account="macanepa")

mf_exit = mc.Menu_Function("Exit App", mc.exit_application, "Exiting App..." )
mf_show_credits = mc.Menu_Function('Credits',credits.print_credits)
mf_manage_dirs = mc.Menu_Function("Manage Dirs",manage_dirs)

menu_create_user = mc.Menu(title="Create User",input_each=True,
                           options={"Name":[str,'>=4'],
                                    "Last_Name":[str],
                                    "Age":[int,'>=18']})
sub_menu02 = mc.Menu(title="Sub Menu Level 02", options=[1,2,3])
sub_menu01 = mc.Menu(title="Sub Menu Level 01", options=[sub_menu02])

menu_main = mc.Menu(title="Main Menu",text="Choose an operation",back = False,
                    options=[menu_create_user, mf_manage_dirs, sub_menu01, mf_show_credits, mf_exit])


while True:
    menu_main.show()
