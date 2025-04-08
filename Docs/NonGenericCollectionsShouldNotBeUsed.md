# 제네릭이 아닌 컬렉션을 사용하면 안 됨

## 동기

.NET이 처음 만들어졌을 때는 제네릭 데이터 타입이 존재하지 않았기 때문에, [System.Collections](https://docs.microsoft.com/dotnet/api/system.collections) 네임스페이스에 있는 컬렉션 타입들은 타입이 지정되어 있지 않습니다. 그러나 그 이후 제네릭 데이터 타입이 도입되면서, [System.Collections.Generic](https://docs.microsoft.com/dotnet/api/system.collections.generic) 및 [System.Collections.ObjectModel](https://learn.microsoft.com/ko-kr/dotnet/api/system.collections.objectmodel?view=net-9.0) 네임스페이스에 새로운 컬렉션들이 추가되었습니다.

## 권장 사항

새로운 코드를 작성할 때는 비제네릭 컬렉션을 사용하지 않는 것이 좋습니다:

- 오류 발생 가능성 증가: 비제네릭 컬렉션은 타입이 지정되어 있지 않기 때문에, object 타입과 실제 원하는 타입 간의 잦은 캐스팅이 필요합니다. 컴파일러가 타입 일관성을 검사할 수 없기 때문에, 잘못된 타입의 데이터를 잘못된 컬렉션에 넣는 실수가 발생하기 쉽습니다.
- 성능 저하: 제네릭 컬렉션은 값 타입을 object로 박싱하지 않아도 되기 때문에 성능상 이점이 있습니다. 예를 들어 `List<int>`는 내부적으로 int[] 배열에 데이터를 저장합니다. 반면, 데이터를 object[]에 저장하게 되면 박싱이 필요하므로 성능이 떨어집니다.

아래 표는 `System.Collections.Generic` 또는 `System.Collections.ObjectModel` 네임스페이스의 제네릭 컬렉션으로 비제네릭 컬렉션을 어떻게 대체할 수 있는지를 보여줍니다:

| Non-Generic Type              | Generic Replacement                                   |
|------------------------------|-------------------------------------------------------|
| ArrayList                    | `List<T>`                                             |
| CaseInsensitiveComparer      | `StringComparer.OrdinalIgnoreCase`                   |
| CaseInsensitiveHashCodeProvider | `StringComparer.OrdinalIgnoreCase`               |
| CollectionBase               | `Collection<T>`                                       |
| Comparer                     | `Comparer<T>`                                         |
| DictionaryBase               | `Dictionary<TKey, TValue>` or `KeyedCollection<TKey, TItem>` |
| DictionaryEntry              | `KeyValuePair<TKey, TValue>`                         |
| Hashtable                    | `Dictionary<TKey, TValue>`                           |
| Queue                        | `Queue<T>`                                           |
| ReadOnlyCollectionBase       | `ReadOnlyCollection<T>`                              |
| SortedList                   | `SortedList<TKey, TValue>`                           |
| Stack                        | `Stack<T>`                                           |

## 원문
- [DE0006: Non-generic collections shouldn't be used](https://github.com/dotnet/platform-compat/blob/master/docs/DE0006.md)