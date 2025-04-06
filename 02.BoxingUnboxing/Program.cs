using System;

struct Position
{
    public float X;
    public float Y;
    public float Z;
}

class Program
{
    static void Main(string[] args)
    {
        Position position;
        position.X = 1.0f;
        position.Y = 2.0f;
        position.Z = 3.0f;

        object boxingPosition = (object)(position);
        Position unboxingPosition = (Position)(boxingPosition);

        Console.WriteLine($"Position: ({unboxingPosition.X}, {unboxingPosition.Y}, {unboxingPosition.Z})");
    }
}