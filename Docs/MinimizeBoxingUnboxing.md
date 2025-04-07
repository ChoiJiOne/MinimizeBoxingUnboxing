# 박싱과 언박싱을 최소화하라
- 값 타입
  - 값을 저장할 때 쓰는 저장소
  - 데이터를 스택(Stack)에 저장
  - 다른 변수에 할당되거나 메서드의 인수로 전달될 때 해당 값이 복사
  - 한 변수의 값을 변경해도 다른 변수에는 영향을 주지 않음
  - EX) `int`, `float`, `bool`, `struct` 등등..
- 참조 타입
  - 값을 저장한 위치를 참조하는 방식의 타입
  - 데이터를 힙(Heap) 메모리에 저장
  - 다른 변수에 할당되거나 메서드의 인수로 전달될 때 참조 값이 복사
  - 하나를 바꾸면 같은 주소를 참조하는 다른 변수도 영향 받음
  - EX) `string`, `class`, `interface`, `delegate` 등등...
- .NET Framework
  - 모든 타입의 최상위 타입을 System.Object로 정의
  - System.Object는 참조 타입
  - 박싱/언박싱을 통해 값 타입과 참조 타입을 이어줌
- 박싱/언박싱
  - 박싱: 값 타입 객체를 임의의 참조 타입 내부에 포함시키는 방법
    - 즉, `int`, `bool`, `struct` 같은 값 타입을 `object` 타입으로 포장
  - 언박싱: 박싱되어 있는 참조 타입의 객체로부터 값 타입 객체의 복사본을 가져오는 방법
    ```CSharp
    int num = 100;
    object boxedNum = num; // 박싱
    int unboxedNum = (int)(boxedNum); // 언박싱
    ```
- 박싱/언박싱은 피하는 게 좋음
  - 박싱/언박싱 → 성능에 좋지 않은 영향을 미침
  - 박싱/언박싱을 수행하는 과정에서 임시 객체 생성 → 예상치 못한 버그 발생

## 코드 예시

### 박싱/언박싱
- 간단한 박싱/언박싱 코드
  - `box`: 박싱 수행
  - `unbox.any`: 언박싱 수행
  ```CSharp
  int number = 100;
  object boxingNumber = (object)(number);
  int unboxingNumber = (int)(boxingNumber);
  ```

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

### 제너릭을 이용한 박싱/언박싱 회피
- MS는 제너릭이 아닌 컬렉션을 사용하지 말라고 권장하고 있음
  - 참조: [제너릭이 아닌 컬렉션을 사용하면 안됨](./NonGenericCollectionsShouldNotBeUsed.md)
- 박싱/언박싱 발생
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

  ```CSharp
  ...
  // queue.Enqueue(1);
  IL_0007: ldloc.0
  IL_0008: ldc.i4.1
  IL_0009: box [System.Runtime]System.Int32
  IL_000e: callvirt instance void [System.Collections.NonGeneric]System.Collections.Queue::Enqueue(object)
  ...
  ```
- 제너릭을 이용한 박싱/언박싱 회피
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

  ```CSharp
  ...
  // queue.Enqueue(1);
  IL_0007: ldloc.0
  IL_0008: ldc.i4.1
  IL_0009: callvirt instance void class [System.Collections]System.Collections.Generic.Queue`1<int32>::Enqueue(!0)
  ...
  ```

### 참조 타입을 요구하는 곳에 값 타입 전달 시 박싱/언박싱 수행
- 참조 타입(`System.Object`)을 요구하는 곳에 값 타입 사용 → 박싱/언박싱 발생
  - 이때, 컴파일러가 자동으로 박싱/언박싱 코드를 생성
  - 이 과정에서 컴파일러는 경고 메시지를 출력하지 않음
- .NET Framework의 일부 API는 `System.Object` 타입 객체를 요구하는 경우 존재 → 박싱/언박싱 발생
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

### 문자열 보간을 이용한 박싱/언박싱 회피
- 문자열 보간 시 `string.Format` 사용  → 박싱/언박싱 발생
  - 그러나, `$`를 이용하여 문자열 보간 수행 시 → 박싱/언박싱 발생 x
  - 내부에서 `DefaultInterpolatedStringHandler`의 `AppendFormatted<T>`를 이용해서 박싱 없이 값 타입을 처리
- `string.Format` 사용
  ```CSharp
  ...
  int firstNumber = 100;
  int secondNumber = 200;
  int thirdNumber = 300;

  string message = String.Format("A few numbers: {0}, {1}, {2}", firstNumber, secondNumber, thirdNumber);
  ...
  ```

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
- 보간 문자열 사용
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
  IL_0045: nop
  IL_0046: ldloca.s 4
  IL_0048: ldstr ", "
  IL_004d: call instance void [System.Runtime]System.Runtime.CompilerServices.DefaultInterpolatedStringHandler::AppendLiteral(string)
  IL_0052: nop
  IL_0053: ldloca.s 4
  IL_0055: ldloc.2
  IL_0056: call instance void [System.Runtime]System.Runtime.CompilerServices.DefaultInterpolatedStringHandler::AppendFormatted<int32>(!!0)
  IL_005b: nop
  ...
  ```

### 컬랙션으로부터 값 타입 객체를 가져오면 박싱된 객체의 복사본을 가져옴
- 컬랙션으로부터 객체를 가져오는 경우
  - 박싱된 객체의 복사본 가져옴 → 버그 발생 가능성 높임
  ```CSharp
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
  ```
  - 기대한 출력 결과: `New Name`
  - 실제 출력 결과: `Old Name`
  - `Person`이 `class`라면 기대한 출력값이 출력됨

## 결론
- 값 타입을 System.Object 타입이나 인터페이스 타입으로 변경하는 코드는 가능한 작성하지 말아야 함