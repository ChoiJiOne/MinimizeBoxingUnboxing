# MinimizeBoxingUnboxing.CSharp
- `이펙티브 C# - 아이템 9 : 박싱과 언박싱을 최소화하라` 내용 정리 및 코드 저장소입니다.

## 목표
- 박싱/언박싱 예제 코드 작성
- 동작 과정을 IL 코드로 분석
- 성능에 미치는 영향을 벤치마크를 통해 확인

## 요구 사항
- Windows 10/11 Home/Pro
- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/downloads/)
  - click 패키지 필요
- [Visual Studio 2022](https://visualstudio.microsoft.com/ko/downloads/)

## 사용 툴
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet)

## 박싱과 언박싱을 최소화하라
- 값 타입
  - 값 자체를 저장하는 타입
  - 데이터를 스택(Stack) 메모리에 저장
  - 다른 변수에 할당되거나 메서드의 인수로 전달될 때 해당 값이 복사
  - 한 변수의 값을 변경해도 다른 변수에는 영향을 주지 않음
  - ex) `int`, `float`, `bool`, `struct` 등등..
- 참조 타입
  - 값을 저장한 위치를 참조하는 타입
  - 데이터를 힙(Heap) 메모리에 저장
  - 다른 변수에 할당되거나 메서드의 인수로 전달될 때 참조 값이 복사
  - 하나를 바꾸면 같은 주소를 참조하는 다른 변수도 영향 받음
  - ex) `string`, `class`, `interface`, `delegate` 등등...
- .NET Framework
  - 모든 타입의 최상위 타입을 `System.Object`로 정의
  - `System.Object`는 참조 타입
  - 박싱/언박싱을 통해 값 타입과 참조 타입을 이어줌
- 박싱/언박싱
  - 박싱: 값 타입 객체를 임의의 참조 타입 내부에 포함시키는 방법
    - 즉, `int`, `bool`, `struct` 같은 값 타입을 `object` 타입으로 포장
  - 언박싱: 박싱되어 있는 참조 타입의 객체로부터 값 타입 객체의 복사본을 가져오는 방법
  - [예시 코드](./../01.BoxingUnboxing/Program.cs)
    ```CSharp
    int num = 100;
    object boxedNum = num; // 박싱
    int unboxedNum = (int)(boxedNum); // 언박싱
    ```
- 박싱/언박싱은 피하는 게 좋음
  - 박싱/언박싱 과정에서 힙 메모리 할당 → 성능에 좋지 않은 영향을 미침
  - 박싱/언박싱 과정에서 임시 객체 생성 → 예상치 못한 버그 발생

## 코드 예시

### 박싱/언박싱

#### [예제](./../01.BoxingUnboxing/Program.cs)
- C# 코드
  ```CSharp
  int number = 100;
  object boxingNumber = (object)(number);
  int unboxingNumber = (int)(boxingNumber);
  ```
- IL 코드
  - `box`: 박싱 수행 명령어
  - `unbox.any`: 언박싱 수행 명령어
  ```CSharp
  // int num = 100;
  IL_0001: ldc.i4.s 100
  IL_0003: stloc.0
  // object obj = num;
  IL_0004: ldloc.0
  IL_0005: box [System.Runtime]System.Int32
  IL_000a: stloc.1
  // int value = (int)obj;
  IL_000b: ldloc.1
  IL_000c: unbox.any [System.Runtime]System.Int32
  IL_0011: stloc.2
  ```

### 제너릭을 이용한 박싱 회피
- MS는 제너릭이 아닌 컬렉션을 사용하지 말라고 권장하고 있음
  - 참조: [제너릭이 아닌 컬렉션을 사용하면 안됨](./NonGenericCollectionsShouldNotBeUsed.md)

#### [예제 (제너릭을 사용하지 않는 경우)](./../03.NonGenericCollections/Program.cs)
- C# 코드
  - 제너릭이 아닌 컬렉션을 사용하는 케이스
  ```CSharp
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
  ```
- IL 코드 일부
  - Queue에 데이터를 추가하는 과정에서 박싱 수행
  ```CSharp
  ...
  // queue.Enqueue(1);
  IL_0007: ldloc.0
  IL_0008: ldc.i4.1
  IL_0009: box [System.Runtime]System.Int32
  IL_000e: callvirt instance void [System.Collections.NonGeneric]System.Collections.Queue::Enqueue(object)
  ...
  ```

