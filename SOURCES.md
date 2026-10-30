# 출처·수정 범위

원본 전체를 무검증 설치하는 패키지가 아니다. 아래 고정 버전에서 지침을 선별하고 제공 환경에 맞게 좁힌 수정본이다. 원저작자의 공식 배포나 보증을 의미하지 않는다.

| Skill | 원본 | 커밋 | 라이선스 | 수정 |
|---|---|---|---|---|
| grill-me | [mattpocock/skills](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/grill-me/SKILL.md) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | MIT | Replaced host-specific wrapper with a relative read of sibling grilling; removed Claude-only frontmatter; retained explicit invocation policy from existing Codex metadata. |
| grilling | [mattpocock/skills](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/grilling/SKILL.md) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | MIT | Limit interview to material task decisions; inspect local facts first; make delegation conditional on available permitted tools; continue authorized work after decisions are answered. |
| verification-before-completion | [obra/superpowers](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | MIT | Add task-scoped validation guidance; no zero-test/fully-skipped success; no new tooling merely to satisfy a generic checklist. |
| frontend-design | [anthropics/skills](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design/SKILL.md) | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Apache-2.0 | Retain design guidance; replace automated screenshot review with participant manual preview; prioritize actual task workflow over visual expansion. |
| diagnosing-bugs | [mattpocock/skills](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/diagnosing-bugs/SKILL.md) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | MIT | Replace headless-browser/HITL script requirements with local CLI/HTTP tests and participant manual preview; restrict load and external operations. |
| api-tester | [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang/blob/acf2587e46be174c10200489c9a2d23a39a98aeb/crates/openfang-skills/bundled/api-tester/SKILL.md) | `acf2587e46be174c10200489c9a2d23a39a98aeb` | MIT/Apache-2.0 | Restrict to task-authorized business API; remove rapid rate-limit probing, secret-bearing verbose traces and alternate-network advice; no external model API. |

각 전달 파일의 SHA-256은 manifest.json에 있다. input_snapshot_sha256은 조사에 사용한 보존본의 해시이며 수정 후 전달 파일 해시와 구분한다. grill-me의 조사 보존본에는 이미 로컬 경로 이식이 있었고 이번에 표준 frontmatter와 자체 상대 경로 진입부로 정리했다.

