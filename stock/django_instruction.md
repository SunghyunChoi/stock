# 장고 인스트럭션

## 모델

### 모델 생성
1. app의 model 파일에 class 선언
2. migrate -> make migrations
3. model import

> from news.models import ModelName

4. 새로 만들려면 객체 하나 만들고, 객체.save()하면 됨 (저장할때 자동으로 id 추가)

### 데이터 조회
1. 모두 조회: 모두 조회하려면 model.objects.all() 하면 됨 그럼 쿼리 셋 반환
2. 조건으로 조회: filter(id=1) 이런식으로 하면 됨, 조건에 맞는 것 없으면 빈 쿼리셋 반환
3. 하나만 조회: get(id=1) 이렇게 하면 됨, 조건에 맞는 것 없으면 오류남
4. 문자열로 검색: filter(subject__contains="장고") 이런식으로 하면 됨
- 조회 관련 공식 문서: docs.djangoproject.com/en/3.0/topics/db/queries


### 데이터 수정
1. 일단 get으로 하나 갖고 온다. 갖고 온 것의 이름을 q라고 치자
2. q.subject = " 수정된 문자열 "
3. q.save() 이렇게 하면 끝

### 데이터 삭제
1. 일단 get으로 갖고 온다.
2. q.delete() 끝

### 연결된 데이터 찾기
1. q.anwer_set.all() 이렇게 하면 됨
