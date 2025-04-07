using System;
using System.Collections;
using System.Collections.Generic;

public struct Person
{
    public string Name { get; set; }

    public override string ToString()
    {
        return Name;
    }
}

class Program
{
    static void Main(string[] args)
    {
        List<Person> attendees = new List<Person>();

        Person person = new Person { Name = "Old Name" };
        attendees.Add(person);

        Person firstPerson = attendees[0];
        firstPerson.Name = "New Name";

        Console.WriteLine(attendees[0].ToString());
    }
}

