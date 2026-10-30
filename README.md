# Percival Mahwaya

Data and platform engineer in Katowice, Poland.

I build systems which run, then publish how well they run. I hold an MSc in Data Science (Akademia WSB, 2026). Before the degree I spent more than five years in law-enforcement IT in Zimbabwe, where a wrong record led to a wrong action. Today I work as a functional QA tester at Keywords Studios.

Open to data, platform and research roles. Open to relocating to Ireland or Australia.

[Portfolio](https://percivalmahwaya.github.io) · [LinkedIn](https://linkedin.com/in/percivalmahwaya) · [Contact page](https://percivalmahwaya.github.io/contact.html)

## Topics I talk about

- Judging a forecast: held-out seasons, noise floors, models built to show where they lose
- Scheduled data pipelines which retrain and publish without me
- Django systems which take payments and keep administrators behind two-factor login
- Release checks run against the deployed system
- Applied machine learning for public safety

## Skills, with proof

Each row links to the file which shows the skill. The last column says what checks it.

| Skill | Proof | What checks it |
|---|---|---|
| Forecast modelling and evaluation (Python, pandas, scikit-learn) | [model.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/model.py), [DECISION_LOG.md](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/DECISION_LOG.md) | Data, leakage and model checks in [qa.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/qa.py), run by the pipeline |
| Optimisation (mixed-integer programming with SciPy) | [optimise.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/optimise.py) | [test_challenger.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/test_challenger.py), 12 tests |
| SQL and schema migration (SQLite) | [migrate.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/migrate.py) | [test_migrate.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/test_migrate.py), 16 tests |
| Scheduled pipelines on GitHub Actions | [fpl.yml](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/.github/workflows/fpl.yml), every three hours | Run history in the Latest section below |
| Alerting | [alert.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/alert.py) | Runs inside the same pipeline |
| Django and PostgreSQL | [bcaChessHub README](https://github.com/percivalmahwaya/bcachesshub/blob/master/README.md), 8 apps | 260 test functions. No CI run yet |
| Payments and authentication | [members/middleware.py](https://github.com/percivalmahwaya/bcachesshub/blob/master/members/middleware.py), [CHANGELOG.md](https://github.com/percivalmahwaya/bcachesshub/blob/master/CHANGELOG.md) | Changelog records two payment flaws I found and closed |
| Checks against a deployed system | [qa_production.py](https://github.com/percivalmahwaya/bcachesshub/blob/master/qa_production.py), [qa_deploy.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/qa_deploy.py) | Run by me before each release |
| Dashboards (Streamlit) | [app.py](https://github.com/percivalmahwaya/crime-hotspot-dss/blob/master/app.py), [master_dashboard.py](https://github.com/percivalmahwaya/team-project-semester4/blob/master/master_dashboard.py) | Live dashboard in Selected work |
| Machine learning for public safety | [model_comparison.csv](https://github.com/percivalmahwaya/crime-hotspot-dss/blob/master/data/model_comparison.csv) | Four models compared on one table |
| Framework-free web (HTML, CSS, JavaScript) | [Portfolio source](https://github.com/percivalmahwaya/percivalmahwaya.github.io) | Source is public. No CI yet |

OSP Scout is a private repository. Its pipeline validates a published data contract and runs five test suites before every publish. I show it on request.

## Still learning

Docker, Terraform and Kubernetes. I have no public proof of them yet, so I do not list them as skills. I hold the AWS Solutions Architect Associate certificate. No AWS project is public yet.

## Selected work

| Project | What it does | Numbers |
|---|---|---|
| [FPL Decision Engine](https://github.com/percivalmahwaya/fpl-decision-engine) · [live](https://percivalmahwaya.github.io/fpl-decision-engine/) | Retrains, predicts, scores itself and republishes every three hours. Backtested against FPL's own expected points on a held-out season. | 77 test functions. Four models on one public scoreboard |
| [Bulawayo Chess Hub](https://github.com/percivalmahwaya/bcachesshub) · [live](https://web-production-abe9b.up.railway.app) | Tournament administration for a chess association: Swiss pairing, Elo ratings, Lichess sign-in, Paynow payments. | 260 test functions. 8 Django apps |
| [Crime Hotspot DSS](https://github.com/percivalmahwaya/crime-hotspot-dss) · [live](https://crime-hotspot-dss-8d2jrkagpvgsegqp6y23d4.streamlit.app/) | My MSc thesis as a dashboard. A Random Forest sorts Chicago police beats into three patrol tiers. The free host sleeps when idle and wakes in about a minute. | AUC-ROC 0.966. Next best model 0.867 |
| OSP Scout · [live](https://osp-scout.pages.dev) | Read-only Fantasy Premier League companion for a friend group. It holds no credentials. | 169 test assertions. Private repository |
| [Portfolio](https://github.com/percivalmahwaya/percivalmahwaya.github.io) · [live](https://percivalmahwaya.github.io) | Three case studies, each with what went wrong. | Plain HTML, CSS and JavaScript |
| [SIPDiDS dashboard](https://github.com/percivalmahwaya/team-project-semester4) | Team project joining Reddit sentiment, stock, movie and publication data. I coordinated the team. | 5 data sources, 5 team members |

## Latest

Updated by a workflow. The workflow fails if a source returns nothing.

<!-- latest:start -->
FPL Decision Engine scoreboard, gameweek 8: model error (MAE) 1.075 against 1.247 and 1.347 for the two baselines. Lower is better. It loses on high-return players: 5.191 against 4.877 and 4.884. Only 5 gameweeks are scored.

FPL pipeline: the last completed run succeeded on 2026-10-29 18:31 UTC.

Recent commits:

- 2026-10-11 [percivalmahwaya.github.io](https://github.com/percivalmahwaya/percivalmahwaya.github.io/commit/283eda2791d2b06acdb4b62ed52b8092bbe9671e): add .nojekyll: a Liquid tag in an ADR was hanging the Pages build
- 2026-10-11 [percivalmahwaya.github.io](https://github.com/percivalmahwaya/percivalmahwaya.github.io/commit/9cbf1af793afe152380a3a8551341762b352985a): correct a wrong "not live" call, and the stale memory behind it
- 2026-10-11 [percivalmahwaya.github.io](https://github.com/percivalmahwaya/percivalmahwaya.github.io/commit/617ca1ed592eb1816241cc4ea000f5024397c612): redesign the site: dark/light editorial rebuild, spec-first
- 2026-10-10 [percivalmahwaya.github.io](https://github.com/percivalmahwaya/percivalmahwaya.github.io/commit/d2a9b54d2919474ae64fa8874e348b29468439d6): add bcaChessHub, Progeny FPL engine, OSP Scout, and chess economics research ...
- 2026-10-01 [bcachesshub](https://github.com/percivalmahwaya/bcaChessHub/commit/be4d8a94088a04c52f74f037bfac1bd9339e9d11): require 2FA for administrator accounts, fix stale pending-list items

<sub>Refreshed 2026-10-30 00:30 UTC by tools/refresh.py.</sub>
<!-- latest:end -->
