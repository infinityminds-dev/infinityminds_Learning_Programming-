using System;
using System.Linq;
using System.Collections.Generic;

namespace HelloWorld
{
    class Player
    {
        public string name = "Harry";
        private int health = 49; // Private: direct access allowed nahi hai

        // Health dekhne ke liye (Getter)
        public int getHealth()
        {
            return health;
        }

        // Health change karne ke liye (Setter)
        public void setHealth(int h)
        {
            health = h;
        }
    }
}