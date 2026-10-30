# moonskill1

Codex용 소규모 Skill 모음. **기본 설치는 선정된 7개 전체(`all`)**를 현재 작업 프로젝트에 등록합니다. 실제 작업에서는 필요한 지침만 사용합니다. 개인 모델 키·새 AI·MCP·Plugin·전역 설정·Codex 업데이트를 요구하지 않습니다. 개인이 관리하는 독립 도구 모음입니다.

## Codex에 자연어로 한 번 요청하기

아래는 일반 셸 명령이 아니라 **Codex 자연어 입력란**에 보낼 요청입니다.

> 허용된 공개 HTTPS 경로로 https://github.com/moon-gi-jeon/moonskill1 의 README와 manifest.json을 읽어라. 현재 작업 프로젝트와 Codex의 Skill 탐색 경로를 확인하고, 선정된 7개 전체(all)를 프로젝트 .agents/skills에 설치해라. 기존 다른 파일·전역 설정·모델·인증·Codex 버전은 변경하지 마라. 파일 설치·해시 검증과 현재 Codex의 $ 목록 인식 여부를 구분해 간결히 보고해라. 지침 본문은 이후 작업에 필요한 것만 읽고 적용해라.

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
| `api-and-interface-design` | API 구현·변경 시 | 화면/서버의 요청·응답·검증·저장 계약 설계 |

여러 Skill을 함께 보관·등록할 수 있으며 각 폴더는 별도 SKILL.md를 갖습니다. 기본 `all`은 위 7개를 설치하고, `core`는 앞의 3개만 설치하는 선택 옵션입니다. 표의 ‘조건부’는 **실제 사용 시점**을 뜻합니다. API가 없으면 api-tester와 api-and-interface-design을 사용하지 않습니다. api-and-interface-design은 core에 포함되지 않습니다. 등록된 모든 본문을 매 요청마다 전부 읽히지는 않습니다.

## 셸에서 수동 설치할 경우

현재 과제 프로젝트에서 실행하는 예입니다. 같은 참고 폴더가 이미 있으면 먼저 내용을 확인해 재사용합니다. Python 명령이 `python`인 환경은 `python3` 대신 그 명령을 사용합니다.

```sh
git clone https://github.com/moon-gi-jeon/moonskill1.git moonskill1-reference
python3 moonskill1-reference/install.py --project .
python3 moonskill1-reference/install.py --project . --apply
```

첫 실행은 dry run입니다. `--apply`를 붙이면 검증 후 7개 전체를 복사합니다. 동일한 기존 core 파일은 보존하고 빠진 4개만 추가합니다. 다른 내용의 동명 폴더는 보존하고 중단합니다. 이미 받은 구버전 사본은 허용된 공개 경로로 최신 버전을 다시 확인해야 합니다. core만 원하면 `--profile core --apply`를 지정합니다. 필요한 것만 개별 추가할 수도 있습니다.

```sh
python3 moonskill1-reference/install.py --project . --skills frontend-design --apply
python3 moonskill1-reference/install.py --project . --skills diagnosing-bugs --apply
python3 moonskill1-reference/install.py --project . --skills api-tester --apply
python3 moonskill1-reference/install.py --project . --skills api-and-interface-design --apply
```

전체 7개를 명시하려면 `--profile all --apply`를 사용합니다. Python이 제공되지 않거나 설치 실행이 허용되지 않으면, Codex가 manifest의 `skills/<name>/` 전체를 프로젝트 `.agents/skills/<name>/`로 복사하고 해시·의존을 확인하는 방법을 쓸 수 있습니다. 차단을 우회하지 않습니다.

## 발견과 실제 사용 확인

1. 현재 작업 폴더의 `.agents/skills/<name>/SKILL.md`와 참조·라이선스를 확인합니다.
2. 제공 Codex의 `/skills` 또는 `$` 입력으로 이름을 확인합니다. 기존 세션에 반영되지 않으면 현재 버전의 정상적인 갱신/새 세션 방법을 사용합니다. 버전을 업데이트하지 않습니다.
3. `$grill-me 내 계획의 미결정 사항을 점검해라`처럼 호출합니다. 목록 표시와 실제 파일 읽기·결과 적용은 별도입니다.
4. 미인식 시 실제 SKILL.md 경로를 지정해 읽게 할 수 있으나, 이는 `$` 메뉴 등록 성공과 구별합니다.

다른 위치에 동명 Skill이 있으면 프로젝트 경로를 명시해 어느 파일을 적용했는지 확인합니다. 다른 Skill을 지우거나 전역 설정을 바꾸지 않습니다.

## 별도 하네스

추가 실행형 하네스는 기본 설치하지 않습니다. Codex의 기존 실행 체계를 이용하며 작업 범위와 필요한 Skill을 실제 프로젝트에 맞춰 정합니다.

## 사용 경계와 출처

실제 환경의 지침·작업 계약이 우선합니다. 허용된 공개 원본 취득 경로를 사용합니다. 비공개 작업 자료·세션·데이터·결과물·인증을 이 저장소에 올리지 않습니다. 제공 AI/인증·관리 설정을 바꾸거나 자동 화면 조작·부하/파괴적 API 검사를 수행하지 않습니다.

frontend-design은 Anthropic 작성 지침을 Codex가 읽는 것이며 Claude를 연결하지 않습니다. 공개 지침의 원문·라이선스·고정 버전·수정 범위는 [출처와 변경](SOURCES.md), [manifest](manifest.json), [제3자 고지](THIRD_PARTY_NOTICES.md)를 확인하세요. 설치 해시 검증은 코드 안전·대상 환경 호환·Skill 효용 보장이 아닙니다.

Codex의 일반 발견/호출 방식: [OpenAI 공식 Skills 문서](https://learn.chatgpt.com/docs/build-skills). 실제 사용 버전은 해당 환경에서 확인해야 합니다.

core만 설치하는 자연어 요청: "현재 프로젝트에 core 3개만 설치해줘. all/추가 API·UI Skill은 설치하지 마라." 기존에 설치된 추가 Skill을 자동 삭제하지는 않습니다.
