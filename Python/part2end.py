a = int(input("enter number"))
b = int(input("enter number"))

try:
    print(a/b)
except Exception  as err:
        print(f"error found {err}")
else:
        print("no error found")
finally:
        print("i am king")
        
print("all work ")

#raise
"""
age = int(input("enter your age"))

if age < 18:
    raise TypeError("nikale")
    
print("welcome")

"""
#file handing

#open("hello.txt","x")

#file = open("king.txt", "w")
#data = input("what you want to write")

#file.write(data)

#file2 = open("king.txt", "r")

#print(file2.read())

with open("king.txt","a") as f:
    f.write(" " + "king never did")
