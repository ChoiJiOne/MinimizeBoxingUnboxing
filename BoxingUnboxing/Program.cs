using System;

class Program
{
    static void Main(string[] args)
    {
        int number = 100;
        object boxingNumber = (object)(number);
        int unboxingNumber = (int)(boxingNumber);

        Console.WriteLine($"Number: {number}");
        Console.WriteLine($"Boxing number: {boxingNumber}");
        Console.WriteLine($"Unboxing object: {unboxingNumber}");
    }
}