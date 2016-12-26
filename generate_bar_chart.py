import matplotlib.pyplot as plt
import numpy as np
import json
from collections import OrderedDict
from itertools import islice

def parse_data(option):
    bytes_dict = dict()
    lang_count_dict = dict()
    with open("lang_data.jsonl") as lang_data:
        count = 0
        for item in lang_data:
            current_item = json.loads(item)
            for lang, bytes_count in current_item.items():
                if lang not in bytes_dict:
                    bytes_dict[lang] = 0
                if lang not in lang_count_dict:
                    lang_count_dict[lang] = 0

                bytes_dict[lang] += int(bytes_count)
                lang_count_dict[lang] += 1
            
            count+=1

    megabytes_per_repo_lang = dict()
    for lang, bytes_count in bytes_dict.items():
        megabytes_per_repo_lang[lang] = bytes_dict[lang]/lang_count_dict[lang]
    
    ordered_megabytes_per_repo_lang = OrderedDict(sorted(megabytes_per_repo_lang.items(), reverse=True, key=lambda t: t[1]))
    ordered_megabytes_per_repo_lang = OrderedDict(islice(ordered_megabytes_per_repo_lang.items(),10))

    ordered_bytes_dict = OrderedDict(sorted(bytes_dict.items(), reverse=True, key=lambda t: t[1]))
    ordered_bytes_dict = OrderedDict(islice(ordered_bytes_dict.items(),10))

    ordered_lang_count_dict = OrderedDict(sorted(lang_count_dict.items(), reverse=True, key=lambda t: t[1]))
    ordered_lang_count_dict = OrderedDict(islice(ordered_lang_count_dict.items(),10))

    if option == 1:
        ylabel = "Total size in GB"
        objects = tuple(ordered_bytes_dict.keys())
        vals = [x/(1024*1024*1024) for x in ordered_bytes_dict.values()]
        vals = tuple(vals)
    elif option == 2:
        ylabel = "Repos appeared in"
        objects = tuple(ordered_lang_count_dict.keys())
        vals = [x for x in ordered_lang_count_dict.values()]
        vals = tuple(vals)
    else:
        ylabel = "megabytes/repo"
        objects = tuple(ordered_megabytes_per_repo_lang.keys())
        vals = [(x/(1024*1024)) for x in ordered_megabytes_per_repo_lang.values()]
        vals = tuple(vals)

    plot_graph(objects,vals, ylabel)

def plot_graph(objects, vals, ylabel):
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, vals, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)
    plt.xlabel("Programming language")
    plt.show()

if __name__ == "__main__":
    while True:
        try:
            option = int(input("What graph do you want to plot?\n1. Size of code vs programming language\n2. Repos appeared in vs programming language\n3. Megabytes/repo vs programming language\n"))
            if option == 1 or option == 2 or option == 3:
                break
            print("Enter 1, 2 or 3")
        except ValueError as ex:
            print("Invalid input, enter again")

    parse_data(option)