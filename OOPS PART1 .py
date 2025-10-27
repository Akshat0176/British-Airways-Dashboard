# class Dog: 
#     def bark(self):
#         print("Whoof, whoof!")

# dog1= Dog() #dog1 is variable Dog is assigned to the variable to call
# dog1.bark() #to call

# class Dog: 
#     def __init__(self, name, breed, owner):
#         self.name = name
#         self.breed = breed
#         self.owner = owner

#     def bark(self):
#         print("Whoof, whoof!")

# class Owner: 
#     def __init__(self, name, address, contact_no):
#         self.name = name 
#         self.address = address 
#         self.phone_number = contact_no
        

        
# owner1 = Owner("Danny", "122 springfield avenue", "888-999")
# dog1 = Dog("Bruce", "Scottish Terrier", owner1)
# # dog1.bark()
# # print(dog1.name)
# # print(dog1.breed)
# print(dog1.owner.name)

# owner2 = Owner("Sally", "122 springfield avenue", "888-999")
# dog2 = Dog("Freya", "Husky", owner2)
# # dog2.bark()
# # print(dog2.name)
# # print(dog2.breed)
# print(dog2.owner.name)

# class Person: 
#     def __init__(self, name, age):
#         self.name = name 
#         self.age = age

#     def greet(self):
#         print(f"My name is {self.name} and I am {self.age} years old.")

# person_1 = Person("Alice", 30)
# person_1.greet()
# person_2 = Person("Ammar", 28)
# person_2.greet()

# class User: 
#     def __init__(self, username, email, password):
#         self.username = username 
#         self._email = email #underscore makes the data protected
#         self.__password = password #double underscore makes it private and we cant access it 
    
#     def get_password(self): 
#         return self.__password
    
#     def set_password(self, new_password): 
#         self.__password = new_password


#     # def say_hi_to_user(self, user): 
#     #     print(f"Message to {user.username}: Hi {user.username}, it's {self.username}")
#     # def clean_email(self): 
#     #     return self._email.lower().strip()
# user1 = User("danthea", "dan@gmail.com", "123")
# user2 = User("batman", "batma@outlook.com", "abc")
# # user1.say_hi_to_user(user2)
# #modify values  
# # print(user1.__password) #cant access it 
# # print(user1.clean_email())

#getter setter property
# class User: 
#     def __init__(self, username, email, password):
#         self.username = username 
#         self._email = email #protected
#         self.password = password 

#     @property  #to read
#     def email(self): 
#         print("Email accessed")
#         return self._email
    
#     @email.setter #to modify
#     def email(self, new_email): 
#         if "@" in new_email: 
#             self._email = new_email


    
# user1 = User("danthea", "dan@gmail.com", "123")
# print(user1.email) 

#static attributes 
#A static attribute (sometimes called a class attribute) is an attribute that belongs to the class itself, not to any specific instance of the class 
#shared by all instances or objects of the class 

# class User: 
#     user_count = 0 

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email 
#         User.user_count += 1 

#     def display_user(self): 
#         print(f"Username : {self.username}, Email : {self.email}")
    
# user1 = User("danthea", "dan@gmail.com")
# user2 = User("sally123", "sally@gmail.com" )
# print(User.user_count)
# print(user1.user_count)   
# print(user2.user_count) 

class BankAccount: 
    MIN_BALANCE = 100 

    def __init__(self, owner, balance=0): 
        self.owner = owner 
        self._balance = balance

    def deposit(self, amount): 
        if self._is_valid_amount(amount):
            self._balance += amount
            # print(f"{self.owner}'s new balance: ${self._balance}")
            self.__log_transaction("deposit", amount)
        else: 
            print("Deposit amount must be positive") 
    
    def _is_valid_amount(self, amount): #protected method
        return amount > 0
    
    def __log_transaction(self, transaction_type, amount): #private amount
        print(f"Logging {transaction_type} of ${amount}")

    @staticmethod
    def is_valid_interest_rate(rate): 
        return 0 <= rate <= 5
    

# Create object and test
account = BankAccount("Alice", 500)
account.deposit(200)
print(BankAccount.is_valid_interest_rate(3))
print(BankAccount.is_valid_interest_rate(10))

