# KMU Campus Life Action Agent

국민대학교 공식 자료를 근거로 학교생활 전반의 질문에 답하고, 필요한 다음 행동까지 도와주는 Agent MVP입니다.

## 주요 기능

- 공식자료 자동 수집: 규정, 학사안내, 학생지원, 학사일정, 공지, 요람, 대학조직, 공개 SWELL 수집
- Chroma Vector DB + JSONL keyword hybrid 검색
- 문장별 출처 표시: 답변에 `[S1]`, `[S2]` citation 부착
- Tool Calling 로그: 분류, 검색, guard, checklist, 문의처 추천 과정을 화면에 표시
- 개인정보 guard: 학번, 성적, 주민번호, 연락처, 포털 ID/PW 요청 차단
- Action flow: 출석인정신청서, 휴학/복학 체크리스트, 수강신청 확인, 증명서 발급, 졸업요건 간이 진단, 수강계획 추천, 문의문 초안
- 문의처 라우팅: 이슈별 담당 부서/교강사/종합서비스센터 추천

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

API 서버는 `http://127.0.0.1:8000`에서 실행됩니다.

프론트엔드 개발 서버:

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://127.0.0.1:5173`을 열면 데모 UI와 관리자 대시보드를 볼 수 있습니다.

## 테스트

```bash
pytest
```

## 데모 질문

- `예비군 때문에 결석하는데 뭐 해야 해?`
- `5월 15일에 예비군 때문에 결석하는데 출석인정 언제까지 내야 해?`
- `질병휴학 하려면 뭐 필요해?`
- `수강신청 완료됐는지 어디서 확인해?`
- `졸업예정증명서 어디서 뽑아?`
- `내 학번이랑 성적으로 처리해줘.`

## API

- `POST /ask`: 질문 답변, 출처, Tool 로그, 다음 행동 반환
- `POST /actions/start`: action 시작
- `POST /actions/continue`: action slot 입력 후 초안 생성
- `POST /ingest/run`: 공식자료 수집, JSONL 저장, Chroma 인덱싱 실행
- `GET /sources`: 공식 chunk 목록
- `GET /health`: 서버 상태

## 데이터와 근거

수집/청킹된 데이터는 `data/processed/chunks.jsonl`에 저장됩니다. 이 파일은 source of truth이며, Chroma가 사용 가능하면 같은 chunk가 `data/vector/chroma` collection에 인덱싱됩니다. Chroma가 사용 불가한 경우에도 JSONL keyword fallback으로 답변 API가 동작합니다.

Crawler는 학교 서버 보호를 위해 보수적으로 동작합니다.

- 도메인별 요청 간격을 사람 속도에 맞춰 랜덤 지연합니다.
- `/ingest/run`은 동시 실행을 막고, 기본 5분 cooldown을 둡니다.
- `ETag`와 `Last-Modified`가 내려오면 다음 수집 때 조건부 요청에 사용합니다.
- 네트워크 실패나 차단 시에는 같은 공식 URL에 연결된 curated fallback text를 사용합니다.
- `/ingest/run` 응답에는 `network_success`, `fallback_used`, `network_failed`, `failed_urls`가 포함되어 실제 크롤링 성공 여부를 숨기지 않습니다.

Source tier:

1. 규정관리시스템
2. 학사안내
3. 학생지원/대학생활 안내
4. 학사일정
5. 공지사항
6. 요람/규정집
7. 대학조직/문의처
8. SWELL 공개 게시판

## 한계와 주의사항

- 실제 행정 처리를 대신하지 않습니다.
- 공식 포털 로그인 이후 개인 화면에는 접근하지 않습니다.
- 실제 학번, 성적, 연락처, 포털 ID/PW는 입력하지 마세요.
- Chroma Vector DB는 구현되어 있으나, 설치/인덱스 장애가 있어도 JSONL 키워드 검색 fallback으로 데모가 동작합니다.
- 최종 처리는 국민대학교 공식 포털, 담당 부서, 학과사무실 또는 담당 교강사 확인이 필요합니다.
