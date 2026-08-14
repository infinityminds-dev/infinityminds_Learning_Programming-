using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using HelloWorld;

namespace Hello
{
    class Program
    {
        //Methods-Function
        static void king(String name)
        {
            Console.WriteLine("hello" + name);
        }

        static float average(int a, int b, int c)
        {
            float sum = a + b + c;
            return sum / 3;
        }

        static float average(int a, int b)
        {
            return (a + b) / 2;
        }


        static void Main(string[] args)
        {
            // single line comment

            /* 
            THIS IS MULIT LINE COMMENT    
            TELL BY CODE WITH HARRY*/

            int op = 56;
            string pan = Console.ReadLine();
            Console.WriteLine(pan);

            Console.WriteLine("Hello World!");
            Console.Write("KING_");
            Console.WriteLine("INFINITY" + op);
            Console.Write("----------------------------------------------");

            /* DATA TYPE 
            Integer - int op = 56; ---> 4 bytes
            Long - long op; ---> 8 bytes
            Floating - float king = 1.5; --->  4 bytes
            Double - double king; ---> 8 bytes
            Character - char a = 'A'; ---> 2 bytes
            Boolean - bool isgood = true; ---> 1 bit
            String - string inp = "hello"; ---> 2 bytes per character
            */

            // DATA TYPE EXAMPLES
            int a = 46;
            float b = 4.6F;
            double c = 45.8D;
            bool d = true;
            char e = 'y';
            string f = "you";
            Console.WriteLine(a);
            Console.WriteLine(b);
            Console.WriteLine(c);
            Console.WriteLine(d);
            Console.WriteLine(e);
            Console.WriteLine(f);

            // TYPE CASTING
            // THERE ARE TWO TYPE OF CASTING
            // 1. Implicit Casting
            // char to int to long to float to double

            int xo = 3;
            double yo = xo;
            float zo = 'v';
            Console.WriteLine(xo);
            Console.WriteLine(yo);
            Console.WriteLine(zo);

            // 2. Eplicit Casting
            int kj = (int)3.5;
            float lj = (int)4.6;
            Console.WriteLine(kj);
            Console.WriteLine(lj);

            // TYPE CONVERSION METHODS (Built-in Convert Class)

            // 1. String to Integer (Sabse Jyada Use Hota Hai User Input Ke Liye)
            string strNum = "45";
            int convertedInt = Convert.ToInt32(strNum); // "45" (string) ban gaya 45 (int)
            Console.WriteLine(strNum);

            // 2. Integer / Double to String
            int myAge = 20;
            string ageString = Convert.ToString(myAge); // 20 ban gaya "20"
            Console.WriteLine(myAge);

            // 3. String to Double / Float
            string priceStr = "99.99";
            double price = Convert.ToDouble(priceStr); // "99.99" ban gaya 99.99 (double)
            Console.WriteLine(priceStr);

            // 4. Integer to Boolean
            int flag = 1;
            bool isTrue = Convert.ToBoolean(flag); // 1 ban jata hai 'true', 0 ban jata hai 'false'
            Console.WriteLine(flag);

            //INPUT TAKING
            Console.Write("Enter Age: ");
            string input = Console.ReadLine(); // User ne 18 type kiya, par ye string "18" hai!

            int age = Convert.ToInt32(input); // Ab ye "18" integer 18 ban gaya!
            Console.WriteLine("Next year age will be: " + (age + 1)); // Output: 19

            //2nd Example
            Console.WriteLine("How many candies do you want?");
            string can = Console.ReadLine();

            // everything in one line without extra variable
            Console.WriteLine("You will get 4 more candies: " + (Convert.ToInt32(can) + 4));


            /*OPERATORS IN C#
            1.Arithmetic Operators
            2.Assignment Opertors
            3.Logical Opertors
            4.Comparison Opertors       
            */

            //1.Arithmetic Operators
            int ba = 7;
            int bc = 4;
            Console.WriteLine("THE VALUE OF A+B IS:" + (ba + bc));
            Console.WriteLine("THE VALUE OF A-B IS:" + (ba - bc));
            Console.WriteLine("THE VALUE OF A*B IS:" + (ba * bc));
            Console.WriteLine("THE VALUE OF A/B IS:" + (ba / bc));

            //2.Assignment Opertors
            int ap = 3;
            int io = ap;
            // io += 4;
            // io -= 3;
            // io *= 5;
            io /= 1;
            Console.WriteLine(io);

            // Logical Operators
            Console.WriteLine(true && false);   // Output: False and IT IS AND
            Console.WriteLine(true && true);    // Output: True and IT IS AND
            Console.WriteLine(false && false);  // Output: False IT IS AND

            Console.WriteLine(true || false);   // Output: True and IT IS OR
            Console.WriteLine(true || true);    // Output: True and IT IS OR
            Console.WriteLine(false || false);  // Output: False and IT IS OR

            Console.WriteLine(!false);          // Output: True
            Console.WriteLine(!true);           // Output: False


            // Comparison Operators
            Console.WriteLine(324 > 555);
            Console.WriteLine(324 <= 555);
            Console.WriteLine(324 >= 555);
            Console.WriteLine(324 != 555);
            Console.WriteLine(5 == 5);

            // Math Class Examples
            int x = 36;
            int y = 50;

            // Maximum aur Minimum nikalna
            Console.WriteLine("Bada number hai: " + Math.Max(x, y));
            Console.WriteLine("Chhota number hai: " + Math.Min(x, y));

            // Square Root (36 ka square root 6 hota hai)
            Console.WriteLine("36 ka Square Root: " + Math.Sqrt(36));

            // Absolute Value (-12 ko +12 kar dega)
            Console.WriteLine("Absolute Value: " + Math.Abs(-12));

            //String Methods
            String name = "hello is \" INFINIY here"; // also we add \n, \t and etc
            Console.WriteLine(name.Length);
            Console.WriteLine(name.ToLower());
            Console.WriteLine(name.ToUpper());
            Console.WriteLine(name.Contains("is"));
            Console.WriteLine(name[1]);
            Console.WriteLine(name.IndexOf("is"));
            Console.WriteLine(name.Substring(4));

            string mo = Console.ReadLine();
            string name1 = Console.ReadLine();

            Console.WriteLine($"your name is {name1} and your money is {mo}");

            // CONDITIONS
            Console.WriteLine("Enter age");
            String agestr = Console.ReadLine();
            int age1 = Convert.ToInt32(agestr);
            bool isvaild = true;

            if (age1 >= 18 && isvaild == true)
            {
                Console.WriteLine("you can drive");
            }
            else if (age1 < 10)
            {
                Console.WriteLine("hey kid go drink some milk ");
            }
            else if (isvaild == false)
            {
                Console.WriteLine("you are not vaild ");
            }
            else
            {
                Console.WriteLine("you cannot drive");
            }

            // SWITCH KEYS
            int money = 0;

            switch (money)
            {
                case 0:
                    Console.WriteLine("garibee");
                    break;


                case 50:
                    Console.WriteLine("you can buy Nothing");
                    break;

                default:
                    Console.WriteLine("enjoy");
                    break;



            }

            //LOOPS
            //While loop
            int i = 0;
            while (i <= 50)
            {
                Console.WriteLine(i + 1);
                i++;
            }

            //Do-While loop
            int ii = 10;
            do
            {
                Console.WriteLine("Ek baar toh chalega hi!");
                ii++;
            } while (ii < 5);

            //For loop
            for (int ioo = 1; ioo <= 5; ioo++)
            {
                Console.WriteLine("Number: " + ioo);
            }

            //Break and Continue
            for (int we = 1; we <= 5; we++)
            {
                Console.WriteLine("break: " + we);
                break;
            }

            for (int nm = 1; nm <= 5; nm++)
            {
                if (nm == 3)
                {
                    continue; // 3 ko print nahi karega, skip karke 4 par chala jayega
                }
                Console.WriteLine(nm);
            }

            king(Console.ReadLine());
            king("Rohit");
            Console.WriteLine(average(3, 4, 6));
            Console.WriteLine(average(5, 3));
            float temp = average(6, 9, 2);
            Console.WriteLine(temp);

            //OOPs - Classes and objects
            Player tommy = new Player();

            // 1. Pehle wali health print hogi (49)
            Console.WriteLine("Pehle Health thi: " + tommy.getHealth());

            // 2. Health update kar di (57)
            tommy.setHealth(57);

            // 3. Nayi health print hogi (57)
            Console.WriteLine("Ab Nayi Health hai: " + tommy.getHealth());




            Console.ReadLine();
        }
    }
}