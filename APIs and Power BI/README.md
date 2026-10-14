# Call Center Analytics with Python, SQL Server, and Power BI

This project turns three months of call center history into a report showing resolved and unresolved calls for each agent.

## What callcenter.py does

1. Uses the Kaggle API to retrieve a dataset containing 5,000 call records covering three months.
2. Uses pandas to read and prepare the data.
3. Uses Microsoft ODBC to load the records into a Microsoft SQL Server database.
4. Makes the stored call history available to Power BI.

The Python script retrieves and loads the data. The chart is created separately in Power BI Desktop.

## Data workflow

Kaggle dataset -> Python and pandas -> Microsoft ODBC -> SQL Server -> Power BI -> PDF report

## Power BI report

The report uses a clustered column chart with two vertical bars for each agent:

| Chart field | Purpose |
| --- | --- |
| X-axis: Agent | Identifies the call center agent |
| Y-axis: Call count | Shows the total number of calls |
| Legend: Resolved = True | Shows resolved calls |
| Legend: Resolved = False | Shows unresolved calls |
| Data labels | Shows the count on each bar |

These are call counts, not resolution percentages. Consider differences in workload when comparing agents.

The exported PDF lets viewers see the report without installing Power BI Desktop.

## Technologies

- Python
- Kaggle API
- pandas
- Microsoft ODBC Driver for SQL Server
- Microsoft SQL Server
- Power BI Desktop

## Setup and usage

1. Install Python and the packages imported by callcenter.py.
2. Configure Kaggle API authentication locally.
3. Install the Microsoft ODBC driver version required by the script.
4. Configure your SQL Server connection and target table locally.
5. Run the script with: python callcenter.py
6. Open the Power BI report and connect to SQL Server.
7. Refresh the report and review the chart.
8. Export the report using File > Export > Export to PDF.

Exact package requirements, connection settings, and table setup depend on the implementation in callcenter.py.

## Project files

| File | Description |
| --- | --- |
| callcenter.py | Retrieves, processes, and loads the data |
| README.md | Explains the project |
| Power BI report (.pbix), if included | Contains the report visuals and connection configuration |
| Exported report (.pdf), if included | Shows resolved and unresolved calls by agent |

## Data source

Kaggle dataset: avishkarkanade/call-center-dataset.

Dataset usage and redistribution are subject to its license.

## Privacy

This README contains no passwords, API keys, account usernames, private server addresses, or personal call records. Keep credentials out of the public repository and review other project files before uploading them.

## Documentation scope

This README describes the supplied project workflow. The Python source code was not reviewed when preparing this documentation. Consult callcenter.py for exact transformations, database schema, and behavior when rerun.
