class Animal:
    def __init__(self, species, name, age, gender, weight, health_status,
                 location, diet, preferred_food, feeding_schedule, exhibit):
        """ Initialize an Animal object with the given attributes. """
        self.__species = species
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__weight = weight
        self.__health_status = health_status
        self.__location = location
        self.__diet = diet
        self.__preferred_food = preferred_food
        self.__feeding_schedule = feeding_schedule
        self.__exhibit = exhibit

    # Getter methods
    def get_species(self):
        """ Return the species of the animal. """
        return self.__species

    def get_name(self):
        """ Return the name of the animal. """
        return self.__name

    def get_age(self):
        """ Return the age of the animal. """
        return self.__age

    def get_gender(self):
        """ Return the gender of the animal. """
        return self.__gender

    def get_weight(self):
        """ Return the weight of the animal. """
        return self.__weight

    def get_health_status(self):
        """ Return the health status of the animal. """
        return self.__health_status

    def get_location(self):
        """ Return the location of the animal. """
        return self.__location

    def get_diet(self):
        """ Return the diet of the animal. """
        return self.__diet

    def get_preferred_food(self):
        """ Return the preferred food of the animal. """
        return self.__preferred_food

    def get_feeding_schedule(self):
        """ Return the feeding schedule of the animal. """
        return self.__feeding_schedule

    def get_exhibit(self):
        """ Return the exhibit the animal belongs to. """
        return self.__exhibit

    # Setter methods
    def set_age(self, age):
        """ Set the age of the animal. """
        self.__age = age

    def set_weight(self, weight):
        """ Set the weight of the animal. """
        self.__weight = weight

    def set_health_status(self, health_status):
        """ Set the health status of the animal. """
        self.__health_status = health_status

    def set_location(self, location):
        """ Set the location of the animal. """
        self.__location = location

    def set_diet(self, diet):
        """ Set the diet of the animal. """
        self.__diet = diet

    def set_preferred_food(self, preferred_food):
        """ Set the preferred food of the animal. """
        self.__preferred_food = preferred_food

    def set_feeding_schedule(self, feeding_schedule):
        """ Set the feeding schedule of the animal. """
        self.__feeding_schedule = feeding_schedule

    def set_exhibit(self, exhibit):
        """ Set the exhibit the animal belongs to. """
        self.__exhibit = exhibit

    def __str__(self):
        """ Return a string representation of the Animal object. """
        return (f"Species: {self.__species}, Name: {self.__name}, Age: {self.__age}, "
                f"Gender: {self.__gender}, Weight: {self.__weight}, Health Status: {self.__health_status}, "
                f"Location: {self.__location}, Diet: {self.__diet}, Preferred Food: {self.__preferred_food}, "
                f"Feeding Schedule: {self.__feeding_schedule}, Exhibit: {self.__exhibit}")

    def __del__(self):
        """ Print a message when the Animal object is being destroyed. """
        print(f"Animal object '{self.__name}' is being destroyed.")

def main():
    """ Main function. """

    # Create an Animal object
    lion = Animal("Lion", "Simba", 5, "Male", 200, "Healthy", "Enclosure 1", "Carnivore", "Meat",
                  ["Morning", "Evening"], "Serengeti")

    # Access animal attributes using getter methods
    print(lion.get_name())  # Output: Simba
    print(lion.get_exhibit())  # Output: Serengeti

    # Modify animal attributes using setter methods
    lion.set_age(6)
    lion.set_exhibit("African Savanna")
    # Print the animal object
    print(lion)
    # Destroy the animal object
    del lion

if __name__ == "__main__": main()