#### [예제 (제너릭을 사용하는 경우)](./../04.GenericCollections/Program.cs)
- C# 코드
  - 제너릭 컬렉션을 사용하는 케이스
  ```CSharp
  using System;
  using System.Collections.Generic;

  class Program
  {
      static void Main(string[] args)
      {
          Queue<int> queue = new Queue<int>();
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
  ```
- IL 코드 일부
  - 값 타입인 경우 박싱을 수행하지 않음
  ```CSharp
  ...
  // queue.Enqueue(1);
  IL_0007: ldloc.0
  IL_0008: ldc.i4.1
  IL_0009: callvirt instance void class [System.Collections]System.Collections.Generic.Queue`1<int32>::Enqueue(!0)
  ...
  ```

### 참조 타입을 요구하는 곳에 값 타입 전달 시 박싱 수행
- 참조 타입(`System.Object`)을 요구하는 곳에 값 타입 사용 할 경우 → 박싱 발생
  - 컴파일러가 자동으로 박싱 코드를 생성
  - 이 과정에서 컴파일러는 경고 메시지를 출력하지 않음
- .NET Framework의 일부 API는 `System.Object` 타입 객체를 요구하는 경우 존재 → 박싱 발생

#### [예제](./../05.ValueToObject/Program.cs)
- C# 코드
  ```CSharp
  static void ShowObject(object obj)
  {
      Console.WriteLine($"{obj}");
  }

  ...
  int number = 100;
  ShowObject(number);
  ...
  ```
- IL 코드 일부
  ```CSharp
  ...
  IL_0000: nop
  // int num = 100;
  IL_0001: ldc.i4.s 100
  IL_0003: stloc.0
  // ShowObject(num);
  IL_0004: ldloc.0
  IL_0005: box [System.Runtime]System.Int32
  IL_000a: call void Program::ShowObject(object)
  ...
  ```

### 문자열 보간을 이용한 박싱 회피
- 문자열 보간 시 `string.Format` 사용  → 박싱 발생
  - 그러나, `$`를 이용하여 문자열 보간 수행 시 → 박싱 발생 x
  - 내부에서 `DefaultInterpolatedStringHandler`의 `AppendFormatted<T>`를 이용해서 박싱 없이 값 타입을 처리

> 이 부분의 경우, 이펙티브 C# 책에 잘못 설명되어 있다. 아마 책이 오래되어서 발생한 문제로, 해당 문서에는 최신 사항을 반영해서 추가
  
#### [예제 (`string.Format` 사용)](./../07.StringInterpolation/Program.cs)
- C# 코드
  ```CSharp
  ...
  int firstNumber = 100;
  int secondNumber = 200;
  int thirdNumber = 300;

  string message = String.Format("A few numbers: {0}, {1}, {2}", firstNumber, secondNumber, thirdNumber);
  ...
  ```
- IL코드 일부
  - `System.String::Format`의 인자로 `System.Object` 타입을 요구하여 박싱 수행
  ```CSharp
  ...
  IL_0010: ldstr "A few numbers: {0}, {1}, {2}"
  IL_0015: ldloc.0
  IL_0016: box [System.Runtime]System.Int32
  IL_001b: ldloc.1
  IL_001c: box [System.Runtime]System.Int32
  IL_0021: ldloc.2
  IL_0022: box [System.Runtime]System.Int32
  IL_0027: call string [System.Runtime]System.String::Format(string, object, object, object)
  IL_002c: stloc.3
  ...
  ```

#### [예제 (보간 문자열 (`$`)사용)](./../06.StringInterpolation/Program.cs)
- C# 코드
  ```CSharp
  using System;

  class Program
  {
      static void Main(string[] args)
      {
          int firstNumber = 100;
          int secondNumber = 200;
          int thirdNumber = 300;

          string message = $"A few numbers: {firstNumber}, {secondNumber}, {thirdNumber}";
          Console.WriteLine(message);
      }
  }
  ```
- IL 코드 일부
  - `DefaultInterpolatedStringHandler`의 `AppendFormatted<T>`를 이용해서 박싱 없이 값 타입을 처리
  ```CSharp
  ...
  IL_0026: nop
  IL_0027: ldloca.s 4
  IL_0029: ldloc.0
  IL_002a: call instance void [System.Runtime]System.Runtime.CompilerServices.DefaultInterpolatedStringHandler::AppendFormatted<int32>(!!0)
  IL_002f: nop
  IL_0030: ldloca.s 4
  IL_0032: ldstr ", "
  IL_0037: call instance void [System.Runtime]System.Runtime.CompilerServices.DefaultInterpolatedStringHandler::AppendLiteral(string)
  IL_003c: nop
  IL_003d: ldloca.s 4
  IL_003f: ldloc.1
  IL_0040: call instance void [System.Runtime]System.Runtime.CompilerServices.DefaultInterpolatedStringHandler::AppendFormatted<int32>(!!0)
  ...
  ```

### 컬랙션으로부터 값 타입 객체 참조 시 박싱된 객체 복사본 참조
- 컬랙션으로부터 객체를 가져오는 경우
  - 박싱된 객체의 복사본 가져옴 → 버그 발생 가능성 높임

#### [예제](./../08.StructCopy/Program.cs)

```CSharp
using System;
using System.Collections;
using System.Collections.Generic;

