# 작업 현황 및 폴더/파일 역할 정리

> KMU Campus Life Action Agent — 한국 국민대학교 학사 RAG 에이전트
> 작성일: 2026-05-19

## 1. 한 줄 요약

학사·휴복학·수강신청·졸업·증명서 등 **국민대 학생생활 질문에 한국어로 근거 기반 답변** 을 주고, **출석인정신청서·휴학 체크리스트·문의문 같은 다음 단계 서류 초안** 까지 자동 생성하는 grounded-RAG 에이전트. FastAPI 백엔드 + Vite/React 프런트엔드.

## 2. 현재 작업 상태 스냅샷

| 항목 | 상태 |
|------|------|
| 크롤링된 공식 문서 | 11개 (8개 소스 어댑터) |
| 인덱싱된 청크 (`chunks.jsonl`) | 46개 |
| 벡터 인덱스 | Chroma 로컬 (`data/vector/chroma`) — 해시 임베딩 64차원, 외부 모델 의존성 없음 |
| 액션(서류 작성) 종류 | 8종 (출석/휴학/복학/증명서/수강신청/졸업감사/이수계획/문의) |
| 테스트 | `pytest` 기준 18개 통과 |
| 프런트엔드 | Vite + React 18 SPA — Chat / ActionForm / Sources / ToolLog / Admin 패널 |
| LLM 호출 | **의도적으로 스텁(stub)** — `llm_client.GuardedLLMClient.generate()`는 빈 문자열 반환. 답변은 결정론적 템플릿으로 조립됨 |
| 가드레일 | 개인정보 정규식 차단 + "근거 없으면 응답 금지" |

## 3. 요청 파이프라인

```
POST /ask
  → agent/guard.inspect_privacy          (학번/주민/연락처/PW/성적 정규식 차단)
  → agent/classifier.classify_issue      (10개 issue_type 룰 기반 분류)
  → retriever/hybrid_retriever.search    (벡터 + 키워드, chunk_id 머지)
  → agent/guard.require_sources          (근거 없으면 차단)
  → agent/planner.suggest_actions        (issue_type + chunk.actions 기반 다음 액션 제안)
  → agent/answer_builder.build_final_answer
        ├─ tools/checklist.generate_checklist
        ├─ tools/contact_router.route_contact
        ├─ tools/deadline (extract_event_date + calculate_deadline)
        └─ agent/citation (S1/S2 라벨 + cite())
```

서류 작성(액션) 흐름은 별도 상태 머신:
`POST /actions/start` → 슬롯 질문 반환 → `POST /actions/continue` (슬롯 값에 다시 privacy 검사) → `tools/document_drafter.draft_action_document`.

## 4. 디렉토리 트리 (요약)

```
kmu-campus-life-action-agent/
├── app.py                     # FastAPI 엔트리포인트 (7개 라우트)
├── llm_client.py              # 가드된 LLM 어댑터 (현재 스텁)
├── requirements.txt           # fastapi, uvicorn, pydantic, requests, beautifulsoup4, chromadb, pytest
├── agent/                     # 파이프라인 노드 (guard/classifier/planner/answer_builder/citation/action_state)
├── retriever/                 # HybridRetriever (vector + keyword)
├── tools/                     # 액션 도구 (checklist/contact_router/deadline/document_drafter/graduation/course_planner)
├── ingestion/                 # 크롤 → 파싱 → 청킹 → 인덱싱 파이프라인
├── crawler/                   # 소스별 어댑터 8종 + BaseCrawler (학교 서버 보호 규칙 내장)
├── data/                      # raw / processed / vector / state / actions
├── frontend/                  # Vite + React SPA (Chat / Action / Source / ToolLog / Admin)
├── tests/                     # pytest 8개 파일
├── scripts/                   # 학사공지 크롤 프로브 3종 (Playwright)
├── CLAUDE.md, README.md, PROGRESS.md, STRUCTURE.md, project_plan.md
```

## 5. 파일별 역할

### 5.1 루트

| 파일 | 역할 |
|------|------|
| `app.py` | FastAPI 앱. 라우트: `GET /`, `GET /health`, `POST /ask`, `POST /actions/start`, `POST /actions/continue`, `POST /ingest/run`, `GET /sources`. `frontend/dist` 존재 시 정적 파일 마운트 |
| `llm_client.py` | `GuardedLLMClient.generate(prompt, grounded_context)` — 현재는 `""` 반환. 추후 Ollama/Qwen 어댑터를 같은 인터페이스로 교체 가능 |
| `requirements.txt` | fastapi, uvicorn, pydantic, pytest, requests, beautifulsoup4, chromadb |
| `README.md` | MVP 기능·API·데모 질문·크롤 정책·소스 티어 설명 |
| `PROGRESS.md` | 진행 로그 (현재 11문서/46청크/18테스트 통과) |
| `STRUCTURE.md` | 폴더 맵 및 모듈 역할 상세 |
| `project_plan.md` | 4주 MVP 계획서 (목표/범위/티어/아키텍처/가드레일/역할 분담) |
| `CLAUDE.md` | Claude Code 작업 시 지켜야 할 규칙 (가드레일, 파이프라인, 인용 계약) |

