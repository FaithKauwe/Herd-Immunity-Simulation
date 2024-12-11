import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        
        # Initialize the logger object
        self.logger = Logger('simulation_log.txt')

        # call create_population and store the returned list in population
        self.population = self._create_population()
        
        # Log metadata from logger object's method
        self.logger.write_metadata(pop_size, vacc_percentage, virus.name, virus.mortality_rate, virus.repro_rate)

        # Store newly infected individuals for the time step
        self.newly_infected = []
        self.time_step_counter = 0
        self.vaccination_saved_count = 0
        self.total_interactions = 0
        self.total_infections = 0
    
       
    
    # leading underscore in method name lets devs know this is a private method, intended for use
    # only in this class
    def _create_population(self):
        population = []
        # cast to int so I only get whole numbers
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        num_unvaccinated = self.pop_size - num_vaccinated
        
        # Create vaccinated individuals using num_vaccinated as the range. For each Person object,
        # create an id (i + 1), set vaccinated attribute to True, infection attribute defaults to None
        for i in range(num_vaccinated):
            population.append(Person(i + 1, True))  # Id starts from 1, vaccinated

        # Create unvaccinated individuals, id adds onto num_vaccinated to ensure no duplicate ids
        for i in range(num_unvaccinated):
            population.append(Person(i + 1 + num_vaccinated, False))  

        # Randomly infect the initial infected individuals, by creating range of indices. use random.sample() 
        # to return infected indices, stored in infected_indices. use initial_infected to determine how large the sample is
        # loop through infected_indices and retrieve Person object at that index in population array.
        # change the infection attribute of Person object from 'none' to 'virus' object
        infected_indices = random.sample(range(len(population)), self.initial_infected)
        for index in infected_indices:
            population[index].infection = self.virus  
        # now population is a list of Person objects, vaccinated and un, with a random selection of Person objects whos
        # infection attribute is now set to 'virus'
        return population
  
# This method will return a boolean indicating if the simulation should continue. 
    def _simulation_should_continue(self):
        # use built in fucntion to iterate through population and sum all Person objects
        # where is_alive is True. sum() treats True as 1 and False as 0
        living_people = sum(person.is_alive for person in self.population)
        vaccinated_people = sum(person.is_vaccinated for person in self.population)
        # return a boolean value based on 2 conditions. 1st, checks if there are living people who are
        # possibly still spreading virus. 2nd, checks if there are living people whho are not vaccinated
        # if both checks are True, it inidcates that there unvacc persons who can contact virus or spread it
        # and simulation should continue. 
        return living_people > 0 and (living_people - vaccinated_people) > 0

    
    # no leading underscore in function name lets devs know this is a public method and meant to be accessed 
    # by anyone using a Simulation instance
    def run(self):
        # time_step represents one iteration of the simulation
        
        
        while self._simulation_should_continue():
            # Advance the simulation by one time step
            self.time_step()  
            self.time_step_counter += 1
        
        # Final log of the simulation results, initial logging takes place when the Simulation object is first
        # instantiated, with self.logger.write_metadata
        living_count = sum(person.is_alive for person in self.population)
        dead_count = sum(not person.is_alive for person in self.population)
        vaccinated_count = sum(person.is_vaccinated for person in self.population)
        self.logger.answers_log(
        self.pop_size,
        self.time_step_counter,
        self.total_interactions,
        dead_count,
        vaccinated_count,
        self.total_infections,
        self.virus.name,
        self.virus.mortality_rate,
        self.virus.repro_rate,
        self.initial_infected,
        self.vaccination_saved_count
    )


       

 # This method will simulate interactions between people, calulate 
 # new infections, and determine vaccinations and fatalities from infections
    def time_step(self):        
        # Reset newly infected list for this time step, capturing only newly infected during the 
        # current iteration
        self.newly_infected = []
        total_step_interactions = 0
        new_infections_count = 0
        surviving_count = 0
        # loop through population array
        for person in self.population:
            if person.is_alive and person.infection:  # Only interact if the person is alive and infected
                # underscore _ can be used as variable name when the variable is never referenced during the 
                # loop and is only used once to trigger the loop
                for _ in range(100):  # Each infected person interacts with 100 others
                    random_person = random.choice(self.population)
                    self.interaction(person, random_person)
                    total_step_interactions += 1
                    self.total_interactions += 1
        new_infections_count = len(self.newly_infected)
        # update the cumulative infections across the simulation
        self.total_infections += new_infections_count

        # after all interactions, check for survival of infected persons
        for person in self.population:
            if person.is_alive and person.infection:
                survived = person.did_survive_infection()

                if not survived:
                   # change the is_alive flag to False 
                    person.is_alive = False
                else: 
                    surviving_count += 1

        # Infect newly infected individuals after all interactions
        self._infect_newly_infected()

        infection_survival_rate = surviving_count/ len(self.newly_infected) if self.newly_infected else 0

        # Log this step's interactions and survival data
        self.logger.log_interactions(self.time_step_counter, total_step_interactions, new_infections_count, infection_survival_rate)


    def interaction(self, infected_person, random_person):
        # If random person is dead, skip interaction
        if not random_person.is_alive:
            return  
        # vaccinated person does not get infected
        if random_person.is_vaccinated:
            self.vaccination_saved_count += 1
            return  
        # already infected person does not get affected
        if random_person.infection:
            return      
        # Not vaccinated and not infected
        infection_chance = random.random()
        # Infection occurs
        if infection_chance < self.virus.repro_rate:  
        # Mark the random person to be infected at the end of the time_step 
            self.newly_infected.append(random_person)  

# infect newly_infected Persons by changing infection attribute to 'virus'
    def _infect_newly_infected(self):        
        for person in self.newly_infected:
            person.infection = self.virus
        


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()


