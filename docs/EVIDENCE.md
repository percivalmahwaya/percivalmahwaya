# Evidence behind the skills table

Counts below come from the repositories, re-verified 2026-11-08 (originally read 2026-10-30 - the
OSP Scout count had already drifted in those 9 days, which is the whole reason this file exists
rather than typing numbers straight into the README).

| Claim in the README | How it was counted | Result |
|---|---|---|
| fpl-decision-engine has 77 test functions | `python -m unittest test_bench.py test_challenger.py test_migrate.py test_transfers.py -v`, run fresh | 77 |
| fpl-decision-engine runs checks in CI | `.github/workflows/fpl.yml` runs `qa.py --all` and `qa_deploy.py`; triggered a real run | Succeeded 2026-11-08 |
| bcaChessHub has 260 test functions | `python manage.py test`, run fresh | 260 |
| bcaChessHub has no CI test run | `gh api repos/percivalmahwaya/bcaChessHub/contents/.github/workflows` | 404 - no CI yet |
| bcaChessHub has 8 apps | App folders under the Django project root: associations, core, matches, members, news, notifications, payments, tournaments | 8 |
| Crime Hotspot DSS AUC-ROC 0.966, next best 0.867 | `data/model_comparison.csv`, Random Forest 0.9663, KNN 0.8666 | Matches |
| OSP Scout has 193 test assertions | Real CI run, 2026-11-08: 97 (schema) + 30 (decide) + 18 (gw_state) + 32 (reselect) + 16 (design_tokens) | 193, up from 169 on 2026-10-30 |
| Docker, Terraform, Kubernetes | `gh api search/code` for `filename:Dockerfile` across all six public repos | 0 hits - still listed as learning |

How the Latest section is built: `tools/refresh.py` reads `site/data/accuracy.json` and the run history of the FPL pipeline, and lists recent commits from six public repositories. It exits non-zero if any source is empty, so a green run means each source returned data.
