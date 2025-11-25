
# CatchRounge

## 📑 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [주요 기능](#주요-기능)
3. [기술 스택](#기술-스택)
4. [아키텍처](#아키텍처)
5. [DB 스키마](#DB-스키마)
6. [디렉토리 구조](#디렉토리-구조)
7. [실행 방법](#실행-방법)
8. [API 명세](#API-명세)
9. [프로젝트 회고](#프로젝트-회고)

## 프로젝트 개요
CatchRounge는 부트 캠프 라운지의 제한된 공간을 공정하게 사용할 수 있도록 만든 라운지 예약 관리 시스템입니다.

| 항목       | 내용                                     |
|------------|----------------------------------------|
| 기간       | 24.09.04 ~ 24.09.07(3일)                                 |
| 인원       | 3명                                     |
| 역할       | 김남훈: 프론트엔드 개발<br>김지훈: 백엔드 개발<br>김현영: 배포 및 문서 작성 |

## 주요 기능
- **좌석 예약/퇴실** : 사용자가 라운지 좌석을 예매하고, 필요 시 직접 퇴실 처리 가능
- **자동 퇴실 기능** : 예약된 시간이 지나면 좌석이 자동으로 해제되어 다른 사용자가 이용 가능

## 기술 스택


| 분야       | 기술                                  |
|-----------|-------------------------------------|
| Backend   | Flask, Python, Jinja2               |
| Frontend  | HTML, CSS, JavaScript             |
| Database  | MongoDB                              |
| DevOps/Infra | Docker                             |

## 아키텍처
![architecture](./docs/architecture.png)

## 디렉토리 구조

```
 ┣ app
 ┃ ┣ 📂common
 ┃ ┃ ┣ 📂initializer 
 ┃ ┃ ┣ config.py 
 ┃ ┃ ┣ error_handler.py 
 ┃ ┃ ┣ extensions.py 
 ┃ ┃ ┗ jwt_filter.py
 ┃ ┣ 📂repository
 ┃ ┣ 📂route
 ┃ ┣ 📂service
 ┃ ┣ 📂static
 ┃ ┣ 📂templates
 ┃ ┗ __init__.py
 ┣ .DS_Store
 ┣ .gitignore
 ┣ Dockerfile
 ┣ docker-compose.yml
 ┣ init-replica.sh
 ┣ requirements.txt
 ┗ run.py
```

## 실행 방법
1. 저장소 클론
```bash
git clone https://github.com/southernlight/catchrounge.git
cd catchrounge
```

2. Docker Compose로 컨테이너 실행
```bash
docker compose up --build -d
```

3. 브라우저에서 접속  
[http://localhost:5000](http://localhost:5000)

## API 명세


## 프로젝트 회고
