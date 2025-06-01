# Minimize Boxing and Unboxing
- `이펙티브 C# 아이템 9 : 박싱과 언박싱을 최소화하라` 내용 정리 및 코드 저장소입니다.

## 목표
- 핵심 내용 정리 문서 작성
- 박싱/언박싱 예제 코드 작성
- 동작 과정을 IL 코드로 분석
- 성능에 미치는 영향을 벤치마크를 통해 확인

## 환경
- Windows 10/11 Home/Pro
- [Git](https://git-scm.com/)
- [Python 3.x](https://www.python.org/downloads/)
  - click 패키지 필요
- [Visual Studio 2022](https://visualstudio.microsoft.com/ko/downloads/)

## 툴
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet)

## 내용 정리

- `이펙티브 C# 아이템 9 : 박싱과 언박싱을 최소화하라`의 내용이 정리된 문서는 [여기](./Docs/MinimizeBoxingUnboxing.md)에서 확인할 수 있습니다.

## 참조 문서

> 참조 문서의 경우, 번역해서 추가했습니다.

- [제네릭이 아닌 컬렉션을 사용하면 안 됨](./Docs/NonGenericCollectionsShouldNotBeUsed.md)
- [C#에서는 문자열 연결(string concatenation)과 보간(string interpolation) 시에 항상 박싱(boxing)이 발생하나요?](./Docs/BoxingInCsharpStrings.md)
