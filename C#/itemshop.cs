using System;

class Program
{
    static void Main(string[] args)
    {
        // 1. Variables setup (Tera example)
        int money = 200;
        int itemPrice = 100;
        bool canBuy = false;

        Console.WriteLine("=== GAMING SHOP SYSTEM ===");
        Console.WriteLine("Aapke paas Money hai: " + money);
        Console.WriteLine("Item ka Price hai: " + itemPrice);
        Console.WriteLine("----------------------------");

        // 2. Logic Check (Sahi Syntax)
        if (money >= itemPrice)
        {
            canBuy = true;
            Console.WriteLine("Status: You can buy this! [Press 'E' to Buy]");
        }
        else
        {
            canBuy = false;
            Console.WriteLine("Sorry, you have no money!");
        }

        // 3. User Input (Keyboard Press Simulator)
        if (canBuy == true)
        {
            Console.Write("\nType 'E' and press Enter to buy: ");
            string input = Console.ReadLine(); // Unity ke Input.GetKey ki jagah

            if (input == "E" || input == "e")
            {
                money = money - itemPrice; // Money deduct ho gaya
                Console.WriteLine("\n[SUCCESS] Item bought! Remaining Money: " + money);
            }
            else
            {
                Console.WriteLine("\n[CANCELLED] Purchase cancelled.");
            }
        }

        //its just example for money = money-itemprice
        int y = 45;
        int x = y;

        y = 100; // Y ko badal diya

        Console.WriteLine("X ki value hai: " + x);
        Console.WriteLine("Y ki value hai: " + y);

    }
}
