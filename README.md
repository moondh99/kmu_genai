# KMU Campus Life Action Agent

국민대학교 공식 자료를 근거로 학교생활 전반의 질문에 답하고, 필요한 다음 행동까지 도와주는 Agent MVP입니다.

## 주요 기능

- 공식 근거 검색: 규정, 학사안내, 학생지원, 학사일정, 공지, 요람, 대학조직 chunk 검색
- 문장별 출처 표시: 답변에 `[S1]`, `[S2]` citation 부착
- Tool Calling 로그: 분류, 검색, guard, checklist, 문의처 추천 과정을 화면에 표시
- 개인정보 guard: 학번, 성적, 주민번호, 연락처, 포털 ID/PW 요청 차단
- 출석인정 action flow: 출석인정신청서 초안 작성을 위한 추가 질문과 초안 생성
- 문의처 라우팅: 이슈별 담당 부서/교강사/종합서비스센터 추천

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

브라우저에서 `http://127.0.0.1:8000`을 열면 데모 UI를 볼 수 있습니다.

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
- `POST /ingest/run`: 관리자용 수집 실행 placeholder
- `GET /sources`: 공식 chunk 목록
- `GET /health`: 서버 상태

## 데이터와 근거

MVP 데이터는 `data/processed/chunks.jsonl`에 저장되어 있습니다. 각 chunk는 공식 출처 URL, source tier, 문서명, 본문, 키워드, 검색 힌트, content hash를 포함합니다.

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
- Chroma Vector DB와 실제 자동 크롤링은 확장 인터페이스만 포함되어 있으며, MVP는 JSONL 키워드 검색 fallback으로 안정적으로 동작합니다.
- 최종 처리는 국민대학교 공식 포털, 담당 부서, 학과사무실 또는 담당 교강사 확인이 필요합니다.

