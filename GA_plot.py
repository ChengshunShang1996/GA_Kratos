import os
import matplotlib.pyplot as plt
import shutil

def creat_folder():

    kratos_pics_folder_name = 'kratos_results_pics'
        
    if os.path.exists(kratos_pics_folder_name):
        shutil.rmtree(kratos_pics_folder_name, ignore_errors=True)
        os.makedirs(kratos_pics_folder_name)
    else:
        os.makedirs(kratos_pics_folder_name)

def plot_every_generation():

    NGEN = 4

    for g_count in range(NGEN):

        aim_folder_name = 'G_' + str(g_count)

        aim_path_and_name = os.path.join(os.getcwd(),'kratos_results_data', aim_folder_name, 'G-Triaxial_Graphs', 'G-Triaxial_graph.grf')

        if os.path.getsize(aim_path_and_name) != 0:
            strain_data_list = []
            stress_data_list = []
            with open(aim_path_and_name, 'r') as stress_strain_data:
                for line in stress_strain_data:
                    values = [float(s) for s in line.split()]
                    strain_data_list.append(values[0]) 
                    stress_data_list.append(values[1] * 1e-6) 

            experiment_strain_data_list = []
            experiment_stress_data_list = []
            with open('usc.dat', 'r') as exp_stress_strain_data:
                for line in exp_stress_strain_data:
                    values = [float(s) for s in line.split()]
                    experiment_strain_data_list.append(values[0]) 
                    experiment_stress_data_list.append(values[1]) 

            
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.plot(strain_data_list, stress_data_list, '--', label='Predicted results')
            ax.plot(experiment_strain_data_list, experiment_stress_data_list, '-', label='Experiment results')
            #plt.title('Legend inside')
            plt.xlabel('Strain / %')  
            plt.ylabel('Stress / MPa') 
            ax.legend()
            fig_name = 'Stress_strain_G' + str(g_count) + '.png'
            fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_pics', fig_name)
            fig.savefig(fig_name_and_path)
        
        else:
            print('No figure generated!')


def plot_final_results():

    aim_strength = 43.23 #MPa
    aim_young_modulus = 5.54  #GPa
    
    read_file_name = 'best_individual_data.txt'
    aim_path_and_name = os.path.join(os.getcwd(),'kratos_results_data', read_file_name)

    if os.path.getsize(aim_path_and_name) != 0:
        generation_id_list = []
        strength_data_list = []
        young_data_list = []
        with open(aim_path_and_name, "r") as f_r:
            for line in f_r:
                values = [float(s) for s in line.split()]
                generation_id_list.append(values[0])
                strength_data_list.append(values[5] * 1e-6) 
                young_data_list.append(values[6] * 1e-9) 

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(generation_id_list, strength_data_list, 'o', label='Predicted strength')
        #plt.title('Legend inside')
        plt.xlabel('Generation')  
        plt.ylabel('Stress / MPa') 
        plt.axhline(y=aim_strength, color='gray', linestyle='-')
        ax.legend()
        fig_name = 'Strength_Generation_total.png'
        fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_pics', fig_name)
        fig.savefig(fig_name_and_path)

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(generation_id_list, young_data_list, 'o', label='Predicted Young modulus')
        #plt.title('Legend inside')
        plt.xlabel('Generation')  
        plt.ylabel('Young modulus / GPa') 
        plt.axhline(y=aim_young_modulus, color='gray', linestyle='-')
        ax.legend()
        fig_name = 'Young_modulus_eneration_total.png'
        fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_pics', fig_name)
        fig.savefig(fig_name_and_path)
    else:
        print('File best_individual_data.grf is empty!')

print('Starting to plot ...')
creat_folder()
plot_every_generation()
plot_final_results()
print('Finish plotting!')
