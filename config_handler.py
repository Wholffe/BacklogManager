import os


def append_to_backlog_config(config_file, backlog):
    with open(f'config/{config_file}.txt', 'a+') as file:
        csv_string = ';'.join(backlog)
        file.write(f'{csv_string}\n')

def fetch_all_categories():
    predefined_categories = fetch_predefined_categories()
    custom_categories = fetch_custom_categories()

    return [*predefined_categories, *custom_categories]


def fetch_backlogs_from_categories(categories):
    backlogs = {}

    for category in categories:
        config_name = category.lower().replace(" ", "_")
        backlogs[category] = fetch_backlogs_from_file(f'config/{config_name}.txt')

    return backlogs


def fetch_backlogs_from_file(path):
    backlogs = []

    if os.path.exists(path) == False:
        print("The provided path does not exist.")        
        return []

    with open(path, 'r') as file:
        for line in file:
            backlogs.append(line.strip().split(';'))

    return backlogs


def fetch_categories_from_file(path):
    categories = []

    if os.path.exists(path) == False:
        print("The provided path does not exist.")        
        return []

    with open(path, 'r') as file:
        for line in file:
            categories.append(line.strip())

    return categories

def fetch_custom_categories():
    return fetch_categories_from_file('config/custom_categories.txt')

def fetch_predefined_categories():
    return fetch_categories_from_file('config/categories.txt')
