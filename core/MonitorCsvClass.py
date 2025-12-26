import csv
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

    def sub_pipe_rule_generation (self, link = "config_file/config.json", rules = ["subway company ticket", "number of months of operation","minimum-maximum starting price", "minimum-maximum fluctuation","percentage chance of deflation"]):
        content = self.cCUC_obj_.read_json_file(link)
        self.basical_verify_json_configuration(content, rules)
        number_company = self.cCUC_obj_.obtain_value_by_key_dict(content, "subway company ticket")
        dict_data = self.generate_name_company(number_company)

    def pipe_generate_file(self):
        self.sub_pipe_rule_generation()
        name_file = self.cCUC_obj_.absolute_link(self.file_name_composer())
        is_exist = self.cCUC_obj_.check_file_exist(name_file)
        if is_exist == True:
            self.cCUC_obj_.error_with_reason("File Already Exist!", True)
        else: 
            self.cCUC_obj_.file_open(name_file, "w")


    def __init__(self):
        self.cCUC_obj_ = cCUC.my_utils()
