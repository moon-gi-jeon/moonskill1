# moonskill1

Codex용 소규모 Skill 모음. 과제 진행에 필요한 지침만 선택해서 **현재 작업 프로젝트**에 등록합니다. 개인 모델 키·새 AI·MCP·Plugin·전역 설정·Codex 업데이트를 요구하지 않습니다. 공식 제품/대회 자료가 아닌 개인 준비 묶음입니다.

## Codex에 자연어로 한 번 요청하기

아래는 일반 셸 명령이 아니라 **Codex 자연어 입력란**에 보낼 요청입니다.

> 공개 저장소 https://github.com/moon-gi-jeon/moonskill1 의 README와 manifest.json을 확인해라. 현재 과제 프로젝트 위치를 확인하고 저장소를 별도 참고 폴더로 가져와라. 기본 core Skills를 현재 프로젝트의 .agents/skills에 등록해라. 기존 지침과 Skills를 덮어쓰지 말고 전역 설정·모델·인증·Codex 버전을 바꾸지 마라. 설치 파일과 해시를 확인하고, /skills 또는 $ 선택 목록에서 인식되는지 확인하라. 목록 확인을 수행할 수 없으면 파일 설치 성공과 인식 미확인을 구분해 보고하라. 그다음 grill-me와 grilling을 적용해 현재 과제의 중요한 미결정 사항만 짧게 점검해라.

**clone은 파일을 가져오는 작업, 설치/등록은 Codex가 찾는 프로젝트 경로에 놓는 작업, 호출은 해당 지침을 실제 사용하는 작업**입니다. 하위 폴더에 clone한 것만으로 기존 작업 세션이 모든 Skill을 발견한다고 가정하지 않습니다.

## 포함한 Skills

| 이름 | 기본/조건부 | 용도 |
|---|---|---|
| `grill-me` | core | 계획·요구의 미결정 사항을 질문하는 진입점 |
| `grilling` | core 의존 | grill-me의 질문 절차. 함께 설치 |
| `verification-before-completion` | core | 완료 선언 전 실제 명령·출력·요구 충족 대조 |
| `frontend-design` | UI 필요 시 | 화면의 정보 배치·상태·문구·시각 설계 |
| `diagnosing-bugs` | 반복 오류 시 | 재현→원인 분리→수정→회귀 검사 |
| `api-tester` | 업무 API 필요 시 | 허용 API의 문서·응답·페이지·오류 검사 |

여러 Skill을 함께 보관·등록할 수 있으며 각 폴더는 별도 SKILL.md를 갖습니다. 등록된 모든 본문을 매 요청마다 전부 읽히지는 않습니다. 과제에 맞는 Skill만 호출합니다. 이 묶음의 `all`은 연결 검증용 선택지이며 시험 기본안은 `core`입니다. API가 필요 없으면 api-tester는 설치하지 않습니다.

## 셸에서 수동 설치할 경우

현재 과제 프로젝트에서 실행하는 예입니다. 같은 참고 폴더가 이미 있으면 먼저 내용을 확인해 재사용합니다. Python 명령이 `python`인 환경은 `python3` 대신 그 명령을 사용합니다.

```sh
git clone https://github.com/moon-gi-jeon/moonskill1.git moonskill1-reference
python3 moonskill1-reference/install.py --project .
python3 moonskill1-reference/install.py --project . --apply
```

첫 실행은 dry run입니다. `--apply`를 붙이면 검증 후 복사합니다. 기본 3개만 설치하며 다른 내용의 동명 폴더는 보존하고 중단합니다. 필요할 때 추가합니다.

```sh
python3 moonskill1-reference/install.py --project . --skills frontend-design --apply
python3 moonskill1-reference/install.py --project . --skills diagnosing-bugs --apply
python3 moonskill1-reference/install.py --project . --skills api-tester --apply
```

가상 연결 시험에서 전체 6개를 설치하려면 `--profile all --apply`를 사용합니다. Python이 제공되지 않거나 설치 실행이 허용되지 않으면, Codex가 manifest의 필요한 `skills/<name>/` 전체를 프로젝트 `.agents/skills/<name>/`로 복사하고 해시·의존을 확인하는 방법을 쓸 수 있습니다. 차단을 우회하지 않습니다.

## 발견과 실제 사용 확인

1. 현재 작업 폴더의 `.agents/skills/<name>/SKILL.md`와 참조·라이선스를 확인합니다.
2. 제공 Codex의 `/skills` 또는 `$` 입력으로 이름을 확인합니다. 기존 세션에 반영되지 않으면 현재 버전의 정상적인 갱신/새 세션 방법을 사용합니다. 버전을 업데이트하지 않습니다.
3. `$grill-me 내 계획의 미결정 사항을 점검해라`처럼 호출합니다. 목록 표시와 실제 파일 읽기·결과 적용은 별도입니다.
4. 미인식 시 실제 SKILL.md 경로를 지정해 읽게 할 수 있으나, 이는 `$` 메뉴 등록 성공과 구별합니다.

다른 위치에 동명 Skill이 있으면 프로젝트 경로를 명시해 어느 파일을 적용했는지 확인합니다. 다른 Skill을 지우거나 전역 설정을 바꾸지 않습니다.

## 별도 하네스

추가 실행형 하네스는 기본 설치하지 않습니다. Codex의 기존 실행 체계를 이용합니다. 필요하면 [짧은 작업 진행 지침](guides/EXAM_WORKFLOW.md)을 읽혀 과제 범위·지침 선택·검증·인계를 정리할 수 있습니다. 이 문서는 선택 자료이며 자동 실행/강제 통제 프로그램이 아닙니다.

## 사용 경계와 출처

실제 환경의 최신 공식 안내·과제 지시가 우선합니다. 개인 파일 업로드 대신 허용된 공개 원본 반입 경로를 사용합니다. 이 저장소는 시험 결과 통지 전까지 공개 유지하는 준비용입니다. 실제 문제·세션·데이터·결과물·인증을 이 저장소에 올리지 않습니다. 제공 AI/인증·관리 설정을 바꾸거나 자동 화면 조작·부하/파괴적 API 검사를 수행하지 않습니다.

frontend-design은 Anthropic 작성 지침을 Codex가 읽는 것이며 Claude를 연결하지 않습니다. 공개 지침의 원문·라이선스·고정 버전·수정 범위는 [출처와 변경](SOURCES.md), [manifest](manifest.json), [제3자 고지](THIRD_PARTY_NOTICES.md)를 확인하세요. 설치 해시 검증은 코드 안전·시험 호환·Skill 효용 보장이 아닙니다.

Codex의 일반 발견/호출 방식: [OpenAI 공식 Skills 문서](https://learn.chatgpt.com/docs/build-skills). 실제 제공 시험 버전은 해당 환경에서 확인해야 합니다.
