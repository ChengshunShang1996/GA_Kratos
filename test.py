import csv 
import os 

log_output_path_and_name = os.path.join(os.getcwd(),'running_log.txt')
if os.path.exists(log_output_path_and_name):
    os.remove(log_output_path_and_name)
log_export_file = open(log_output_path_and_name, 'a+')

log_export_file.write('Hola Barcelona' + '\n')
log_export_file.write('Hola Barcelona' + '\n')
log_export_file.write('Hola Barcelona' + '\n')
