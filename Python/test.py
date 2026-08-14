print("Pankaj")

#it all starting here

GOD = 100
B = -50
A = 6.0 
C = 12/2
D = 1999 + 5j
E = True

print(A,B,GOD)

print(type(A))

print(type(B))

print(type(GOD))

print(type(C))

print(type(D))

print(type(E))

""" CCTV LOG """

Storage = 'System is online man "No is not online pls try again"'

print(Storage)

#WOW THIS IS AMAZING

a = "p"
b = "pubajbnjkca76j"
c ="hloKINGkl"
d = "o'w2a6a4y7j9j2hner"
e = "hlo58292"

print(ord(a))

print(b[0], b[3], b[6], b[8], b[10], b[13])

print(c[3:7])

print(d[0 : 14 : 2])

print(e[: :])

# now see this

z = "45"
z = int(z)

print(type(z))

u = 8.0
u = int(u)

print(type(u))

p="8.0"
p = float(p)

print(type(p))


t = "72"
t = float(t)

print(type(t))

print(p, u, z, t)

y = 34
i = 45 + 6j
k = 4.00

y = str(y)
i = str(i)
k = str(k)

print(type(y))

print(y,i,k)

qa= "a"
ui = 0.0

print(bool(qa))
print(bool(ui))

pa = 5

print(pa/2)

# Chapter 5

name = "pankaj"
age = 17

print(f"my name is {name} and my age is {age}")

user = input("what is your name:")
password = int(input("what is your password:"))

print("user name is",user,"and password is",password*5)

X = 5
Y = 8

print(X/2)
print(Y//4)

print (7**168)

print(25%7)

#bond mass rule :
    
print(3+4*2)
print(15//4+15%4)
print(3+2 **2*5-1)

# comparison

print(34 == 34)
print(78 > 77)
print(45 < 30)
print(67 >= 67)
print(89 <= 56)

print(23 != 23)
print(45 != 79)

# and or not

print(35==46 and 35==35)#false

print(35==46 or 35==35)#true

print(not 35==35)#oppsite


a = 10

a += 20 

print(a)

#conditions

num1 = int(input(" Entet first number:"))
num2 = int(input(" Entet second number:"))

if num1 > num2:
        print(f"{num1} is gearter then {num2}")
elif num1 == num2:      
     print(f"{num1} are both are same {num2}")
else:
           print(f"{num2} is gearter then {num1}")
           
#test2

gen = input("Enter your gender:")
              
if gen == "M" or gen =="m":  
    print("hello sir")
    
elif gen == "F" or gen =="f":
     print("hello man")
else:     
    print("other")
    
a = int(input("pls enter number"))

if a%2 ==0:
    print("it is even number")
else:
        print("it is not even number it is odd number")
        
#test3

name = input("Enter your name")
money =int(input("Enter your money"))

if money > 1200:
    print(f"{name} buy this")
else:
        print(f"{name} you need only {1200 - money}")
       
year = int(input("enter year"))

if year% 100== 0 and year%400 == 0:
    print ("it is leap year")
elif year%100 != 0 and year %4 == 0:
        print("it leap year ")
else:
        print("it is not leap year")
        
#test4

temp = int(input("enter yout temp"))
  
if temp >= -5 and temp <=5:
    print("very cold")
elif temp >=6 and temp <=18:
     print("cold")
elif temp >= 19 and temp <=30:
     print("hot")
else:
     print("very hot")
     
# loops
for i in range(10,21,1):
      print(i)
      
for v in range(5,51,5):
      print(v)
      
n = int(input("enter number"))

for o in range(n,(n*10)+1,n):
      print(o)
 
m = "INFINITY"
for x in range(len(m)):
     print(f"{x} : {m[x]}")
     
for q in range(1,12,1):
   if q == 5:
      break
   print(q)
   
for t in range(1,12,1):
  if t == 5:
      continue
  print(t)
   
for e in range(1,12,1):
    if e == 5:
      break
    print(e)
else:
         print("whyd")
 
for t in range(1,12,1):
  if t == 5:
      continue
  print("pankaj")