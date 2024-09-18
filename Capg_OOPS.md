1. **Class**: A blueprint for creating objects that defines a set of attributes and methods.
2. **Object**: An instance of a class that encapsulates data and behavior.
3. **Encapsulation**: The concept of wrapping data and methods into a single unit (class) and restricting access to some of the object's components.
4. **Inheritance**: A mechanism that allows one class to inherit attributes and methods from another class.
5. **Polymorphism**: The ability for different classes to be treated as instances of the same class through a common interface, allowing for method overriding and method overloading.
6. **Interface**: A contract that defines a set of methods that implementing classes must provide, without specifying how they should be implemented.
7. **Abstraction**: The process of hiding complex implementation details and showing only the essential features of an object.
8. **SUPER**: super() is used to call methods from a parent or superclass from within a subclass
```python
# Define a base class to illustrate inheritance, encapsulation, and abstraction
class Animal:
    def __init__(self, name, species):
        self.name = name  # Encapsulation: private attribute
        self.species = species  # Encapsulation: private attribute
    def make_sound(self):
        raise NotImplementedError("Subclasses must implement this method")  # Abstraction
    def __str__(self):
        return f"{self.name} is a {self.species}"


# Define a subclass to demonstrate inheritance and polymorphism
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")  # Inheritance: call the base class constructor
        self.breed = breed  # Encapsulation: private attribute
    def make_sound(self):
        return "Woof!"  # Polymorphism: overriding the base class method
    def __str__(self):
        return f"{self.name} is a {self.breed} {self.species}"


# Define another subclass to demonstrate inheritance and polymorphism
class Cat(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Cat")  # Inheritance: call the base class constructor
        self.breed = breed  # Encapsulation: private attribute
    def make_sound(self):
        return "Meow!"  # Polymorphism: overriding the base class method
    def __str__(self):
        return f"{self.name} is a {self.breed} {self.species}"


# Demonstrate usage
if __name__ == "__main__":
    # Create instances of the Dog and Cat classes
    dog1 = Dog("Buddy", "Golden Retriever")
    cat1 = Cat("Whiskers", "Siamese")

    # Create an instance of the Zoo class and add animals to it
    zoo = Zoo()
    zoo.add_animal(dog1)
    zoo.add_animal(cat1)

    # Show all animals in the zoo
    zoo.show_animals()

    # Demonstrate polymorphism
    for animal in zoo.animals:
        print(f"{animal.name} says {animal.make_sound()}")

```
