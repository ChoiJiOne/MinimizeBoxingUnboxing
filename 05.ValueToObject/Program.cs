using System;

struct Position
{
    public float X;
    public float Y;
    public float Z;
}

class Program
{
    static void ShowObject(object obj)
    {
        Console.WriteLine($"{obj}");
    }

    static void Main(string[] args)
    {
        int number = 100;
        ShowObject(number);

        Position position;
        position.X = 1.0f;
        position.Y = 2.0f;
        position.Z = 3.0f;
        ShowObject(position);
    }
}