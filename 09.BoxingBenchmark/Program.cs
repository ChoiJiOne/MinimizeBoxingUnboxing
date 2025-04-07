using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]
[ShortRunJob]
class BoxingBenchmarks
{
    private int _iterationCount = 1000000;

    [Benchmark]
    public int WithBoxing()
    {
        object boxed;
        int sum = 0;
        for (int i = 0; i < _iterationCount; i++)
        {
            boxed = i;
            sum += (int)boxed;
        }
        return sum;
    }

    [Benchmark]
    public int WithoutBoxing()
    {
        int sum = 0;
        for (int i = 0; i < _iterationCount; i++)
        {
            sum += i;
        }
        return sum;
    }
}

class Program
{
    static void Main(string[] args)
    {
        BenchmarkRunner.Run<BoxingBenchmarks>();
    }
}