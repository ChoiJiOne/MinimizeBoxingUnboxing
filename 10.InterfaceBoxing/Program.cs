using System;

class Program
{
    static void Main(string[] args)
    {
        int number = 42;
        IFormattable formattable = number;
        Console.WriteLine($"{formattable}");
    }
}