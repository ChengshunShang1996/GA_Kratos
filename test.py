from distutils.dir_util import copy_tree
import os
import matplotlib.pyplot as plt

generation_id_list = [1,2,3,4,5]
strength_data_list = [1,2,3,4,5]
young_data_list = [1,2,3,4,5]

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(generation_id_list, strength_data_list, 'o', label='Predicted strength')
#plt.title('Legend inside')
plt.xlabel('Generation')  
plt.ylabel('Stress / MPa') 
ax.legend()
fig_name = 'Stress_Generation_total.png'
fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_data', 'kratos_results_pics', fig_name)
fig.savefig(fig_name_and_path)

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(generation_id_list, young_data_list, 'o', label='Predicted strength')
#plt.title('Legend inside')
plt.xlabel('Generation')  
plt.ylabel('Young / GPa') 
ax.legend()
fig_name = 'Young_Generation_total.png'
fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_data', 'kratos_results_pics', fig_name)
fig.savefig(fig_name_and_path)