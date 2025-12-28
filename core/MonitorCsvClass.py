import random
import time
import core.coreUtilsClass as cCUC
class monitor_csv :
    def file_name_composer(self):
        unix_time = str(time.time())
        time_reform = unix_time.replace(".", "")
        return f"output\\{time_reform}.dataset.csv"
    
    def basical_verify_json_configuration(self, content, rules):
        is_not_nothing = self.cCUC_obj_.check_is_file_not_nothing(content)
        if is_not_nothing == False:
            self.cCUC_obj_.error_with_reason("Config File Nothing Information", True)
        is_valide_rule  = self.cCUC_obj_.check_is_good_file_config(content, rules)
        if is_valide_rule == False:
            self.cCUC_obj_.error_with_reason("Bad Formating Config File", True)

    def generate_name_company(self, number_company, base_name = "Subway Company"):
        is_zero = self.cCUC_obj_.is_equal_value_integer(number_company)
        if is_zero == True:
            self.cCUC_obj_.error_with_reason("Value Invalide: Define a '0'", True)
        list_name_company = {}
        for tick in range(number_company):
            list_name_company[f"{base_name} {tick+1}"] = []
        return list_name_company

    def generate_world_environnement_economic(self, number_tick_world, range_fluctuation_price, percentage_possible_deflation):
        is_list = self.cCUC_obj_.is_list(range_fluctuation_price)
        if is_list == False:
            self.cCUC_obj_.error_with_reason("Bad Format : Not List", True)
        world_economic_environnement = {}
        for tick in range(number_tick_world):
            if tick == 0:
                world_economic_environnement[tick] = [0, True]
            else: 
                type_evolution =  random.randint(0, 100)
                if type_evolution > percentage_possible_deflation:
                    type_evolution = True #inflation
                else:
                    type_evolution = False #deflation
                world_economic_environnement[tick] = [random.randint(range_fluctuation_price[0], range_fluctuation_price[1]), type_evolution]
        return world_economic_environnement

    def star_price_of_company(self, dict_data, range_start_price):
        for one_company in dict_data:
            dict_data[one_company].append(random.uniform(range_start_price[0], range_start_price[1]))
        return dict_data
    
    def generate_all_data(self, number_tick_world, dict_data, world_economic_environnement, range_noise):
        is_list = self.cCUC_obj_.is_list(range_noise)
        if is_list == False:
            self.cCUC_obj_.error_with_reason("Bad Format : Not List", True)
        for one_company in dict_data:
            for tick in range(number_tick_world):
                noise_value = 0
                if tick != 0:
                    is_noise = random.randint(0, 100)
                    if is_noise >= 99:
                        noise_value = random.randint(range_noise[0], range_noise[1])                        
                    if world_economic_environnement[tick][1] == True:
                        dict_data[one_company].append(base_price+(world_economic_environnement[tick][0]-noise_value))
                    else: 
                        dict_data[one_company].append(base_price-(world_economic_environnement[tick][0]-noise_value))
                    base_price = dict_data[one_company][tick]
                else:
                    base_price = dict_data[one_company][0]
        return dict_data
    
    def print_csv_title_line(self, handle, dict_data):
        title_line = ""
        for one_data in dict_data:
            title_line = title_line+","+one_data
        handle.write(title_line+"\n")

    def print_csv_data_line(self, handle, dict_data):
        for one_tick in range(self.number_tick_world_):
            one_line = ""
            for one_data in dict_data:
                one_line = one_line+","+str(dict_data[one_data][one_tick])
            handle.write(one_line+"\n")

    def sub_pipe_rule_generation (self, link = "config_file/config.json", rules = ["subway company ticket", "number of months of operation","minimum-maximum starting price", "minimum-maximum fluctuation","percentage chance of deflation", "range of noise"]):
        content = self.cCUC_obj_.read_json_file(link)
        self.basical_verify_json_configuration(content, rules)
        number_company = self.cCUC_obj_.obtain_value_by_key_dict(content, "subway company ticket")
        dict_data = self.generate_name_company(number_company)
        number_tick_world = self.cCUC_obj_.obtain_value_by_key_dict(content, "number of months of operation")
        range_start_price = self.cCUC_obj_.obtain_value_by_key_dict(content, "minimum-maximum starting price")
        range_fluctuation_price = self.cCUC_obj_.obtain_value_by_key_dict(content, "minimum-maximum fluctuation")
        percentage_possible_deflation = self.cCUC_obj_.obtain_value_by_key_dict(content, "percentage chance of deflation")
        range_noise = self.cCUC_obj_.obtain_value_by_key_dict(content, "range of noise")
        world_economic_environnement = self.generate_world_environnement_economic(number_tick_world, range_fluctuation_price, percentage_possible_deflation)
        dict_data = self.star_price_of_company(dict_data, range_start_price)
        dict_data = self.generate_all_data(number_tick_world, dict_data, world_economic_environnement, range_noise)
        self.number_tick_world_ = number_tick_world
        return dict_data

    def pipe_generate_file(self):
        dict_data = self.sub_pipe_rule_generation()
        name_file = self.cCUC_obj_.absolute_link(self.file_name_composer())
        is_exist = self.cCUC_obj_.check_file_exist(name_file)
        if is_exist == True:
            self.cCUC_obj_.error_with_reason("File Already Exist!", True)
        else: 
            self.cCUC_obj_.file_open(name_file, "w")
            handle = self.cCUC_obj_.file_open(name_file, "a")
            self.print_csv_title_line(handle, dict_data)
            self.print_csv_data_line(handle, dict_data)

    def __init__(self):
        self.cCUC_obj_ = cCUC.my_utils()
