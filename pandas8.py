import pandas as pd 
data = { 
    "Name": ['Akshat', 'Arzhel', 'Avon'], 
    "Age": [20, 21, 17],
    "City" : ['Mumbai', 'Guwahati', 'Bangalore']
}
df = pd.DataFrame(data)
print(df) 