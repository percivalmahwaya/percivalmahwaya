<img src="./assets/terminal.svg" width="100%" alt="Terminal window. Command: whoami --verbose. Output: name: Percival Mahwaya. role: Data and platform engineer. where: Katowice, Poland. degree: MSc Data Science, Akademia WSB, 2026. before: More than half a decade of law-enforcement IT. now: Functional QA tester, Keywords Studios. stack: Python, SQL, Django, GitHub Actions. open: Data, platform, research. Ireland or Australia.">

<p align="center">
  <a href="https://percivalmahwaya.github.io">Portfolio</a> ·
  <a href="https://linkedin.com/in/percivalmahwaya">LinkedIn</a> ·
  <a href="https://percivalmahwaya.github.io/contact.html">Contact</a> ·
  <a href="https://github.com/percivalmahwaya?tab=repositories">Repositories</a>
</p>

<p align="center">
  <img src="./assets/knights-tour.svg" width="360" alt="Animation of a knight's tour on a chessboard. A knight starts on a1 and visits all 64 squares exactly once in 63 moves, ending on h5. Each visited square is numbered in order.">
</p>

I build systems which run, then publish how well they run. I spent more than half a decade in law-enforcement IT in Zimbabwe, where a wrong record led to a wrong action. I also build chess software, so the animation above is a knight's tour.

### `$ cat topics.txt`

- Judging a forecast: held-out seasons, noise floors, models built to show where they lose
- Scheduled pipelines which retrain and publish without me
- Django systems with payments and two-factor administrator login
- Release checks run against the deployed system
- Applied machine learning for public safety

### `$ ls skills/`

Each row links to the file which shows the skill. Under each link is what checks it.

| Skill | Proof and check |
|---|---|
| Forecast modelling and evaluation (Python, pandas, scikit-learn) | [model.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/model.py), [DECISION_LOG.md](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/DECISION_LOG.md)<br>Data, leakage and model checks in [qa.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/qa.py), run by the pipeline |
| Optimisation (mixed-integer programming with SciPy) | [optimise.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/optimise.py)<br>[test_challenger.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/test_challenger.py), 12 tests |
| SQL and schema migration (SQLite) | [migrate.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/migrate.py)<br>[test_migrate.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/test_migrate.py), 16 tests |
| Scheduled pipelines on GitHub Actions | [fpl.yml](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/.github/workflows/fpl.yml), every three hours<br>Run history in the log at the bottom |
| Alerting | [alert.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/alert.py)<br>Runs inside the same pipeline |
| Django and PostgreSQL | [bcaChessHub README](https://github.com/percivalmahwaya/bcachesshub/blob/master/README.md), 8 apps<br>260 test functions. No CI run yet |
| Payments and authentication | [members/middleware.py](https://github.com/percivalmahwaya/bcachesshub/blob/master/members/middleware.py), [CHANGELOG.md](https://github.com/percivalmahwaya/bcachesshub/blob/master/CHANGELOG.md)<br>Changelog records two payment flaws I found and closed |
| Checks against a deployed system | [qa_production.py](https://github.com/percivalmahwaya/bcachesshub/blob/master/qa_production.py), [qa_deploy.py](https://github.com/percivalmahwaya/fpl-decision-engine/blob/main/qa_deploy.py)<br>Run by me before each release |
| Dashboards (Streamlit) | [app.py](https://github.com/percivalmahwaya/crime-hotspot-dss/blob/master/app.py), [master_dashboard.py](https://github.com/percivalmahwaya/team-project-semester4/blob/master/master_dashboard.py)<br>Live dashboard in work/ |
| Machine learning for public safety | [model_comparison.csv](https://github.com/percivalmahwaya/crime-hotspot-dss/blob/master/data/model_comparison.csv)<br>Four models compared on one table |
| Framework-free web (HTML, CSS, JavaScript) | [Portfolio source](https://github.com/percivalmahwaya/percivalmahwaya.github.io)<br>Source is public. No CI yet |

OSP Scout is a private repository: a pipeline which validates a data contract and runs five test suites before each publish. I show it on request.

Still learning: Docker, Terraform and Kubernetes. No public proof yet, so they are not listed as skills.

### `$ ls work/`

- [FPL Decision Engine](https://github.com/percivalmahwaya/fpl-decision-engine) · [live](https://percivalmahwaya.github.io/fpl-decision-engine/). Retrains, predicts, scores itself and republishes every three hours. 77 test functions.
- [Bulawayo Chess Hub](https://github.com/percivalmahwaya/bcachesshub) · [live](https://web-production-abe9b.up.railway.app). Tournament administration with Swiss pairing, Elo and Paynow payments. 260 test functions, 8 Django apps.
- [Crime Hotspot DSS](https://github.com/percivalmahwaya/crime-hotspot-dss) · [live](https://crime-hotspot-dss-8d2jrkagpvgsegqp6y23d4.streamlit.app/). My MSc thesis as a dashboard. AUC-ROC 0.966, next best model 0.867. The free host sleeps and wakes in about a minute.
- [Portfolio](https://github.com/percivalmahwaya/percivalmahwaya.github.io) · [live](https://percivalmahwaya.github.io). Three case studies, each with what went wrong.
- [SIPDiDS dashboard](https://github.com/percivalmahwaya/team-project-semester4). Team project over 5 data sources. I coordinated 5 people.

### `$ git log --oneline`

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

<p align="center">
  <a href="https://percivalmahwaya.github.io/contact.html"><code>$ echo "open to data, platform and research roles"</code></a>
  <br>
  <sub>Katowice, Poland. Open to Ireland and Australia.</sub>
</p>
