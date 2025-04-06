using System;

class Program
{
    static void Main(string[] args)
    {
        int firstNumber = 100;
        int secondNumber = 200;
        int thirdNumber = 300;

        string message = String.Format("A few numbers: {0}, {1}, {2}", firstNumber, secondNumber, thirdNumber);
        Console.WriteLine(message);
    }
}