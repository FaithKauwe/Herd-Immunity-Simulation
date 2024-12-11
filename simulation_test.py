import pytest
from simulation import Simulation
from virus import Virus

@pytest.fixture
def setup_simulation():
    virus = Virus("Flu", 0.2, 0.1)  # Example virus
    simulation = Simulation(virus, 1000, 0.1, 10)
    return simulation

def test_create_population(setup_simulation):
    simulation = setup_simulation
    population_length = len(simulation.population)
    assert population_length == 1000
    
    vaccinated_count = sum(person.is_vaccinated for person in simulation.population)
    assert vaccinated_count == 100  # 10% of 1000 is 100

def test_survival_after_infection(setup_simulation):
    simulation = setup_simulation
    infected_person = simulation.population[0]
    infected_person.infection = simulation.virus
    survived = infected_person.did_survive_infection()  # Simulate survival check
    
    if not survived:
        infected_person.is_alive = False  # This would align with your implementation context

    assert infected_person.is_alive or infected_person.is_vaccinated  # Should still be alive or vaccinated

# Add more tests as needed