### 5.2 `agent/` — 파이프라인 노드

| 파일 | 역할 |
|------|------|
| `guard.py` | `inspect_privacy()` — 학번/주민/연락처/PW/성적 정규식 차단. `require_sources()` — 근거 없으면 응답 금지 |
| `classifier.py` | `classify_issue()` — 10개 issue_type (attendance, leave_return, course_registration, certificate, graduation, schedule, contact, military, student_support, other) 룰 기반 분류 |
| `planner.py` | `suggest_actions(issue_type, chunks)` — chunk의 `actions` 메타데이터 + issue_type별 디폴트로 다음 행동 추천 |
| `answer_builder.py` | `build_final_answer()` — `[답변 요약]/[해야 할 일]/[필요 서류]/[신청 경로]/[기한]/[문의처]/[다음 행동]/[근거]/[주의]` 9개 섹션 결정론적 조립 |
| `citation.py` | `build_citations()` 로 청크별 `S1`, `S2` … 라벨 부여, `cite()` 로 `[S1]` 마커 생성 — 모든 사실 문장에 부착 |
| `action_state.py` | 액션 상태 머신. `start_action()`/`continue_action()` — 슬롯이 부족하면 추가 질문, 모두 채워지면 `document_drafter` 호출 |

### 5.3 `retriever/`

| 파일 | 역할 |
|------|------|
| `hybrid_retriever.py` | `HybridRetriever` — 벡터+키워드 결과를 `chunk_id` 기준 머지, `score → source_tier` 순으로 랭킹. `reload()` 로 인덱스 갱신, `status()` 로 헬스 체크 |
| `vector_retriever.py` | Chroma 영속 인덱스. `hash_embedding()` 으로 SHA256 기반 64차원 결정론적 벡터 생성 (외부 모델 불필요). 초기화 실패 시 `available=False` 로 조용히 다운그레이드 |
| `keyword_retriever.py` | JSONL 폴백 검색. 토큰 겹침 + 키워드 완전일치(2배 가중) + `issue_type` 일치(+2) + `source_tier` 보너스로 스코어링 |

### 5.4 `tools/` — 액션 도구

| 파일 | 역할 |
|------|------|
| `checklist.py` | `generate_checklist()` — issue_type별 필수 서류·신청 경로·제출처를 청크에서 추출하여 작업 목록화 |
| `contact_router.py` | `route_contact()` — 청크의 `contacts` + `DEFAULT_CONTACTS` 폴백을 머지하여 부서 연락처 라우팅 |
| `deadline.py` | `extract_event_date()` (한국어 월/일 + ISO 파싱) + `calculate_deadline()` (`rule_days` 오프셋) |
| `document_drafter.py` | **액션 디스패처**. `ACTION_SCHEMAS` 에 8개 슬롯 스키마, `draft_action_document()` 가 액션별 핸들러(`_attendance_document`, `_leave_checklist`, `_graduation_audit`, `_course_plan` 등) 호출 |
| `graduation.py` | `audit_graduation_requirements()` — 현재 이수 학점 vs 목표/전공 학점 비교, gap 리턴 |
| `course_planner.py` | `recommend_course_plan()` — 졸업 gap + 학생 관심사로 강의 추천 |

> ⚠ `graduation`/`course_planner` 는 `/ask` 가 아니라 **액션 흐름에서만** 호출됨.

### 5.5 `ingestion/`

| 파일 | 역할 |
|------|------|
| `pipeline.py` | `run_ingestion(source, limit, force_rebuild)` — 크롤러 디스패치 → content_hash 중복 제거 → `chunks.jsonl` 기록 → Chroma upsert. **300초 쿨다운** 강제 |
| `parser.py` | `extract_visible_text()` — BeautifulSoup 으로 script/style/nav/footer 제거 후 텍스트 추출 |
| `chunker.py` | `chunk_text()` — 700자 이하 단락 인지 청킹 |
| `file_extractors.py` | `describe_attachment_support()` — PDF/DOCX 지원 상태 선언 (HWP/OCR 은 추후) |

### 5.6 `crawler/`

`BaseCrawler` (`base.py`) 가 **학교 서버 보호 규칙** 을 강제:
- 호스트별 랜덤 지연 8–18s
- `max_pages_per_run = 3`, `INGEST_COOLDOWN_SECONDS = 300`
- 모듈 레벨 `_INGEST_LOCK` 로 동시 실행 차단
- `ETag` / `Last-Modified` 조건부 GET (304 → 청크 재생성 스킵)
- 네트워크 실패/빈 응답 시 `SourcePage.fallback_text` 사용, `used_fallback: true` 태깅

