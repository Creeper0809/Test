# A + B

표준 입력에서 공백으로 구분된 정수 두 개를 읽고 합을 출력하는 Python 스크립트입니다.

```console
$ python app/main.py
1 2
3
```

# A * B

`app/multiply.py`는 표준 입력에서 공백으로 구분된 정수 두 개를 읽고 곱을 출력합니다.

```console
$ python app/multiply.py
2 3
6
```

테스트는 Python 표준 라이브러리의 `unittest`로 실행합니다.

```console
$ python -m unittest discover -s tests -v
```