struct Person
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
  ```
- 기대한 출력 결과: `New Name`
- 실제 출력 결과: `Old Name`

```CSharps
...
Person firstPerson = attendees[0];
firstPerson.Name = "New Name";
...
```
- `Person firstPerson = attendees[0];` 과정에서 참조가 아닌 Person의 복사본을 가져옴
- 따라서, `firstPerson.Name = "New Name";`는 복사본의 값을 변경하는 코드임
- `Person`이 `class`라면 기대한 출력값이 출력됨

### 값 타입을 인터페이스 타입으로 변환 시 박싱 수행
- 값 타입을 인터페이스 타입으로 변환할 경우 → 박싱 수행
- 인터페이스는 참조 타입이기 때문에, 값 타입이 인터페이스 타입으로 할당되기 위해서는 힙에 박싱된 객체가 생성되어야 함
  - 이로 인해 추가적인 메모리 할당과 성능 비용이 발생하며, 다형성 구현 시 주의가 필요함

#### [예제](./../10.InterfaceBoxing/Program.cs)
- C# 코드
  ```CSharp
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
  ```
- IL 코드
  ```CSharp
  // IFormattable value = 42;
  IL_0000: ldc.i4.s 42
  IL_0002: box [System.Runtime]System.Int32
  IL_0007: stloc.0
  ```

### [BenchmarkDotNet으로 박싱 성능 측정](./../09.BoxingBenchmark/Program.cs)
- 성능 측정 테스트 코드
  - `WithBoxing`: 박싱하며 덧셈 연산 1000000번 수행
  - `WithoutBoxing`: 박싱하지 않고 덧셈 연산 1000000번 수행

```CSharp
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
```

#### 실행 결과

| Method        | Mean       | Error     | StdDev   | Gen0      | Allocated  |
|-------------- |-----------:|----------:|---------:|----------:|-----------:|
| WithBoxing    | 1,944.7 us | 325.34 us | 17.83 us | 1433.5938 | 24000001 B |
| WithoutBoxing |   208.2 us |  14.16 us |  0.78 us |         - |          - |

- `WithBoxing` 메서드는 `WithoutBoxing`보다 약 9배 이상 느린 실행 시간을 보임
- `WithBoxing`은 박싱된 객체를 100만 번 생성하므로, 24MB 이상의 메모리가 할당됨
- Gen0(GC 0세대 수집)도 1400회 이상 발생 → GC 부담 증가
- 반면 `WithoutBoxing`은 메모리 할당 없이 연산을 마치고, GC도 발생하지 않음
- 즉, 박싱은 성능 저하, 메모리 낭비, GC 압박을 모두 유발하는 요인이 될 수 있음

## 결론
- 값 타입을 `System.Object` 타입이나 인터페이스 타입으로 변경하는 코드는 가능한 피해야 함
- 박싱/언박싱은 눈에 띄지 않게 발생하지만, 반복되면 성능 저하와 불필요한 메모리 할당을 초래함
- 박싱 발생 지점을 사전에 차단하는 습관이 필요함
  - 제네릭 컬렉션 및 제네릭 메서드 사용
  - string.Format 대신 보간 문자열 ($"") 사용
  - 값 타입에 인터페이스 할당 피하기

## 참조 문서
- [제네릭이 아닌 컬렉션을 사용하면 안 됨](./Docs/NonGenericCollectionsShouldNotBeUsed.md)
- [C#에서는 문자열 연결(string concatenation)과 보간(string interpolation) 시에 항상 박싱(boxing)이 발생하나요?](./Docs/BoxingInCsharpStrings.md)
