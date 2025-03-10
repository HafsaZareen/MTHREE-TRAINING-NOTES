# #Numpy is fundamental for data analysis in python
# #Numpy is used to create arrays and matrices
# #Numpy is used to perform mathematical operations on arrays and matrices
# #Numpy is used to perform statistical operations on arrays and matrices
# #Numpy is used to perform linear algebra operations on arrays and matrices
# #Numpy is used to perform Fourier transformations on arrays and matrices
# #Numpy is used to perform random number generation on arrays and matrices
# #Numpy is used to perform linear regression on arrays and matrices
# #Numpy is used to perform polynomial regression on arrays and matrices
# #Numpy is used to perform exponential regression on arrays and matrices
# #Numpy is used to perform logarithmic regression on arrays and matrices
# #Numpy is used to perform power regression on arrays and matrices
# #Numpy is used to perform polynomial regression on arrays and matrices
import numpy as np

# #Create an array
# arr = np.array([1, 2, 3, 4, 5])
# arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
# print(arr)
# print(arr_2d)

# #Create an array with random numbers
# arr_random = np.random.rand(3, 4)

# zeros_array = np.zeros((3, 4))
# ones_array = np.ones((3, 4))
# full_array = np.full((3, 4), 10)

# print(arr_random)
# print(zeros_array)
# print(ones_array)
# print(full_array)

# #Create an array with a range of numbers
# arr_range = np.arange(10, 20)
# print(arr_range)

# #Create an array with a range of numbers with a step
# arr_range_step = np.arange(10, 20, 0.5)
# print(arr_range_step)

# #Matrix addition
# matrix_1 = np.array([[1, 2, 3], [4, 5, 6]])
# matrix_2 = np.array([[1, 2, 3], [4, 5, 6]])

# matrix_addition = matrix_1 + matrix_2
# print(matrix_addition,"addition of matrix")

# #Matrix subtraction
# matrix_subtraction = matrix_1 - matrix_2
# print(matrix_subtraction,"subtraction of matrix")

# #Matrix multiplication
# matrix_multiplication = matrix_1 * matrix_2
# print(matrix_multiplication,"multiplication of matrix")

# #Matrix division
# matrix_division = matrix_1 / matrix_2
# print(matrix_division,"division of matrix")

# #Matrix power
# matrix_power = matrix_1 ** matrix_2
# print(matrix_power,"power of matrix")

# #Matrix transpose
# matrix_transpose = matrix_1.T
# print(matrix_transpose,"transpose of matrix")

# # #Matrix dot product
# # matrix_dot_product = np.dot(matrix_1, matrix_2)
# # print(matrix_dot_product,"dot product of matrix")

# #Numpy mean median mode
# arr=[1,2,3,4,5,6,7,8,9,10]
# arr_mean = np.mean(arr)
# arr_median = np.median(arr)

# print(arr_mean,"mean of array")
# print(arr_median,"median of array")

# #Numpy standard deviation and variance
# arr_std = np.std(arr)
# arr_var = np.var(arr)
# print(arr_std,"standard deviation of array")
# print(arr_var,"variance of array")

import pandas as pd

# series = pd.Series([1, 2, 3, 4, 5])
# print(series)

# series_2 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
# print(series_2)

# data = {
#     'Name': ['John', 'Jane', 'Jim', 'Jill'],
#     'Age': [20, 21, 22, 23],
#     'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
# }

# df = pd.DataFrame(data)
# # print(df)

# #Create a dataframe from a csv file
df_csv = pd.read_csv('data.csv')

df_csv = pd.concat([df_csv, df_csv])
print(df_csv)
next_idx = len(df_csv)
print(next_idx)
#Create a dataframe from a sql table
df_csv.loc[next_idx] = ['Ashfdkjshn', 20, 'New York']
print(df_csv)
df_csv.to_csv('data_new.csv', index=False)