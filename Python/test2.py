n = int(input("tell your number"))

for i in range(1,n+1):
    print(i)

n = int(input("tell your number"))

for i in range(1,n+1):
    print(i)
    
n = int(input("tell your number"))

for i in range(1,11):
    print(f"{n}x{i}={n*i}")
 
s = 0  
n = int(input("tell your number"))

for i in range(1,n+1):
   s = s + i
print(s)

f = 1
n = int(input("tell your number"))

for i in range(1,n+1):
   f = f * i
print(f)
 
n = 10
even_sum = 0
odd_sum = 0

for i in range(1, n + 1):
    if i % 2 == 0:
        even_sum += i  # Even numbers judte jayenge
    else:
        odd_sum += i   # Odd numbers judte jayenge

print("Even sum =", even_sum, ", Odd sum =", odd_sum)
# Output: Even sum = 30 , Odd sum = 25

num = 12
print(f"{num} ke factors hain:")

for i in range(1, num + 1):
    if num % i == 0:  # Agar remainder 0 aaya toh wo factor hai
        print(i, end=" ")
# Output: 1 2 3 4 6 12


num = 6
factor_sum = 0

for i in range(1, num):
    if num % i == 0:
        factor_sum += i

if factor_sum == num:
    print(f"{num} is a Perfect Number")
else:
    print(f"{num} is NOT a Perfect Number")

num = 17
is_prime = True

for i in range(2, num):
    if num % i == 0:
        is_prime = False  # Beech mein kisi ne divide kar diya!
        break

if is_prime and num > 1:
    print(f"{num} is Prime")
else:
    print(f"{num} is NOT Prime")

string = "Python"
reversed_string = ""

for char in string:
    reversed_string = char + reversed_string  # Naya akshar hamesha aage judega

print(reversed_string)
# Output: nohtyP

string = "racecar"
reversed_string = ""

for char in string:
    reversed_string = char + reversed_string

if string == reversed_string:
    print("Palindrome")
else:
    print("Not a palindrome")

text = "P@#yn26at^&i5ve"
chars = 0
digits = 0
symbols = 0

for char in text:
    if char.isalpha():
        chars += 1
    elif char.isdigit():
        digits += 1
    else:
        symbols += 1

print(f"Chars={chars}, Digits={digits}, Symbols={symbols}")
# Output: Chars=8, Digits=3, Symbols=4
