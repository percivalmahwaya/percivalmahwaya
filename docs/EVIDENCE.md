# Evidence behind the skills table

Counts below come from the repositories, read on 2026-10-30.

| Claim in the README | How it was counted | Result |
|---|---|---|
| fpl-decision-engine has 77 test functions | `def test_` in `test_bench.py` (30), `test_challenger.py` (12), `test_migrate.py` (16), `test_transfers.py` (19) | 77 |
| fpl-decision-engine runs checks in CI | `.github/workflows/fpl.yml` runs `qa.py --all` and `qa_deploy.py` | Last run succeeded 2026-10-29 |
| bcaChessHub has 260 test functions | `def test_` across the repository | 260 |
| bcaChessHub has no CI test run | `.github/workflows` does not exist. The only Actions run is the dependency graph update | No CI yet |
| bcaChessHub has 8 apps | README architecture table | 8 |
| Crime Hotspot DSS AUC-ROC 0.966, next best 0.867 | `data/model_comparison.csv`, Random Forest 0.9663, KNN 0.8666 | Matches |
| OSP Scout has 169 test assertions | OSP Scout README, five suites run in `publish.yml` before each publish | Private repository |
| Docker, Terraform, Kubernetes | No Dockerfile or `.tf` file in any repository. `docker-learning` is empty | Listed as learning |

How the Latest section is built: `tools/refresh.py` reads `site/data/accuracy.json` and the run history of the FPL pipeline, and lists recent commits from six public repositories. It exits non-zero if any source is empty, so a green run means each source returned data.
