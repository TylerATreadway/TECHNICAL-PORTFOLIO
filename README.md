
None selected

Skip to content
Using Gmail with screen readers
Conversations
57% of 100 GB used
Terms · Privacy · Program Policies
Last account activity: 10 minutes ago
Details
README-3.md

# Tyler A. Treadway | Technical Portfolio

**Business Analysis · Quality Assurance · Python · API Integrations · Data Analytics**

Welcome to my technical portfolio. My background spans insurance technology, banking, business analysis, and software quality assurance. This repository brings together practical projects that demonstrate how I work with data, integrate systems, and communicate results.

## Featured Projects

| Project | Focus | Technologies |
| --- | --- | --- |
| [Call Center Analytics](APIs%20and%20Power%20BI/) | Import historical call data into SQL Server and visualize resolved and unresolved calls by agent | Python, Kaggle API, pandas, pyodbc, SQL Server, Power BI |
| [Social Security Retirement Calculator](Python-Portfolio/SSA-Retirement-Calculator/) | Explore estimated retirement benefit percentages at different claiming ages | Python, HTML, interactive browser charts |

### Call Center Analytics with Python, SQL Server, and Power BI

This project connects data collection, preparation, database storage, and reporting in one workflow. It uses a Kaggle dataset containing 5,000 historical call records from January through March 2021.

**Data workflow:** Kaggle API → Python and pandas → Microsoft ODBC → SQL Server → Power BI → PDF report.

The Python importer:

- Downloads the dataset through the Kaggle API or reads a local Excel workbook.
- Validates required columns, dates, call IDs, flags, and numeric values.
- Converts call information into typed records for SQL Server.
- Creates the `dbo.CallCenterCalls` table if it does not exist.
- Inserts missing call IDs without deleting or updating existing records.
- Supports a dry run that validates the data without changing the database.

Power BI connects to the SQL Server table and displays a clustered column chart with resolved and unresolved call counts for each agent. The report is also available as a PDF for easy review.

**Explore the project:**

- [Python importer](APIs%20and%20Power%20BI/CallCenter/import_call_center.py)
- [Power BI report (.pbix)](APIs%20and%20Power%20BI/PowerBI/BI_1.pbix)
- [Calls by Agent report (.pdf)](APIs%20and%20Power%20BI/PowerBI/Calls_By_Agent.pdf)
- [Project overview](APIs%20and%20Power%20BI/README.md)

This project demonstrates API-based data retrieval, data validation, SQL loading, and business reporting. The dataset is historical practice data rather than a live call center feed.

### Social Security Retirement Calculator

This Python project generates a standalone interactive HTML chart for exploring estimated retirement benefits at claiming ages from 62 through 70.

The browser interface allows users to:

- Enter a date of birth and review the calculated full retirement age.
- Compare estimated benefit percentages at different claiming ages.
- Enter an estimated monthly benefit at full retirement age to explore monthly and annual amounts.
- Adjust the chart without rerunning Python.

**Explore the project:**

- [Python source](Python-Portfolio/SSA-Retirement-Calculator/SSA_Retirement_Calc.py)
- [Interactive HTML file](Python-Portfolio/SSA-Retirement-Calculator/social_security_interactive.html)
- [Setup and usage instructions](Python-Portfolio/SSA-Retirement-Calculator/readme.md)

Download the HTML file and open it in a browser to use the interactive interface. It is an educational estimator, not an official Social Security benefit determination.

## Professional Background

### Plymouth Rock Assurance

- Experience with third-party data integrations in insurance workflows, including CARFAX.
- Validation of REST API exchanges and XML/XSLT data transformations.
- Python parsing and structured data handling.
- Data validation, testing, and investigation of discrepancies.

### TD Bank and Cape Cod Five

- Experience in banking and customer-focused financial services.
- Business-process understanding, clear communication, and attention to data accuracy.

## Skills Demonstrated

| Area | Skills |
| --- | --- |
| Data analytics | pandas, Excel data preparation, Power BI reporting |
| Database integration | SQL Server, Microsoft ODBC, pyodbc, parameterized inserts |
| Programming | Python scripting, validation, data parsing, HTML generation |
| API integrations | Kaggle API, REST API validation, XML, XSLT |
| Quality assurance | Functional testing, integration testing, data validation, defect investigation |
| Business analysis | Requirements communication, process understanding, documentation |

## Education and Professional Development

**Suffolk University**  
Bachelor of Arts in Advertising  
Minor in Information Systems

The [Certifications folder](Certifications/) provides a place for training records and credentials as they are added.

## Repository Navigation

- [APIs and Power BI](APIs%20and%20Power%20BI/) — Call center import and reporting project.
- [Python Portfolio](Python-Portfolio/) — Python applications and interactive tools.
- [Certifications](Certifications/) — Professional development documentation.

## Connect

[Tyler A. Treadway on GitHub](https://github.com/TylerATreadway)

---

These projects are presented for demonstration and learning.

Displaying README-3.md.
