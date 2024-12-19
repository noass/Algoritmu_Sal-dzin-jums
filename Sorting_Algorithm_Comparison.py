import random
import sys
import time
import numpy as np #pip install numpy
import math
import matplotlib.pyplot as graph_lib #pip install matplotlib
from terminaltables import AsciiTable #pip install terminaltables

memory_error_reached = False
two_minutes_reached = False

def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'): #https://handhikayp.medium.com/creating-terminal-progress-bar-using-python-without-external-library-b51dd907129c
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def validation(input_msg: str, expected_answer_1, expected_answer_2, error_msg: str, expected_answer_3= None, range: bool=False) -> str:
    validation = False
    while(validation == False):
        user_input = input(f"{input_msg}").lower()
        if(range == False):
            if(user_input == expected_answer_1 or user_input == expected_answer_2 or user_input == expected_answer_3):
                validation = True
                return user_input
        else:
            if(user_input.isnumeric() and int(user_input) >= expected_answer_1 and int(user_input) <= expected_answer_2):
                validation = True
                return user_input
        
        print(f"{error_msg}")

def pretty_output(message: str, print_ending: bool=True, print_start: bool=True):

    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    border = '=' * max_length
    if(print_start):
        print(border)
    print(message)
    if(print_ending):
        print(border)

def generate_filled_array(size: int) -> list:
    try:
        new_arr = []
        for i in range(size):
            new_arr.append(i)
        random.shuffle(new_arr)

        return new_arr
    except MemoryError:
        print(f"Memory Error, the generation of ", size, "unique number array has lead to a memory error thus this process has been stopped and no new array file has been added!")
        return []

def self_made(arr: list) -> list:
    unsorted_arr = arr
    for i in range(0, (len(unsorted_arr) - 1)):
        for i in range(0, (len(unsorted_arr) - 1)):
            if(unsorted_arr[i + 1] < unsorted_arr[i]):
                temp_elm = unsorted_arr[i]
                unsorted_arr[i] = unsorted_arr[i + 1]
                unsorted_arr[i + 1] = temp_elm
    return unsorted_arr

def quick_sort(array_file): # Atsauce: https://www.geeksforgeeks.org/python-program-for-quicksort/
    def partition(arr, low, high):
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort_helper(arr, low, high):
        while low < high:
            pi = partition(arr, low, high)
            if pi - low < high - pi:
                quicksort_helper(arr, low, pi - 1)
                low = pi + 1
            else:
                quicksort_helper(arr, pi + 1, high)
                high = pi - 1

    quicksort_helper(array_file, 0, len(array_file) - 1)

def python_sort(array):
    array.sort()

def store_array_in_a_file(size: int, preferred_file_name: str=None):
    global memory_error_reached
    try:
        unsorted_array = generate_filled_array(size)
        if(preferred_file_name == None):
            np.save(f"generated_arrays/unsorted_array_10^{int(math.log10(size))}", np.array(unsorted_array))
        else:
            np.save(f"generated_arrays/{preferred_file_name}", np.array(unsorted_array))
    except MemoryError as err:
        memory_error_reached = True
        print("An error has occured whilst generating an array. Error Description: ", err)

def measure_sorting_speed(function: callable, array: list) -> float:
    global memory_error_reached
    global two_minutes_reached
    try:
        start_time = time.time()
        function(array)

        measured_time = (time.time() - start_time)
        if(measured_time > 120):
            two_minutes_reached == True
        return measured_time
    except MemoryError as err:
        memory_error_reached = True
        print("An error has occured whilst sorting an array. Error Description: ", err)

def measure_sorting_algorithm(algorithm_functions: list, from_n: int, to_n: int = None, range_given: bool = False, custom_file_name: str = None) -> list:
    list_of_measured_times = []
    elapsed_time = []
    global two_minutes_reached
    global memory_error_reached

    if(range_given):
        total_iterations = 10 * (to_n - from_n + 1) * len(algorithm_functions)
        to_value = to_n + 1
    else:
        total_iterations = 10 * len(algorithm_functions)
        to_value = from_n + 1
    progress = 1
    
    for functions in algorithm_functions:
        stop_current_algo = False
        for i in range(from_n, to_value):
            if(stop_current_algo == False):
                try_again = True
                while try_again:
                    try:
                        if(custom_file_name):
                            unsorted_array = np.load(f"generated_arrays/{custom_file_name}.npy").tolist()
                        else:
                            unsorted_array = np.load(f"generated_arrays/unsorted_array_10^{i}.npy").tolist()
                        try_again = False
                    except FileNotFoundError:
                        if(custom_file_name):
                            user_input = validation(
                                input_msg="The file name you've provided doesn't exist, would you like to create it? (y/n): ",
                                expected_answer_1="y",
                                expected_answer_2="n",
                                error_msg="Please provide a y or n answer."
                            )
                            if(user_input == "y"):
                                store_array_in_a_file(size=10**i, preferred_file_name=custom_file_name)
                            else:
                                print("Make sure the file name you've provided matches up next time!")
                        else:
                            store_array_in_a_file(size=10**i)
                for x in range(0, 10):
                    array = unsorted_array.copy()
                    if(two_minutes_reached and x >= 2 or memory_error_reached):
                        print()
                        print(f"The algorithm got cut short: Memory error reached({memory_error_reached}), two minutes passed({two_minutes_reached})")
                        stop_current_algo = True
                        break

                    elapsed_time.append(measure_sorting_speed(functions, array)) 
                    progress_bar(progress, total_iterations, prefix="Progress:", suffix="Complete", length=50)
                    progress += 1
                
                total_time = 0
                for i in elapsed_time:
                    total_time = total_time + i
                list_of_measured_times.append({
                        "algorithm": functions.__name__,
                        "time intervals (s)": [f"{x:.3f}" for x in elapsed_time],
                        "average time (s)": round(total_time / len(elapsed_time), 6),
                        "size": len(array)
                })
                elapsed_time.clear()

    return list_of_measured_times

