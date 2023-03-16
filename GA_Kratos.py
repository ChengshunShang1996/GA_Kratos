import random
from operator import itemgetter
import os
import shutil
import glob
from time import sleep
#import matplotlib.pyplot as plt
from decimal import Decimal
from distutils.dir_util import copy_tree
 
 
class Gene:
    """
    This is a class to represent individual(Gene) in GA algorithom
    each object of this class have two attribute: data, size
    """
    def __init__(self, **data):
        self.__dict__.update(data)
        self.size = len(data['data'])  # length of gene
 
 
class GA:
    """
    This is a class of GA algorithm.
    """
 
    def __init__(self, parameter):
        """
        Initialize the pop of GA algorithom and evaluate the pop by computing its' fitness value.
        The data structure of pop is composed of several individuals which has the form like that:
        {'Gene':a object of class Gene, 'fitness': 1.02(for example)}
        Representation of Gene is a list: [b s0 u0 sita0 s1 u1 sita1 s2 u2 sita2]
 
        """
        # parameter = [CXPB, MUTPB, NGEN, popsize, low, up]
        self.parameter = parameter
 
        low = self.parameter[4]
        up = self.parameter[5]
 
        self.bound = []
        self.bound.append(low)
        self.bound.append(up)
 
        pop = []
        for i in range(self.parameter[3]):
            geneinfo = []
            for pos in range(len(low)):
                geneinfo.append(random.randint(self.bound[0][pos], self.bound[1][pos]))  # initialise popluation
 
            fitness = self.evaluate(geneinfo)  # evaluate each chromosome
            pop.append({'Gene': Gene(data=geneinfo), 'fitness': fitness})  # store the chromosome and its fitness
 
        self.pop = pop
        self.bestindividual = self.selectBest(self.pop)  # store the best chromosome in the population
        self.clear_old_and_creat_new_kratos_data_folder() # clear old and creat new kratos data folder
        self.aim_strength = parameter[6]
        self.aim_young_modulus = parameter[7]
 
    def evaluate(self, geneinfo):
        """
        fitness function
        """
        x1 = geneinfo[0]
        x2 = geneinfo[1]
        x3 = geneinfo[2]
        x4 = geneinfo[3]
        y = 1 / (x1**2 + x2**2 + x3**3 - x4**4)
        return y
 
    def selectBest(self, pop):
        """
        select the best individual from pop
        """
        s_inds = sorted(pop, key=itemgetter("fitness"), reverse=True)          # from large to small, return a pop
        return s_inds[0]
 
    def selection(self, individuals, k):
        """
        select some good individuals from pop, note that good individuals have greater probability to be choosen
        for example: a fitness list like that:[5, 4, 3, 2, 1], sum is 15,
        [-----|----|---|--|-]
        012345|6789|101112|1314|15
        we randomly choose a value in [0, 15],
        it belongs to first scale with greatest probability
        """
        s_inds = sorted(individuals, key=itemgetter("fitness"),
                        reverse=True)  # sort the pop by the reference of fitness
        sum_fits = sum(ind['fitness'] for ind in individuals)  # sum up the fitness of the whole pop
 
        chosen = []
        for i in range(k):
            u = random.random() * sum_fits  # randomly produce a num in the range of [0, sum_fits], as threshold
            sum_ = 0
            for ind in s_inds:
                sum_ += ind['fitness']  # sum up the fitness
                if sum_ >= u:
                    # when the sum of fitness is bigger than u, choose the one, which means u is in the range of
                    # [sum(1,2,...,n-1),sum(1,2,...,n)] and is time to choose the one ,namely n-th individual in the pop
                    chosen.append(ind)
                    break
        # from small to large, due to list.pop() method get the last element
        chosen = sorted(chosen, key=itemgetter("fitness"), reverse=False)
        return chosen
 
    def crossoperate(self, offspring):
        """
        cross operation
        here we use two points crossoperate
        for example: gene1: [5, 2, 4, 7], gene2: [3, 6, 9, 2], if pos1=1, pos2=2
        5 | 2 | 4  7
        3 | 6 | 9  2
        =
        3 | 2 | 9  2
        5 | 6 | 4  7
        """
        dim = len(offspring[0]['Gene'].data)
 
        geninfo1 = offspring[0]['Gene'].data  # Gene's data of first offspring chosen from the selected pop
        geninfo2 = offspring[1]['Gene'].data  # Gene's data of second offspring chosen from the selected pop
 
        if dim == 1:
            pos1 = 1
            pos2 = 1
        else:
            pos1 = random.randrange(1, dim)  # select a position in the range from 0 to dim-1,
            pos2 = random.randrange(1, dim)
 
        newoff1 = Gene(data=[])  # offspring1 produced by cross operation
        newoff2 = Gene(data=[])  # offspring2 produced by cross operation
        temp1 = []
        temp2 = []
        for i in range(dim):
            if min(pos1, pos2) <= i < max(pos1, pos2):
                temp2.append(geninfo2[i])
                temp1.append(geninfo1[i])
            else:
                temp2.append(geninfo1[i])
                temp1.append(geninfo2[i])
        newoff1.data = temp1
        newoff2.data = temp2
 
        return newoff1, newoff2
 
    def mutation(self, crossoff, bound):
        """
        mutation operation
        """
        dim = len(crossoff.data)
 
        if dim == 1:
            pos = 0
        else:
            pos = random.randrange(0, dim)  # chose a position in crossoff to perform mutation.
 
        crossoff.data[pos] = random.randint(bound[0][pos], bound[1][pos])
        return crossoff
    
    def clear_old_and_creat_new_kratos_data_folder(self):

        kratos_data_folder_name = 'kratos_results_data'
        
        if os.path.exists(kratos_data_folder_name):
            shutil.rmtree(kratos_data_folder_name, ignore_errors=True)
            os.makedirs(kratos_data_folder_name)
        else:
            os.makedirs(kratos_data_folder_name)

        '''
        kratos_pic_folder_name = 'kratos_results_pics'
        aim_path_and_folder = os.path.join(os.getcwd(),'kratos_results_data', kratos_pic_folder_name)
        
        if os.path.exists(aim_path_and_folder):
            shutil.rmtree(aim_path_and_folder, ignore_errors=True)
            os.makedirs(aim_path_and_folder)
        else:
            os.makedirs(aim_path_and_folder)
        '''
    
    def clear_old_and_creat_new_kratos_case_folder(self):

        kratos_case_folder_name = 'Generated_kratos_cases'

        if os.path.exists(kratos_case_folder_name):
            shutil.rmtree(kratos_case_folder_name, ignore_errors=True)
            os.makedirs(kratos_case_folder_name)
        else:
            os.makedirs(kratos_case_folder_name)

        kratos_temp_data_folder_name = 'kratos_results_data_temp'
        
        if os.path.exists(kratos_temp_data_folder_name):
            shutil.rmtree(kratos_temp_data_folder_name, ignore_errors=True)
            os.makedirs(kratos_temp_data_folder_name)
        else:
            os.makedirs(kratos_temp_data_folder_name)

        cases_run_path_and_name = os.path.join(os.getcwd(),'cases_run.sh')
        if os.path.exists(cases_run_path_and_name):
            os.remove(cases_run_path_and_name)

    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + "_" + str(counter) + extension
            counter += 1

        return path
    
    def generate_kratos_cases(self, g_count, nextoff):

        print('Generating kratos cases ...')
        # creat the cases_run.sh
        cases_run_path_and_name = os.path.join(os.getcwd(),'cases_run.sh')
        with open(cases_run_path_and_name, "w") as f_w_cases_run:
            f_w_cases_run.write('#!/bin/bash'+'\n')

            #loop every individual in the pop
            for indiv_ in nextoff:

                Young_mudulus_particle = str(indiv_['Gene'].data[0])
                Young_mudulus_bond     = str(indiv_['Gene'].data[1])
                sigma_max_bond         = str(indiv_['Gene'].data[2])
                cohesion_ini_bond      = str(indiv_['Gene'].data[3])

                #creat new folder
                new_folder_name = 'G' + str(g_count) + '_Ep' + Young_mudulus_particle + '_Eb' + Young_mudulus_bond\
                                + '_Sig' + sigma_max_bond + '_Coh' + cohesion_ini_bond
                aim_path = os.path.join(os.getcwd(),'Generated_kratos_cases', new_folder_name)
                aim_path = self.uniquify(aim_path)
                os.mkdir(aim_path)

                #copy source file
                seed_file_name_list = ['decompressed_material_triaxial_test_PBM_GA_230315.py', 'G-TriaxialDEM_FEM_boundary.mdpa',\
                                        'G-TriaxialDEM.mdpa', 'ProjectParametersDEM.json', 'MaterialsDEM.json', 'run_omp.sh']
                for seed_file_name in seed_file_name_list:
                    seed_file_path_and_name = os.path.join(os.getcwd(),'kratos_seed_files',seed_file_name)
                    aim_file_path_and_name = os.path.join(aim_path, seed_file_name)

                    if seed_file_name == 'MaterialsDEM.json':
                        with open(seed_file_path_and_name, "r") as f_material:
                            with open(aim_file_path_and_name, "w") as f_material_w:
                                for line in f_material.readlines():
                                    if "YOUNG_MODULUS" in line:
                                        line = line.replace("5.0e10", str(Young_mudulus_particle))
                                    if "BOND_YOUNG_MODULUS" in line:
                                        line = line.replace("3.0e8", str(Young_mudulus_bond))
                                    if "BOND_SIGMA_MAX" in line:
                                        line = line.replace("1e5", str(sigma_max_bond))
                                    if "BOND_TAU_ZERO" in line:
                                        line = line.replace("5e5", str(cohesion_ini_bond))
                                    f_material_w.write(line)
                    elif seed_file_name == 'ProjectParametersDEM.json':
                        with open(seed_file_path_and_name, "r") as f_parameter:
                            with open(aim_file_path_and_name, "w") as f_parameter_w:
                                for line in f_parameter.readlines():
                                    f_parameter_w.write(line)
                    elif seed_file_name == 'run_omp.sh':
                        with open(seed_file_path_and_name, "r") as f_run_omp:
                            with open(aim_file_path_and_name, "w") as f_run_omp_w:
                                for line in f_run_omp.readlines():
                                    if "BTS-Q-Ep6.2e10-T1e3-f0.1" in line:
                                        line = line.replace("BTS-Q-Ep6.2e10-T1e3-f0.1", new_folder_name)
                                    f_run_omp_w.write(line)
                    else:
                        shutil.copyfile(seed_file_path_and_name, aim_file_path_and_name) 

                # write the cases_run.sh
                f_w_cases_run.write('cd '+ aim_path + '\n')
                f_w_cases_run.write('sbatch run_omp.sh' + '\n')

    def run_kratos_cases(self):
        print('Running kratos cases ...')
        command_execution = 'sh cases_run.sh'
        os.system(command_execution)
    
    def read_kratos_results_and_add_fitness(self, g_count, nextoff):
        
        print('Reading kratos results and adding fitness ...')
        for indiv_ in nextoff:

            Young_mudulus_particle = str(indiv_['Gene'].data[0])
            Young_mudulus_bond     = str(indiv_['Gene'].data[1])
            sigma_max_bond         = str(indiv_['Gene'].data[2])
            cohesion_ini_bond      = str(indiv_['Gene'].data[3])

            #the strength files
            aim_folder_name = 'G' + str(g_count) + '_Ep' + Young_mudulus_particle + '_Eb' + Young_mudulus_bond\
                            + '_Sig' + sigma_max_bond + '_Coh' + cohesion_ini_bond
            aim_path_and_name = os.path.join(os.getcwd(),'Generated_kratos_cases', aim_folder_name, 'G-Triaxial_Graphs', 'G-Triaxial_graph.grf')

            if os.path.getsize(aim_path_and_name) != 0:
                stress_data_list = []
                with open(aim_path_and_name, 'r') as stress_strain_data:
                    for line in stress_strain_data:
                        values = [float(s) for s in line.split()]
                        stress_data_list.append(values[1]) 
                strength_max = max(stress_data_list)
                rel_error_strength = (strength_max - self.aim_strength)**2
            else:
                strength_max = 0.0
                rel_error_strength = (self.aim_strength)**2

            #the Young modulus files
            aim_path_and_name = os.path.join(os.getcwd(),'Generated_kratos_cases', aim_folder_name, 'G-Triaxial_Graphs', 'G-Triaxial_graph_young.grf')

            if os.path.getsize(aim_path_and_name) != 0:
                young_data_list = []
                with open(aim_path_and_name, 'r') as young_data:
                    for line in young_data:
                        values = [float(s) for s in line.split()]
                        young_data_list.append(values[1]) 
                young_modulus_max = max(young_data_list)
                rel_error_young_modulus = (young_modulus_max - self.aim_young_modulus)**2
            else:
                young_modulus_max = 0.0
                rel_error_young_modulus = (self.aim_young_modulus)**2

            if rel_error_strength + rel_error_young_modulus:
                fitness = 1 / (rel_error_strength + rel_error_young_modulus)
            else:
                fitness = 0

            indiv_['fitness'] = fitness
    
        return nextoff, strength_max, young_modulus_max
    
    def save_and_plot_best_individual_results(self, g_count, best_individual, strength_max, young_modulus_max):
        
        print('Saving and ploting best individual results ...')
        #save data files
        new_file_name = 'best_individual_data.txt'
        aim_path_and_name = os.path.join(os.getcwd(),'kratos_results_data', new_file_name)

        with open(aim_path_and_name, "a+") as f_w:
            f_w.write(str(g_count) + ' ' + str(best_individual['Gene'].data[0])+ ' ' + str(best_individual['Gene'].data[1])+ ' ' + str(best_individual['Gene'].data[2])\
                      + ' ' + str(best_individual['Gene'].data[3]) + ' ' + str(strength_max) + ' ' + str(young_modulus_max) + '\n')
        f_w.close()
        
        #plot and save
        Young_mudulus_particle = str(best_individual['Gene'].data[0])
        Young_mudulus_bond     = str(best_individual['Gene'].data[1])
        sigma_max_bond         = str(best_individual['Gene'].data[2])
        cohesion_ini_bond      = str(best_individual['Gene'].data[3])

        aim_folder_name = 'G' + str(g_count) + '_Ep' + Young_mudulus_particle + '_Eb' + Young_mudulus_bond\
                        + '_Sig' + sigma_max_bond + '_Coh' + cohesion_ini_bond
        ''' It seems we can not save a figure in Linux
        aim_path_and_name = os.path.join(os.getcwd(),'Generated_kratos_cases', aim_folder_name, 'G-Triaxial_Graphs', 'G-Triaxial_graph.grf')

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
            fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_data', 'kratos_results_pics', fig_name)
            fig.savefig(fig_name_and_path)
        
        else:
            print('No figure generated!')
        '''

        #save the best individual case to results folder
        from_directory = os.path.join(os.getcwd(),'Generated_kratos_cases', aim_folder_name)
        to_directory = os.path.join(os.getcwd(),'kratos_results_data', aim_folder_name)

        #TODO: if there is already a same folder, what will happen?
        copy_tree(from_directory, to_directory)

    ''' It seems we can not save a figure in Linux
    def plot_final_results(self):

        read_file_name = 'best_individual_data.grf'
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
            plt.axhline(y=self.aim_strength, color='gray', linestyle='-')
            ax.legend()
            fig_name = 'Strength_Generation_total.png'
            fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_data', 'kratos_results_pics', fig_name)
            fig.savefig(fig_name_and_path)

            fig = plt.figure()
            ax = plt.subplot(111)
            ax.plot(generation_id_list, young_data_list, 'o', label='Predicted Young modulus')
            #plt.title('Legend inside')
            plt.xlabel('Generation')  
            plt.ylabel('Young modulus / GPa') 
            plt.axhline(y=self.aim_young_modulus, color='gray', linestyle='-')
            ax.legend()
            fig_name = 'Young_modulus_eneration_total.png'
            fig_name_and_path = os.path.join(os.getcwd(),'kratos_results_data', 'kratos_results_pics', fig_name)
            fig.savefig(fig_name_and_path)
        else:
            print('No figure generated!')
    '''
    
    def GA_main(self):
        """
        main frame work of GA
        """
        popsize = self.parameter[3]
 
        print("Start of evolution")
 
        # Begin the evolution
        for g in range(NGEN):
 
            #clear old kratos case files and creat new one
            self.clear_old_and_creat_new_kratos_case_folder()
            
            print("############### Generation {} ###############".format(g))
 
            # Apply selection based on their converted fitness
            selectpop = self.selection(self.pop, popsize)
 
            nextoff = []
            while len(nextoff) != popsize:
                # Apply crossover and mutation on the offspring
 
                # Select two individuals
                offspring = [selectpop.pop() for _ in range(2)]
 
                if random.random() < CXPB:  # cross two individuals with probability CXPB
                    crossoff1, crossoff2 = self.crossoperate(offspring)
                    if random.random() < MUTPB:  # mutate an individual with probability MUTPB
                        muteoff1 = self.mutation(crossoff1, self.bound)
                        muteoff2 = self.mutation(crossoff2, self.bound)
                        #fit_muteoff1 = self.evaluate(muteoff1.data)  # Evaluate the individuals
                        #fit_muteoff2 = self.evaluate(muteoff2.data)  # Evaluate the individuals
                        #nextoff.append({'Gene': muteoff1, 'fitness': fit_muteoff1})
                        #nextoff.append({'Gene': muteoff2, 'fitness': fit_muteoff2})
                        nextoff.append({'Gene': muteoff1})
                        nextoff.append({'Gene': muteoff2})
                    else:
                        fit_crossoff1 = self.evaluate(crossoff1.data)  # Evaluate the individuals
                        fit_crossoff2 = self.evaluate(crossoff2.data)
                        #nextoff.append({'Gene': crossoff1, 'fitness': fit_crossoff1})
                        #nextoff.append({'Gene': crossoff2, 'fitness': fit_crossoff2})
                        nextoff.append({'Gene': crossoff1})
                        nextoff.append({'Gene': crossoff2})
                else:
                    nextoff.extend(offspring)

            #generate kratos cases according to pop 
            self.generate_kratos_cases(g, nextoff)

            self.run_kratos_cases()

            #check whether all the kratos cases in this generation finished
            file_num = 0
            time_count = 0
            while file_num != popsize:
                aim_path_and_folder = os.path.join(os.getcwd(),'kratos_results_data_temp')
                file_num = len(glob.glob1(aim_path_and_folder,"*.txt"))
                sleep(12)
                print('-----Waiting for kratos cases -----')
                time_count += 0.2
                print('-------Generation {} cost {} min(s)-------'.format(g, time_count))

            #add fitness to nextoff
            nextoff, strength_max, young_modulus_max = self.read_kratos_results_and_add_fitness(g, nextoff)

            # The population is entirely replaced by the offspring
            self.pop = nextoff
 
            # Gather all the fitnesses in one list and print the stats
            fits = [ind['fitness'] for ind in self.pop]
 
            best_ind = self.selectBest(self.pop)
 
            if best_ind['fitness'] > self.bestindividual['fitness']:
                self.bestindividual = best_ind
                # save the data of the best individual for post processing
                self.save_and_plot_best_individual_results(g, self.bestindividual, strength_max, young_modulus_max)
            else:
                self.save_and_plot_best_individual_results(g, best_ind, strength_max, young_modulus_max)
 
            print("Best individual found is {}, {}".format(self.bestindividual['Gene'].data,
                                                           self.bestindividual['fitness']))
            print("  Max fitness of current pop: {}".format(max(fits)))

        print("------ End of (successful) evolution ------")
 
 
if __name__ == "__main__":
    CXPB, MUTPB, NGEN, popsize = 0.8, 0.1, 5, 20  # popsize must be even number
    aim_strength, aim_young_modulus = 4.323e7, 5.54e9
 
    up = [1e8, 1e8, 1e10, 1e10]  # upper range for variables
    low = [1e5, 1e5, 1e8, 1e8]  # lower range for variables
    parameter = [CXPB, MUTPB, NGEN, popsize, low, up, aim_strength, aim_young_modulus]
    run = GA(parameter)
    run.GA_main()