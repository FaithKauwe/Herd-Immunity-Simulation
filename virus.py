class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        # Define the attributes of your your virus
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate
       


# Test this class
if __name__ == "__main__":
    # Test your virus class by making an instance and confirming 
    # it has the attributes you defined
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    covid = Virus("Covid", 0.6, 0.2)
    assert covid.name == "Covid"
    assert covid.repro_rate == 0.6
    assert covid.mortality_rate == 0.2

    ebola = Virus("Ebola", 0.4, 0.9)
    assert ebola.name == "Ebola"
    assert ebola.repro_rate == 0.4
    assert ebola.mortality_rate == 0.9
