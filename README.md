# A + B

표준 입력에서 공백으로 구분된 정수 두 개를 읽고 합을 출력하는 Python 스크립트입니다.

```console
$ python app/main.py
1 2
3
```

정수의 0 이상 거듭제곱은 `power` 함수로 계산할 수 있습니다.

```python
from app.power import power

print(power(2, 10))  # 1024
print(power(-3, 3))  # -27
print(power(0, 0))   # 1
```

테스트는 Python 표준 라이브러리의 `unittest`로 실행합니다.

```console
$ python -m unittest discover -s tests -v
```
