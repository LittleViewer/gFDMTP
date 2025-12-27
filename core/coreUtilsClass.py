import pathlib
import sys
import os
import json
import datetime

class my_utils :

    def check_file_exist(self, link):
        handle = pathlib.Path(link)
        return handle.exists()
    
    def error_with_reason(self, reason, to_break = False, code = 1000):
        print(f"[{self.date_}] - Stop Reason: " + reason)
        if to_break == True:
            sys.exit(code)

    def file_open(self, link, mode = "r", encoding_would="utf-8"):
        handle = open(link, mode, encoding=encoding_would)
        return handle
    
    def create_dir(self, link, would_create = True) :
        if would_create == True:
            os.mkdir(link)
        return True
    
    def order_dict(self, items_add_dict, organiser_element, dict_orderized, tick ):
        if tick == 0 :
            dict_orderized[organiser_element] = [items_add_dict]
            return dict_orderized
        
        list_key = list(dict_orderized.keys())
        if organiser_element in list_key :
            dict_orderized[organiser_element].append(items_add_dict)
        else: 
             dict_orderized[organiser_element] = [items_add_dict]
        return dict_orderized
    
    def string_formated_name_file(self, string, unformated_sign = [".", ",",",","'",";", "?", "!",":","-", " ", "/"]):
        string_formated = ""
        for one_sign in string:
            if one_sign in unformated_sign:
                string_formated = string_formated + "_"
            else:
                string_formated = string_formated + one_sign
        return string_formated
    
    def absolute_link(self, link):
            return os.path.join(os.getcwd(), link)
    
    def read_json_file(self, link):
        handle = self.file_open(self.absolute_link(link))
        content =  json.load(handle)
        return content

    def check_is_file_not_nothing(self, content):
        if len(content) == 0:
            return False
        else:
            return True

    def check_is_good_file_config(self, content, rules):
        for one_rule in content:
            if one_rule not in rules:
                return False
        return True
    
    def is_variable_not_used(self, variable, to_break_if_error = True):
        if variable is None:
            self.error_with_reason("Variable not used", to_break_if_error)
            return False
        elif type(variable) != int:
            if len(variable) == 0:
                self.error_with_reason("Variable not used", to_break_if_error)
        return True

    def obtain_value_by_key_dict(self, dict_user, key):
        for one_test in [dict_user, key]:
            self.is_variable_not_used(one_test)
        value =  dict_user[key]
        return value
    
    def is_equal_value_integer(self, integer, equal = 0):
        if integer == equal:
            return True
        return False
    
    def is_list(self, possible_list):
        if type(possible_list) is list:
            return True
        return False

    def __init__(self):
        self.date_ = datetime.datetime.now()