def display_algorithm_data_in_a_graph(algorithm_data: list):
    all_self_made_results = []
    all_quick_sort_results = []
    all_python_sort_results = []
    for element in algorithm_data:
        if(element["algorithm"] == "self_made"):
            all_self_made_results.append(element)
        elif(element["algorithm"] == "quick_sort"):
            all_quick_sort_results.append(element)
        elif(element["algorithm"] == "python_sort"):
            all_python_sort_results.append(element)
    
    if(len(all_self_made_results) > 0):
        self_made_x = []
        self_made_y = []
        for measurement in all_self_made_results:
            self_made_x.append(f'10^{int(math.log10(measurement["size"]))}')
            self_made_y.append(measurement["average time (s)"])

        graph_lib.plot(self_made_x, self_made_y, label='Self Made')

    if(len(all_quick_sort_results) > 0):
        quick_sort_x = []
        quick_sort_y = []
        for measurement in all_quick_sort_results:
            quick_sort_x.append(f'10^{int(math.log10(measurement["size"]))}')
            quick_sort_y.append(measurement["average time (s)"])
        graph_lib.plot(quick_sort_x, quick_sort_y, label='Quick Sort')

    if(len(all_python_sort_results) > 0):
        python_sort_x = []
        python_sort_y = []
        for measurement in all_python_sort_results:
            python_sort_x.append(f'10^{int(math.log10(measurement["size"]))}')
            python_sort_y.append(measurement["average time (s)"])
        graph_lib.plot(python_sort_x, python_sort_y, label='Python Sort')

    if(len(all_python_sort_results) > 0 or len(all_quick_sort_results) > 0 or len(all_quick_sort_results) > 0):
        graph_lib.title("Algorithm Measurement Graph")
        graph_lib.xlabel("Size")
        graph_lib.ylabel("Average Time (s)")
        graph_lib.legend()
        graph_lib.show()
    else:
        print("Something went wrong no sorting results were given!")

