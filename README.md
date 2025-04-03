# MinimizeBoxingUnboxing-CSharp
- `이펙티브 C# - 아이템 9 : 박싱과 언박싱을 최소화하라` 내용 정리 및 실험 코드 저장소입니다.

## 목표
- 대표적인 예시 정리 및 이를 코드로 실험
- 성능에 미치는 영향을 벤치마크를 통해 확인
- 메모리 사용량 및 GC(가비지 컬렉션) 동작에 어떤 영향을 주는지 분석
- 동작 과정을 IL 코드로 분석

## 요구 사항
- `Windows 10/11 Home/Pro`
- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/downloads/)
  - click 패키지 필요 (`pip install click`)
- [Visual Studio 2022](https://visualstudio.microsoft.com/ko/downloads/)

## 사용 툴
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet)

## 참조
- Effective C# Item 9: Minimize Boxing and Unboxing
- [값 형식 - C# Reference](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/builtin-types/value-types)
- [참조 형식 - C# Reference](https://learn.microsoft.com/ko-kr/dotnet/csharp/language-reference/keywords/reference-types)