| 어댑터 | 소스 | 티어 |
|--------|------|------|
| `kmu_rule.py` | 학칙 제303조 | **1 (최우선)** |
| `kmu_academic_guide.py` | 출석·휴복학 가이드 | 2 |
| `kmu_student_support.py` | 증명서 발급 안내 | 3 |
| `kmu_schedule.py` | 휴복학·수강신청 일정 | 4 |
| `kmu_notice.py` | 2026-1 수강신청 공지 | 5 |
| `kmu_cradle.py` | 졸업 요람 | 6 |
| `kmu_org.py` | 학사·학생처 조직도 | 7 |
| `swell_public.py` | SWELL 공개 게시판 | 8 |

청크 순위 동률 시 **티어 낮은 쪽 우선**.

### 5.7 `data/`

| 하위 | 역할 |
|------|------|
| `raw/` | 크롤러 원본 HTML/JSON |
| `processed/chunks.jsonl` | **검색 진실의 원천**. 메타데이터: `source_tier`, `issue_types`, `keywords`, `search_hints`, `application_path`, `required_documents`, `submit_to`, `contacts`, `schedule`, `deadline_rule`, `actions` |
| `processed/notices_crawled.jsonl` | `scripts/crawl_notice.py` 프로브 출력 |
| `vector/chroma/` | Chroma SQLite 인덱스 (선택적 가속기) |
| `vector_db/` | 대체 벡터 저장소 슬롯 |
| `state/crawler_state.json` | 문서별 content_hash + ETag/Last-Modified |
| `actions/` | 액션 폼 스키마 정의 |

### 5.8 `tests/` (pytest, 18개 통과)

| 파일 | 커버리지 |
|------|----------|
| `conftest.py` | repo root 를 `sys.path` 에 주입 |
| `test_guard.py` | 학번/주민/PW/성적/연락처 차단 검증 |
| `test_classifier.py` | issue_type 분류 정확도 |
| `test_retriever.py` | 하이브리드 검색 결과 (수강신청 확인, 증명서) |
| `test_deadline.py` | 한국어 날짜 파싱·기한 계산 |
| `test_contact_router.py` | issue_type 별 부서 라우팅 |
| `test_actions.py` | 출석인정 슬롯 흐름·문서 초안 |
| `test_ingestion.py` | document→chunk 보존, 쿨다운 로직, fetch 요약 |

### 5.9 `frontend/`

- **스택**: Vite 5 + React 18.2 + 자체 CSS
- **빌드 산출물**: `frontend/dist` → FastAPI 가 `/` 와 `/assets` 로 서빙
- **주요 컴포넌트**
  - `App.jsx` — 라우팅·전체 레이아웃
  - `ChatPanel.jsx` — `/ask` 바인딩, 사용자 질문/답변 표시
  - `ActionForm.jsx` — `/actions/start` → `/actions/continue` 다단계 슬롯 폼
  - `SourcePanel.jsx` — 검색된 청크와 인용 노출
  - `ToolLogPanel.jsx` — classifier/retriever/guard/checklist/contact 도구 호출 로그
  - `AdminDashboard.jsx` — `/health`, `/ingest/run` 트리거, 크롤 상태

### 5.10 `scripts/` (학사공지 Playwright 프로브)

| 스크립트 | 용도 |
|----------|------|
| `crawl_notice.py` | KMU 학사공지 페이지네이션 워크 → `notices_crawled.jsonl`, 옵션으로 `chunks.jsonl` 머지 |
| `probe_notice_page.py` | `?currentPageNo=N` 페이지네이션 동작 확인 |
| `probe_notice_view.py` | 공지 #11798 본문 추출이 잘리는 문제 디버그 (`.view_cont`) |

## 6. 반드시 지켜야 할 가드레일 (`project_plan.md` §7)

1. 학번·주민번호·연락처·성적표 원본·포털 ID/PW **수집·반향 금지** — `agent/guard.PRIVACY_PATTERNS` 가 canonical
2. 공식 청크 없이 절차 답변 **금지** — `require_sources()` 가 차단
3. 로그인 필요 화면(ON국민, SWELL 개인 화면) · 에브리타임 **자동 크롤 금지**
4. LLM 도입 시에도 **검색된 청크만 소비** + **인용 마커 보존**
5. `cite(chunk, labels)` 부착 — 모든 사실 문장이 `[근거]` 블록의 출처와 매칭되어야 함

## 7. 알려진 다음 단계 / 미해결

- `llm_client` 에 실제 모델 연결 (현재 결정론 템플릿만)
- HWP / OCR 첨부파일 처리 (`file_extractors.py` 에서 미지원 선언만)
- `scripts/probe_notice_view.py` 의 본문 절단 문제
- `data/vector_db/` (대체 저장소) 정리 여부 결정
