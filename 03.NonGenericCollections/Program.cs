using System;
using System.Collections;

class Program
{
    static void Main(string[] args)
    {
        Queue queue = new Queue();
        queue.Enqueue(1);
        queue.Enqueue(2);
        queue.Enqueue(3);
        queue.Enqueue(4);
        queue.Enqueue(5);

        while (queue.Count > 0)
        {
            Console.WriteLine($"{queue.Dequeue()}");
        }
    }
}