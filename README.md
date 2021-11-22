## DB 응용과 XML - Report 1

### Description
MySQL, PyQt를 이용하여, "선수 테이블 검색" 인터페이스 구현하기

### Tools
- Pycharm
- MySQL
- PyQt

### Start
- MySQL에 kleague DB import
- MySQL에 guest 계정 만들기  
-> command line client 실행
```
use mysql;

select user, host from user;
create user guest@localhost identified by ‘bemyguest’;
select user, host from user;

show grants for guest@localhost;
grant all privileges on *.* to guest@localhost;
show grants for guest@localhost;
```

### 기능
1. 선수 검색
- 팀명, 포지션, 출신국을 선택할 수 있음
- 키, 몸무게를 입력받을 수 있음
2. 파일 출력
- CSV, JSON, XML 파일 중 선택된 파일을 출력할 수 있음
