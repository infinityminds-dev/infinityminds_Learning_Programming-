a = 1
while a !=21:
    print(a)
    a = a +1
    
n = int(input("tell your number"))

while n > 0:
    print(n%10)
    n = n // 10 
    
q = int(input("tell your number"))

rev = 0

while q > 0:
    rev = rev*10 + q%10
    q = q // 10 

print(rev)


q = int(input("tell your number"))
copy = a
rev = 0

while q > 0:
    rev = rev*10 + q%10
    q = q // 10 

if rev == copy:
    print("palindrome")
else:
        print("not palindrome")

