# #Encapsulation : bundling attributes
# class BadBankAccount: 
#     def __init__(self, balance):
#         self.balance = balance 

# # account = BadBankAccount(0.0)
# # account.balance = -1 
# # print(account.balance)

# class BankAccount: 
#     def __init__(self):
#         self._balance = 0.0   # ✅ use _balance (not balance)

#     @property 
#     def balance(self): 
#         return self._balance 

#     def deposit(self, amount): 
#         if amount <= 0: 
#             raise ValueError("Deposit amount must be positive")
#         self._balance += amount 

#     def withdraw(self, amount): 
#         if amount <= 0: 
#             raise ValueError("Withdraw amount must be positive")
#         if amount > self._balance:   # ✅ corrected comparison
#             raise ValueError("Insufficient Funds")
#         self._balance -= amount 


# # --- Testing ---
# account = BankAccount()
# print(account.balance)   # ✅ property accessed without ()
# account.deposit(1.99)
# print(account.balance)
# print(account.withdraw(100))
# print(account.balance)

#Abstraction 
#reduces complexity by hiding unecessary details 

# class EmailServices: 

#     def _connect(self): 
#         print("Connecting to email server....")
    
#     def _authenticate(self): 
#         print("Authenticating...")
        
#     def send_email(self): 
#         self._connect()
#         self._authenticate
#         print("Sending email...")
#         self._disconnect()

#     def _disconnect(self): 
#         print("Disconnecting from email server...")

# email = EmailServices()
# email.send_email()

#Inhertiance : Inheritance is a fundamental concept in oops that involved creating new classes (subclasses or derived classes) based on existing classes(superclasses or base classes)

class Vehicle: 
    def __init__(self, brand, model, year):
        self.brand = brand 
        self.model = model 
        self.year = year

    def start(self): 
        print("Vehicle is starting")
    
    def stop(self): 
        print("Vehicle is stopping")

class Car(Vehicle): 
    def __init__(self, brand, model, year, number_of_doors, number_of_wheels):
        super().__init__(brand, model, year)
        self.number_of_doors = number_of_doors
        self.number_of_wheels = number_of_wheels
    
class Bike(Vehicle): 
    def __init__(self, brand, model, year, number_of_wheels):
        super().__init__(brand, model, year)
        self.number_of_wheels = number_of_wheels

car = Car("Ford", "Focus", "2008", 5, 4)
bike = Bike("Honda", "Scoupy", 2018, 2)
print(car.__dict__) 
print(bike.__dict__)







                