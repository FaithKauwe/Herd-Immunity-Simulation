class Logger(object):
    # the file_name passed in as a param will be the same data_file used in the 
    # logger methods below.  That file will persist for the lifespan of the logger objec
    def __init__(self, file_name):
        self.file_name = file_name
        

    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.
    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude: 
    #   The population size, the number of living, the number of dead, and the number 
    #   of vaccinated people at that step. 
    # When the simulation concludes you should log the results of the simulation. 
    # This should include: 
    #   The population size, the number of living, the number of dead, the number 
    #   of vaccinated, and the number of steps to reach the end of the simulation. 

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # open in write mode which overwrites any previous data so this method can only be called
        # once and must be called before the other 2 logger methods
        with open(self.file_name, 'w') as data_file:
            data_file.write(f"Population Size: {pop_size}\n")
            data_file.write(f"Vaccination Percentage: {vacc_percentage}\n")
            data_file.write(f"Virus Name: {virus_name}\n")
            data_file.write(f"Mortality Rate: {mortality_rate}\n")
            data_file.write(f"Reproduction Rate: {basic_repro_num}\n")
        

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections, infection_survival_rate=None):
        with open(self.file_name, 'a') as data_file:
            data_file.write(f"======================================\n")
            data_file.write(f"Step: {step_number}\n")
            data_file.write(f"Total interactions: {number_of_interactions}\n")
            data_file.write(f"Total new infections: {number_of_new_infections}\n")
            if infection_survival_rate is not None:  # Optional logging
                data_file.write(f"Infection Survival Rate: {infection_survival_rate:.2f}\n")
            data_file.write(f"======================================\n")

    def answers_log(self, pop_size, time_step_counter, total_interactions, dead_count, vaccinated_count, total_infections, virus_name, mortality_rate, repro_rate, initial_infected, vaccine_saves):
        with open("answers.txt", "w") as log: 
            log.write(f"""
    What were the inputs you gave the simulation? (Population size, percent vaccinated, virus name, mortality rate, reproductive rate)
    Initial population size: {pop_size}
    Vaccination percentage: {round(vaccinated_count/ pop_size * 100)}%
    Name of the virus: {virus_name}
    Mortality rate: {mortality_rate}
    Reproductive rate of {virus_name} was: {repro_rate}
    Total initial infected: {initial_infected}

    What percentage of the population died from the virus?
    About {round((dead_count / pop_size) * 100)}% of the population died from the virus.

    What percentage of the population became infected at some point before the virus burned out?
    About {round((total_infections / pop_size) * 100)}% of the population became infected at some point before the virus burnt out.

    Out of all interactions sick individuals had during the entire simulation, how many times, in total, did a vaccination save someone from potentially becoming infected?
    The total times a vaccine saved a sick individual was: {vaccine_saves}

    Total steps: {time_step_counter}
    Total interactions: {total_interactions}
    Total people dead: {dead_count}
    Total vaccinated: {vaccinated_count}
    Total infections: {total_infections}
    """)

