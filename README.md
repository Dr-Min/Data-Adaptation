## one_file.py


라벨링의 데이터가 openai 튜닝 구조로 하나의 파일에 다 때려 박아 넣어집니다.

하나의 파일로 만들어지기 때문에 무거운 파일이 하나 생긴다고 보면 됩니다.

## in_dividual.py


라벨링 데이터가 openai 튜닝 구조로 1대1 대응되는 방식으로 생겨납니다.

100개의 json 라벨링 데이터가 있다면 100개의 jsonl openai 튜닝 구조 방식의 출력이 생겨납니다.


## 사용법

- 각 폴더의 경로만 알면 사용하기 쉽습니다.

### one_file.py

python one_file.py 입력_디렉토리_경로 출력_파일_경로_파일이름.jsonl

예시 : python one_file.py C:\Users\USER\Desktop\wjscjfl\input C:\Users\USER\Desktop\wjscjfl\output\combined_output.jsonl

## in_dividual.py 사용법

python in_dividual.py 입력_디렉토리_경로 출력_디렉토리_경로

예시 : .\in_dividual.py C:\Users\USER\Desktop\wjscjfl\input C:\Users\USER\Desktop\wjscjfl\output


> 두 파일의 차이점이라고 한다면 one_file은 마지막에 파일 이름을 지정해주어야 합니다. 그 외의 폴더 경로는 동일합니다.



데이터 변환 및 재구성 (Data Transformation and Restructuring):
원본 데이터를 새로운 형식과 구조로 변환하고 있습니다.


데이터 포맷팅 (Data Formatting):
OpenAI의 파인튜닝 요구사항에 맞게 데이터 형식을 조정하고 있습니다.


데이터 준비 (Data Preparation):
AI 모델 학습을 위해 데이터를 최적화된 형태로 준비하고 있습니다.


데이터 어댑테이션 (Data Adaptation):
원본 데이터를 특정 AI 모델과 학습 목적에 맞게 조정하고 있습니다.