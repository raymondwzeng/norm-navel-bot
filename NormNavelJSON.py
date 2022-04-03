#NormNavelJSON.py

import json

categories_list = []
role_table = {}

#Loads the JSON file into memory. Should only be done during initialization, as the memory will hold the most recent version.
def load_initial() -> None: 
    with open("courses.json", "r") as read_file:
        global role_table
        global categories_list
        role_table = json.load(read_file)
        for category_name in role_table:
            categories_list.append(category_name)

#Saves the JSON file into disk from existing memory. Should be done frequently in case something bad occurs.
def save_data_to_file() -> None:
    with open("courses.json", "w") as write_file:
        json.dump(role_table, write_file)

#Adds a role to a specified category, with an optional link.
#TODO: Add check to make sure you're not overriding over an existing role
#TODO: Also add a parser before command execution to standardize inputs (all caps or all lower)
def add_role_to_category(role_name: str, category_name: str, role_id:str, optional_link:str = "") -> None:
    global role_table
    try:
        category = role_table[category_name]
        if category_name == "majors_and_degrees":
            category[role_name] = role_id
        else:
            category[role_name] = {
                "role": role_id,
                "servers": []
            }
            print(category)
            if(optional_link != ""): #TODO: Maybe add regex parsing for valid discord URLs?
                add_link_to_role(optional_link, role_name, category_name)
        save_data_to_file()
    except KeyError:
        print("[Warning] Error accessing category.")
    print(role_table)

#Adds a link to an existing role. Will NOT create a role if it does not exist.
def add_link_to_role(link: str, role_name: str, category_name: str) -> None:
    if category_name == "majors_and_degrees":
        print("[Warning] Can not add a server to a major or degree!")
        return
    global role_table
    try:
        role_dict = role_table[category_name][role_name]
        role_dict["servers"].append(link)
    except KeyError:
        print("[Warning] Error accessing category or subcategory.")

#Removes a link from an existing role. Should match the existing link exactly.
def remove_link_from_role(link: str, role_name: str, category_name: str) -> None:
    global role_table
    if category_name == "majors_and_degrees":
        print("[Warning] No servers exist in majors and degrees!")
        return
    try:
        role_dict = role_table[category_name][role_name]
        role_dict["servers"].remove(link)
    except KeyError:
        print("[Warning] Could not find link to remove.")

#Removes a role from a category.
def remove_role(role_name: str, category_name: str) -> None:
    global role_table
    try:
        category = role_table[category_name]
        category.pop(role_name)
    except KeyError:
        print("[Warning] Error accessing category.")

#Removes ALL server links. Mind the big red button.
def nuke_servers() -> None:
    global role_table
    for category_name in role_table:
        if category_name != "majors_and_degrees":
            for role_name in role_table[category_name]:
                try:
                    role_table[category_name][role_name]["servers"] = []
                except KeyError:
                    print("[Warning] Unexpected error while deleting. Servers key not found.")

#Returns the roles from a category in a list/array. Mostly for exception handling.
def get_servers_from_role(role_name: str, category_name: str) -> list:
    if category_name == "majors_and_degrees":
        print("[Warning] No servers exist for individual majors or degrees.")
        return []
    try:
        return role_table[category_name][role_name]["servers"]
    except KeyError:
        print("[Warning] Error accessing category or role.")
        return []

#Edits the role of one category by adding a new role, linking the list, then removing the old role.
#Deprecated, do not use. This was done as there is no simple way for the JSON function to modify role names without causing a circular dependency.
# def edit_role_name(role_name: str, new_role_name: str, category_name: str) -> None:
#     global role_table
#     try:
#         if category_name == "majors_and_degrees":
#             role_table[category_name].remove(role_name)
#             role_table[category_name].insert(new_role_name)
#         else:
#             add_role_to_category(new_role_name, category_name)
#             for server in get_servers_from_role(role_name, category_name):
#                 add_link_to_role(server, new_role_name, category_name)
#             remove_role(role_name, category_name)
#     except KeyError:
#         print("[Warning] Error editing category or role.")

#Returns a list of roles within a category.
def get_roles_in_category(category_name: str) -> list:
    try:
        category = role_table[category_name]
        if category_name == "majors_and_degrees":
            return category
        else:
            role_list = []
            for role in category:
                role_list.append(role)
            return role_list
    except KeyError:
        print("[Warning] Unable to find category.")
        return []

#Getter for role_table
def get_role_table() -> dict:
    return role_table

#Getter for categories_list
def get_categories_list() -> list:
    return categories_list

def run_tests():
    #REQUIRED part
    global role_table
    load_initial()
    # print(role_table)
    print("adding role CS141 to role list under UPPER_DIV")
    add_role_to_category("CS141", "upper_div", "<@134542233341223>")
    print("adding role CS010A to role list under lower_div")
    add_role_to_category("CS010A", "lower_div", "<@12331231>")
    print("adding link https://discord.gg/lmao to CS141 under upper_div")
    add_link_to_role("https://discord.gg/lmao", "CS141", "upper_div")
    # print(role_table)
    print("printing list of servers for CS141:")
    print(get_servers_from_role("CS141", "upper_div"))
    print("get list of roles in lower-division")
    print(get_roles_in_category('lower_div'))
    print('removing CS010A from dictionary')
    remove_role("CS010A", "lower_div")
    print("adding random links to CS010B and CS010C, and CS100")
    add_link_to_role("https://discord.gg/lmao", "CS010B", "lower_div")
    add_link_to_role("https://discord.gg/lmao", "CS010C", "lower_div")
    add_link_to_role("https://discord.gg/lmao", "CS141", "upper_div")
    print(role_table)
    print("TACTICAL NUKE, INCOMING")
    nuke_servers()
    print("Final table:", role_table)
    save_data_to_file()
