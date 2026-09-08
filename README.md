\# FIFA World Cup 2026 Data Analysis



\## Project Overview



This project analyses FIFA World Cup 2026 data using statistical methods to

investigate differences in player and team performance.



The project consists of four analytical tasks focusing on attacking

performance, player discipline, goalkeeping performance, and team possession.



Python was used for data cleaning, preparation, sampling, visualisation,

descriptive statistics, confidence intervals, and hypothesis testing.



\---



\## Research Questions



\### Task 1 — Attacking Performance



\*\*Research Question:\*\*  

Do forwards and midfielders differ significantly in their average number of

assists during the FIFA World Cup 2026?



\- Dataset: Player Standard Stats

\- Variable: `Ast`

\- Groups: Forwards (FW) vs Midfielders (MF)

\- Focus: Attacking contribution

\- Statistical Test: Independent two-sample t-test



\### Task 2 — Player Discipline



\*\*Research Question:\*\*  

Do defenders and midfielders differ significantly in their average number of

yellow cards during the FIFA World Cup 2026?



\- Dataset: Player Standard Stats

\- Variable: `CrdY`

\- Groups: Defenders (DF) vs Midfielders (MF)

\- Focus: Player discipline

\- Statistical Test: Independent two-sample t-test



\### Task 3 — Goalkeeping Performance



\*\*Research Question:\*\*  

Do goalkeepers from teams that progressed to the knockout stage differ

significantly in average save percentage from goalkeepers whose teams were

eliminated in the group stage?



\- Dataset: Goalkeeping + Match Results

\- Variable: `Save%`

\- Groups: Knockout vs Group-stage elimination

\- Focus: Goalkeeping performance

\- Statistical Test: Independent two-sample t-test



\### Task 4 — Team Possession



\*\*Research Question:\*\*  

Do teams that progressed to the knockout stage have a significantly different

average possession percentage from teams eliminated in the group stage?



\- Dataset: Squad Possession + Match Results

\- Variable: `Poss`

\- Groups: Knockout vs Group-stage elimination

\- Focus: Team possession/control

\- Statistical Test: Independent two-sample t-test



\---



\## Methodology



Each analytical task follows a consistent statistical workflow:



1\. Define the research question and variables.

2\. Load and inspect the relevant FIFA World Cup datasets.

3\. Clean and prepare the data.

4\. Define the population and obtain an appropriate sample.

5\. Calculate descriptive statistics.

6\. Visualise the distributions and group differences.

7\. Calculate 95% confidence intervals.

8\. Check relevant statistical assumptions.

9\. Conduct an independent two-sample t-test.

10\. Interpret the results in relation to the research question.



A significance level of \*\*α = 0.05\*\* is used for hypothesis testing.



\---



\## Task 4 — Key Finding



The team possession analysis found that sampled teams progressing to the

knockout stage had higher average possession than teams eliminated during the

group stage.



| Group | Sample Size | Mean Possession |

|---|---:|---:|

| Group Eliminated | 12 | 43.02% |

| Knockout | 24 | 51.55% |



The observed difference in mean possession was \*\*8.53 percentage points\*\*.



Welch's independent two-sample t-test produced:



\- \*\*t(18.03) = 2.5553\*\*

\- \*\*p = 0.0199\*\*

\- \*\*Cohen's d = 0.980\*\*



Since the p-value was below 0.05, the null hypothesis was rejected. The

analysis therefore found a statistically significant difference in average

possession between the two progression groups within the analysed sample.



The large Cohen's d also suggests that the observed difference was substantial

in magnitude.



\---



\## Tools and Technologies



\- Python

\- Pandas

\- NumPy

\- SciPy

\- Matplotlib

\- Jupyter Notebook

\- Git

\- GitHub



\---



\## Project Structure



```text

Fifa-World-Cup-2026/

│

├── data/

│   ├── raw/

│   └── processed/

│

├── notebooks/

│   ├── task\_attacking\_shooting.ipynb

│   ├── player\_discipline.ipynb

│   ├── task4\_team\_possession\_analysis.ipynb

│   └── ...

│

├── README.md



