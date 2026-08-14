import random

com = random.randint(1, 100)
tries = 0

while True:
    tries = tries + 1
    hum = int(input("Guess the number: "))
    
    if hum == com:
        
        print(f"Congratulations! You won the game in {tries} tries!")  
        break 
      
    elif hum > com:
        print("Guess lower")
            
    elif hum < com:
        print("Guess higher")
