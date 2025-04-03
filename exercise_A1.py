from collections import defaultdict
from itertools import islice
import os
import heapq






def check_input_validity(file_path, n):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file is invalid")

    if type(n)!=int or n<=0:
        raise ValueError("N is not a positive integer")


def count_errors(lines):
  errors_dict= defaultdict(int)
  for line in lines:
      error_code= int(line[-5:-2])
      errors_dict[error_code]+= 1
  return errors_dict


def count_errors_in_chunks(file_path):
    list_of_errors= []

    with open(file_path, 'r') as file:
        lines= list(islice(file, 1000))
        while lines:
            errors= count_errors(lines)
            list_of_errors.append(errors)
            lines= list(islice(file, 1000))

    return list_of_errors


def merge_dicts(list_of_errors):
    errors_dict= defaultdict(int)

    for errors in list_of_errors:
        for key, count in errors.items():
            errors_dict[key]+= count
    return errors_dict


def n_most_frequent_errors(file_path: str, n: int= 1):

    try:
        check_input_validity(file_path, n)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")

    list_of_errors= count_errors_in_chunks(file_path)
    errors_dict= merge_dicts(list_of_errors)

    if n> len(errors_dict):
        n= len(errors_dict)

    frequent_errors= heapq.nlargest(n, errors_dict, key=errors_dict.get)
    return {key: errors_dict[key] for key in frequent_errors}


def print_errors(errors):
    for key, values in errors.items():
        print(f"Error code: {key}      frequency: {values}")





if __name__=="__main__":
    file_path= "logs.txt"
    n= 3
    errors_dictionary= n_most_frequent_errors(file_path,n)
    print_errors(errors_dictionary)
