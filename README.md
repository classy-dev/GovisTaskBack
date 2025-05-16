# GOPIZZA Task Management System (Govis Task) - Backend

![대쉬보드 이미지](https://github.com/futureplanning/front-rnd/blob/master/public/dash_boadrd2.png?raw=true)

![작업,일정 이미지](https://raw.githubusercontent.com/futureplanning/front-rnd/refs/heads/master/public/tasks_list.png)

![평가 및 성과관리 이미지](https://raw.githubusercontent.com/futureplanning/front-rnd/refs/heads/master/public/evalution.png)

![Report 이미지](https://raw.githubusercontent.com/futureplanning/front-rnd/refs/heads/master/public/report.png)

![LLM](https://raw.githubusercontent.com/futureplanning/front-rnd/refs/heads/master/public/llm.png)

## 프로젝트 개요

Govis Task Backend는 고피자의 혁신적인 업무 관리 시스템의 서버 측 구현체입니다. 이 API 서버는 조직 내 업무의 복잡성을 효율적으로 관리하기 위한 스마트 워크 플랫폼의 백엔드를 담당합니다. 직급과 권한에 따라 차별화된 인사이트를 제공하고, 실시간 업무 진행 상황 모니터링, 투명한 성과 관리, 데이터 기반 의사결정을 위한 API 엔드포인트를 제공합니다.

## 기술 스택

### 백엔드 프레임워크

- **언어**: Python 3.11+
- **웹 프레임워크**: Django 5.0, Django REST Framework 3.14
- **인증**: JWT (Simple JWT)
- **문서화**: drf-spectacular (OpenAPI 3.0)

### 데이터베이스

- **RDBMS**: PostgreSQL
- **ORM**: Django ORM

### AI 및 데이터 분석

- **LLM 통합**: LangChain 0.3.7
- **AI 모델**: Anthropic Claude
- **데이터 처리**: NumPy, SQLAlchemy

## 프로젝트 구조

```
GovisTaskBack/
├── accounts/              # 사용자 관리 및 인증
├── activities/            # 사용자 활동 로깅
├── config/                # 프로젝트 설정
├── experiments/           # LLM 기반 데이터 분석
├── notifications/         # 알림 시스템
├── organizations/         # 조직 관리 (부서, 팀)
├── reports/               # 데이터 분석 및 리포트
├── requirements/          # 의존성 관리
├── tasks/                 # 작업 관리 시스템
├── .env                   # 환경 변수
├── manage.py              # Django 관리 명령
└── schema.yml             # OpenAPI 스키마
```

## 주요 API 엔드포인트

- `/api/users/` - 사용자 관리
- `/api/departments/` - 부서 관리
- `/api/tasks/` - 작업 관리
- `/api/task-comments/` - 작업 코멘트
- `/api/task-attachments/` - 작업 첨부파일
- `/api/task-history/` - 작업 이력
- `/api/task-time-logs/` - 작업 시간 로그
- `/api/task-evaluations/` - 작업 평가
- `/api/notifications/` - 알림 관리
- `/api/reports/` - 리포트 생성
- `/api/activities/` - 활동 로그
- `/api/experiments/llm/` - LLM 기반 분석
- `/api/token/` - JWT 토큰 발급
- `/api/token/refresh/` - JWT 토큰 갱신
- `/api/docs/` - API 문서 (Swagger UI)

## 주요 특징

### 1. RESTful API 구조

- 직급별 맞춤형 데이터 접근 및 권한 관리
- 모듈화된 앱 구조로 유지보수성 향상
- Swagger/OpenAPI 문서화로 API 탐색 용이

### 2. 작업 관리 시스템

- 작업 생성, 조회, 수정, 삭제 기능
- 작업 상태 관리 및 이력 추적
- 실시간 작업 시간 기록 및 분석
- 작업 의존성 관리

### 3. 조직 및 사용자 관리

- 부서, 팀 구조 관리
- 직급 및 권한 기반 사용자 관리
- 안전한 인증 및 권한 부여 시스템

### 4. 성과 평가 시스템

- 작업별 평가 및 피드백 관리
- 난이도, 성과 점수 분석
- 작업 수행 시간 분석 및 효율성 측정

### 5. 데이터 분석 및 리포트

- 사용자, 팀, 부서별 성과 데이터 집계
- 작업 효율성 및 진행 상황 분석
- 맞춤형 리포트 생성 API

### 6. AI 기반 데이터 분석

- LangChain과 Anthropic 모델을 활용한 자연어 데이터 처리
- 질의응답 기반 데이터 분석
- 업무 패턴 및 인사이트 도출

## 설치 및 실행 방법

### 개발 환경 요구사항

- Python 3.11 이상
- PostgreSQL 14 이상
- pip 또는 virtualenv

### 설치 및 실행

```bash
# 1. 프로젝트 클론
git clone https://github.com/gopizza/GovisTask.git
cd GovisTaskBack

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 3. 의존성 설치
pip install -r requirements/base.txt

# 4. 환경 변수 설정
# .env 파일 생성 및 필요한 환경 변수 추가
# SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT 등

# 5. 데이터베이스 마이그레이션
python manage.py migrate

# 6. 개발 서버 실행
python manage.py runserver
```

개발 서버는 기본적으로 [http://localhost:8000](http://localhost:8000)에서 실행됩니다.
API 문서는 [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)에서 확인할 수 있습니다.

## 핵심 구현 특징

### 1. 권한 기반 접근 제어

사용자의 역할과 직급에 따라 API 접근 권한을 세분화하여, 데이터 보안과 업무 흐름에 적합한 권한 관리를 구현했습니다.

### 2. 작업 생명주기 관리

작업 상태 변경을 추적하고, 각 상태별 필요한 검증과 비즈니스 로직을 적용하여 완전한 작업 생명주기 관리를 제공합니다.

### 3. 성과 평가 및 분석

작업 난이도, 소요 시간, 평가 점수 등 다양한 지표를 수집하고 분석하여 객관적인 성과 평가 시스템을 구현했습니다.

### 4. 알림 시스템

작업 상태 변경, 새 코멘트 추가, 마감일 임박 등 중요 이벤트 발생 시 실시간 알림을 제공하는 시스템을 구현했습니다.

### 5. AI 기반 데이터 분석

LangChain과 Anthropic Claude 모델을 활용하여 자연어 기반의 데이터 분석 및 인사이트 도출 기능을 구현했습니다.

## 데이터 모델

### 주요 모델

- **User**: 직급, 역할, 부서 정보를 포함한 사용자 모델
- **Department**: 조직 구조를 나타내는 부서 모델
- **Task**: 작업 관리의 핵심 모델로 상태, 우선순위, 담당자, 마감일 등 포함
- **TaskComment**: 작업에 대한 코멘트 및 토론
- **TaskAttachment**: 작업 관련 파일 첨부
- **TaskHistory**: 작업 상태 변경 이력
- **TaskTimeLog**: 작업 시간 기록
- **TaskEvaluation**: 작업 성과 평가

## GOPIZZA Task Management API 특징

1. **효율적인 데이터 관리**: 구조화된 API를 통해 업무 데이터의 효율적인 생성, 조회, 수정, 삭제를 지원
2. **보안 및 규정 준수**: 역할 기반 접근 제어로 데이터 보안 및 규정 준수 보장
3. **업무 프로세스 최적화**: 작업 생명주기 관리를 통한 업무 프로세스 자동화 및 최적화
4. **데이터 기반 의사결정**: 종합적인 데이터 수집 및 분석 API를 통한 의사결정 지원
5. **확장성 및 유지보수성**: 모듈화된 설계로 시스템 확장 및 장기적 유지보수 용이
