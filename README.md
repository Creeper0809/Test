# A + B

표준 입력에서 공백으로 구분된 정수 두 개를 읽고 합을 출력하는 Python 스크립트입니다.

```console
$ python app/main.py
1 2
3
```

모듈러 거듭제곱은 `app.modular.modular_pow`로 계산할 수 있습니다.
지수의 비트를 `& 1`로 확인하고 `>> 1`로 이동하는 반복 제곱 방식을 사용합니다.
반복 횟수는 지수의 비트 수에 비례하며, 매 곱셈 결과에 모듈러 연산을 적용합니다.

```python
from app.modular import modular_pow

assert modular_pow(2, 10, 1000) == 24
assert modular_pow(3, 13, 17) == 12
```

세 인수는 `bool`을 제외한 정수여야 합니다. 지수는 0 이상이고 모듈러스는
0이 아니어야 하며, 음수 모듈러스도 Python의 나머지 연산 규칙을 따릅니다.
정수가 아닌 인수는 `TypeError`, 음수 지수나 0 모듈러스는 `ValueError`를 발생시킵니다.
지수가 0이면 `1 % modulus`를 반환합니다. 외부 의존성은 필요하지 않습니다.

테스트는 Python 표준 라이브러리의 `unittest`로 실행합니다.

```console
$ python -m unittest discover -s tests -v
```
