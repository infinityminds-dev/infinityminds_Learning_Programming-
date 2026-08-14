#List

a = [22,43,54,5,5]
print(type(a))
print(a[1])

#changing vaule
a[2] = 77

print(a)

# dublicating power

l=[3,3,3,3,3,5,5,6,5]
print(l)

#traversing on vaule

for i in l:
    print(i)
    
for i in range(0,len(a)):
    print(f"{i} : {a[i]}")
    
for v in range(0,len(l)):
    print(f"{v} : {l[v]}")

# Method

# method knowing list
print(dir(list()))

#append add a vaule in last spot

p =[939,"king",7,8,8.000,True]

p.append("749")
p.append(6.00)

print(p)

# insert

p.insert(2,"is god")

print(p)

#pop it return value and chanes to save num to other variable

l =[10,20,30,40,67,50,60]

l.pop(4)

print(l)

#remove it not save vaule in other variable and remove only first matching number

l =[10,20,30,40,67,50,60]

l.remove(67)

#clear is mean remove all number or string in list 
l.clear()

print(l)

#sort
q = [23,65,64,83,73,76,257]
o =[23,65,64,83,73,76,257]

q.sort()
o.sort(reverse=True) # use for reveres sort number

print(q)
print(o)

#questions solving

# ==========================================
# 1. POSITIVE / NEGATIVE SUM FIXED CODE
# ==========================================
w = [47, 58, -53, -68]

pos = []
neg = []

for x in w:
    if x >= 0:
        pos.append(x)
    else:
        neg.append(x)

# Loop ke BAHAR nikal kar print karo (No extra spaces before print)
print(f"your positive list {pos} and your negative list {neg}")


# ==========================================
# 2. AVERAGE FIXED CODE
# ==========================================
ox = [34, 55, 77, 25, 62, 55]

total_sum = 0 
for u in ox:
    total_sum = total_sum + u

# Print ko loop ke bahar kiya taaki final average ek hi baar aaye
print(f"your final avreage is {total_sum/len(ox)}")


# ==========================================
# 3. LARGEST VALUE FIXED CODE
# ==========================================
wa = [24, 64, 92, 58]

lar = wa[0]
for s in wa:
    if s > lar:
        lar = s

# Loop khatam hone ke baad print
print(f"your final big vaule is {lar}")


# ==========================================
# 4. SECOND LARGEST FIXED CODE
# ==========================================
ty = [24, 65, 3, 66]

largest = ty[0]
sec = ty[0]

for z in ty:
    if z > largest:
        sec = largest
        largest = z
    elif z > sec and z != largest:
        sec = z

# Loop ke ekdum bahar final check
print(f"second large number is {sec} and first is {largest}")

#tuple
om = [34,34,34,34,45,46,6]

tup = tuple(om)
print(tup[3])

print(type(om))
print(tup.index(34))
print(tup.count(34))

#sets
cv = {23,41,45}

io =(23,"good")
print(type(cv))

pa = [1,2,2,2,44,44,66,7,9,9,7,6,7]
s = set(pa)
print(s)
print(hash(io))

#set mthod .add,.clear,.discard,.copy

nam = {24,4,355,4,4,5,5,79,976,}

nam.add(30)
nam.discard(24)
LM = nam.pop()

print(nam)
print(LM)

s1= {23,65,76,6,47,7}
s2 = {22,88,35,6,457}

s1 -= s2
s1& s2
s1&= s2

print(s1 - s2)
print(s2 - s1)
print(s2)
print(s1)

#Dictionaries
#vanila python

w = {23: "pankaj", 33:17}
print(w)
print(w[23]) #reading a key
w[50] = 866#creating a key
w[23] = "king"
print(w)

#method use
red = {23:33,43:44,58:5,12:5,13:1,57:99,34:"panb"}

#red.clear()
#y = red.fromkeys([23,43,50,70],"go to home")

#print(red.get(13))
#print(red.items())
#print(red.keys())
#print(red.values())
#print(red.pop(23))
#red.popitem()
#red.setdefault(60,300)
#red.update({43:"nikale"})
print(red)
#print(y)

#tarversing (loops)
re = {23:33,43:44,58:5,12:5,13:1,57:99,34:"panb"}

for i in re:
    print(f"keys {i} values {re[i]}")
    
#questions
p1={"a":45,"b":58,"c":96}
p2={"d":85,"e":28,"f":36}

for i in p2:
    p1[i] = p2[i]
    
print(p1)

#2
p3={"a":45,"b":58,"c":96}
sum = 0

for e in p3:
    sum = sum + p3[e]
    
print(sum)

#3
mc =["a","b","a","c","b"]


k = {}
for o in mc:
    if o in k.keys():
        k[o] = k[o] + 1
else:
       k[o] = 1 
       
print(k)