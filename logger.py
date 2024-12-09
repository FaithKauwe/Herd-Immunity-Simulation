class Logger(object):
    # the file_name passed in as a param will be the same data_file used in the 
    # logger methods below.  That file will persist for the lifespan of the logger objec
    def __init__(self, file_name):
        self.file_name = file_name
        

    # The methods below are just suggestions. You can rearrange these or 
    # rewrite them to better suit your code style. 
    # What is important is that you log the following information from the simulation:
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
            data_file.write(f"Population Size: {pop_size}\tVaccination Percentage: {vacc_percentage}\tVirus Name: {virus_name}\tMortality Rate: {mortality_rate}\tReproduction Rate: {basic_repro_num}\n")
        
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        with open(self.file_name, 'a') as data_file:
            data_file.write(f"Step {step_number}: Interactions: {number_of_interactions}, New Infections: {number_of_new_infections}\n")


        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        # open in append mode
        with open(self.file_name, 'a') as data_file:
            data_file.write(f"Step {step_number}: Population Count: {population_count}, New Fatalities: {number_of_new_fatalities}\n")

