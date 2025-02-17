#float->str->float
#преобразование
num = 3.14
num_str = str(num)
print(f"число в строку: {num_str}, тип: {type(num_str)}")

num2 = float(num_str)
print(f"из строки в число: {num2}, тип: {type(num2)}")