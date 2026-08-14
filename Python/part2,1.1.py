def king():
    print("not your king")
king()

def name(a,b):
    print(a+b)
name(23,50)

def test(q):
    copy = q
    rev = 0
    
    while q > 0:
        rev = rev*10 + q%10
        q = q // 10 
    
    if rev == copy:
        print("palindrome")
    else:
            print("not palindrome")
    
test(200)

#default 
def fyc(a,b,c,d=5,e=12):
    print(a*b+c//+d-e)
fyc(22,33,55)

#keyword
def fyc(a,b,c,d):
    print(a*b+c-d)
fyc(22,c = 3,d = 5, b=20)

#return

def gh():
    return "how are you"
    
b = gh()
print(b)