config = {
    "Sorting Functions: ": [python_sort, quick_sort],
    "From 10^: ": 2,
    "To 10^: ": 8,
    "Range: ": True,
    "Custom File Name: ": None
}
user_has_choices = True
while(user_has_choices):
    pretty_output(
    f"""This is the current config: 
Sorting Functions: {[functions.__name__ for functions in config["Sorting Functions: "] ]}
From 10^: {config["From 10^: "]}
To 10^: {config["To 10^: "]}
Use given from to as range: {config["Range: "]}
Custom array file name: {config["Custom File Name: "]}"""
)

    user_input = validation(input_msg="Would you like to edit this config?: (y/n)",
                            expected_answer_1="y",
                            expected_answer_2="n",
                            error_msg='Please provide a y or n answer')
    
    if(user_input == "n"):
        user_has_choices = False
        break
    else:
        cfg_len = len(config)
        user_input = validation(input_msg=f"Which one of these values do you want to change?: (1 - {len(config)}) (or type 0 if you wish to start)",
                                expected_answer_1=0,
                                expected_answer_2=cfg_len , #nevar izmantot f"{len(config)}", jo tas ir <class 'set'> type?
                                error_msg=f"Please provide an answer that's between 0 and {len(config)}",
                                range= True)
        if(int(user_input) == 0):
            user_has_choices = False
            break
        elif(int(user_input) == 1):
            pretty_output("You've choosen to change algorithm functions (Note: There are only 3 functions provided)", print_ending= False)
            user_done = False
            while(user_done == False):
                user_input = validation(input_msg=f"Would you like to remove or add a function (if ur done type back): ",
                                        expected_answer_1="remove",
                                        expected_answer_2="add",
                                        expected_answer_3= "back",
                                        error_msg=f"Type remove, add or back")
                
                if user_input == "add":
                    pretty_output("Here are all the functions that you can add: ", print_ending=False)
                    function_listing = []

                    if "self_made" not in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(self_made)
                        print(f'{len(function_listing)}. self_made')
                    if "quick_sort" not in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(quick_sort)
                        print(f'{len(function_listing)}. quick_sort')
                    if "python_sort" not in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(python_sort)
                        print(f'{len(function_listing)}. python_sort')
                    
                    if(len(function_listing) == 0):
                        print("There are no functions for you to add!")
                        user_done = True
                    else: 
                        user_input = validation(input_msg=f"Which function would you like to add (or type 0 if you changed ur mind): ",
                                                expected_answer_1=0,
                                                expected_answer_2=len(function_listing),
                                                error_msg=f"Provide the correct function number that you would like to add!",
                                                range= True)
                        if(int(user_input) == 0):
                            user_done = True
                        else:
                            config["Sorting Functions: "].append(function_listing[int(user_input) - 1])
                            print("Sucessfully added function: ", function_listing[int(user_input) - 1].__name__)

                elif user_input == "remove":
                    pretty_output("Here are all the functions that you can remove: ", print_ending=False)
                    function_listing = []

                    if "self_made" in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(self_made)
                        print(f'{len(function_listing)}. self_made')
                    if "quick_sort" in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(quick_sort)
                        print(f'{len(function_listing)}. quick_sort')
                    if "python_sort" in [functions.__name__ for functions in config["Sorting Functions: "]]:
                        function_listing.append(python_sort)
                        print(f'{len(function_listing)}. python_sort')
                    
                    if(len(function_listing) == 0):
                        print("There are no functions for you to remove!")
                        user_done = True
                    else: 
                        user_input = validation(input_msg=f"Which function would you like to remove (or type 0 if you changed ur mind): ",
                                                expected_answer_1=0,
                                                expected_answer_2=len(function_listing),
                                                error_msg=f"Provide the correct function number that you would like to add!",
                                                range= True)
                        if(int(user_input) == 0):
                            user_done = True
                        else:
                            config["Sorting Functions: "].remove(function_listing[int(user_input) - 1])
                            print("Sucessfully removed function: ", function_listing[int(user_input) - 1].__name__)
            
                else:
                    user_done = True
                    break
        
        elif(int(user_input) == 2):
            pretty_output("You've choosen to change configs From 10^ value (note this value must be less than To 10^ value)", print_ending= False)
            user_input = validation(input_msg = f'Pick a value from 2 to {config["To 10^: "] - 1}: ',
                                    expected_answer_1=2,
                                    expected_answer_2=(config["To 10^: "] - 1),
                                    error_msg=f'Incorrect value Pick a value from 2 to {config["To 10^: "] - 1}',
                                    range= True)
            
            if(int(user_input) == 0):
                user_done = True
            else:
                config["To 10^: "] = int(user_input)

        elif(int(user_input) == 3):
            pretty_output("You've choosen to change configs To 10^ value (note this value must be more than From 10^ value)", print_ending= False)
            user_input = validation(input_msg = f'Pick a value from {config["From 10^: "] + 1} to 15 (recommended below 8): ',
                                    expected_answer_1=(config["From 10^: "] + 1),
                                    expected_answer_2=15,
                                    error_msg=f'Incorrect value Pick a value from {config["From 10^: "] + 1} to 15',
                                    range= True)
            
            if(int(user_input) == 0):
                user_done = True
            else:
                config["To 10^: "] = int(user_input)

        elif(int(user_input) == 4):
            pretty_output("You've choosen to change configs range value (note if this value is false then the selected algorithms will measure speed only on From 10^ size)", print_ending= False)
            user_input = validation(input_msg = f'Type True or False: ',
                                    expected_answer_1="true",
                                    expected_answer_2="false",
                                    error_msg=f'Incorrect type True or False')
            
            if(user_input.lower() == "true"):
                config["Range: "] = True
            else:
                config["Range: "] = False
        
        elif(int(user_input) == 5):
            pretty_output("You've choosen to change configs custom array file value (note if this value is set then the selected algorithms will measure speed by sorting the provided array file.)", print_ending= False)
            user_input = input("Provide file name : (note this file must be placed inside the working folder, also if you changed ur mind type none): ")
            
            if(user_input.lower() != "none"):
                config["Custom File Name: "] = user_input


algorithm_data = measure_sorting_algorithm(algorithm_functions= config["Sorting Functions: "], from_n= config["From 10^: "],
                                  to_n= config["To 10^: "], range_given= config["Range: "], custom_file_name= config["Custom File Name: "])

table_data = [
    ["Sorting function", "array size", "time intervals (s)", "average time (s)"],     
]

for instance in algorithm_data:
    row = [
        instance["algorithm"],
        instance["size"],
        instance["time intervals (s)"],
        instance['average time (s)']
    ]
    table_data.append(row)

print()
table = AsciiTable(table_data)
print(table.table)

display_algorithm_data_in_a_graph(algorithm_data= algorithm_data)

#dependencies: #pip install terminaltables
               #pip install matplotlib
               #pip install numpy
