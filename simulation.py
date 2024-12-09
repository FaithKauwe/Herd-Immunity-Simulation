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

        # Create the population
        self.population = self._create_population()
        
        # Log metadata from logger object's method
        self.logger.write_metadata(pop_size, vacc_percentage, virus.name, virus.mortality_rate, virus.repro_rate)

        # Store newly infected individuals for the time step
        self.newly_infected = []
    
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.        
        
    # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
    def _create_population(self):
        population = []
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        num_unvaccinated = self.pop_size - num_vaccinated
        
        # Create vaccinated individuals
        for i in range(num_vaccinated):
            population.append(Person(i + 1, True))  # Id starts from 1, vaccinated

        # Create unvaccinated individuals
        for i in range(num_unvaccinated):
            population.append(Person(i + 1 + num_vaccinated, False))  # Id continues, unvaccinated

        # Randomly infect the initial infected individuals
        infected_indices = random.sample(range(len(population)), self.initial_infected)
        for index in infected_indices:
            population[index].infection = self.virus  # Infect those individuals

        return population


    
        
        
# This method will return a boolean indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
    def _simulation_should_continue(self):
        living_people = sum(person.is_alive for person in self.population)
        vaccinated_people = sum(person.is_vaccinated for person in self.population)
        return living_people > 0 and (living_people - vaccinated_people) > 0


  # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step.    
    # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue   
    def run(self):
        time_step_counter = 0
        
        while self._simulation_should_continue():
            self.time_step()  # Advance the simulation by one time step
            time_step_counter += 1
        
        # Final log of the simulation results
        living_count = sum(person.is_alive for person in self.population)
        dead_count = sum(not person.is_alive for person in self.population)
        vaccinated_count = sum(person.is_vaccinated for person in self.population)
        self.logger.log_infection_survival(time_step_counter, len(self.population), dead_count)

           

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 

    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        # Reset newly infected list for this time step
        self.newly_infected = []

        for person in self.population:
            if person.is_alive and person.infection:  # Only interact if the person is alive and infected
                for _ in range(100):  # Each infected person interacts with 100 others
                    random_person = random.choice(self.population)
                    self.interaction(person, random_person)

        # Infect newly infected individuals after all interactions
        self._infect_newly_infected()

    def interaction(self, infected_person, random_person):
        if not random_person.is_alive:
            return  # If random person is dead, skip interaction
        
        if random_person.is_vaccinated:
            return  # vaccinated person does not get infected

        if random_person.infection:
            return  # already infected person does not get affected
            
        # Not vaccinated and not infected
        infection_chance = random.random()
        if infection_chance < self.virus.repro_rate:  # Infection occurs
            self.newly_infected.append(random_person)  # Mark the random person to be infected later



    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        pass

    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
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

    # Make a new instance of the imulation
    virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()
