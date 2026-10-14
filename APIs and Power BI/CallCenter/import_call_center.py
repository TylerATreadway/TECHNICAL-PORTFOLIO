"""Import 5,000 historical Kaggle calls (January-March 2021) into Winhost.

Windows setup (Python 3.10+):
  py -m pip install kaggle pandas openpyxl pyodbc
Install Microsoft ODBC Driver 18 for SQL Server separately.
Configure Kaggle authentication using https://www.kaggle.com/settings/api
(legacy kaggle.json goes in %USERPROFILE%\\.kaggle\\kaggle.json).
Do not share your Kaggle token or database password.

Run:      py import_call_center.py
Preview:  py import_call_center.py --dry-run
Offline preview of already downloaded workbook:
          py import_call_center.py --file "01 Call-Center-Dataset.xlsx" --dry-run

Uses KaggleApi, temporary downloads, typed SQL columns and parameterized inserts.
Creates dbo.CallCenterCalls; inserts missing IDs without deleting/updating existing
records. A single transaction commits only if the whole load succeeds.
Power BI: Get data > SQL Server; s18.winhost.com; DB_97863_as;
Database authentication; DB_97863_as_user; table dbo.CallCenterCalls.
Dataset: https://www.kaggle.com/datasets/avishkarkanade/call-center-dataset
This is historical practice data, not a live feed; real-world provenance has
not been independently established. Check the publisher's license before reuse.
"""

import argparse
import datetime as dt
import getpass
import os
from pathlib import Path
import tempfile

import pandas as pd

DATASET = 'avishkarkanade/call-center-dataset'
START, END = pd.Timestamp('2021-01-01'), pd.Timestamp('2021-04-01')
REQUIRED = ['Call Id', 'Agent', 'Date', 'Time', 'Topic', 'Answered (Y/N)',
            'Resolved', 'Speed of answer in seconds', 'AvgTalkDuration',
            'Satisfaction rating']


def seconds(value):
    if pd.isna(value):
        return None
    if isinstance(value, dt.time):
        return value.hour * 3600 + value.minute * 60 + value.second
    parts = str(value).strip().split(':')
    if len(parts) != 3:
        raise ValueError(f'Invalid duration: {value!r}')
    h, m, s = map(float, parts)
    if h < 0 or not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError(f'Invalid duration: {value!r}')
    return int(h * 3600 + m * 60 + s)


def clean(path):
    frame = pd.read_excel(path)
    frame.columns = frame.columns.str.strip()
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f'Dataset schema changed; missing columns: {sorted(missing)}')
    frame = frame[REQUIRED].copy()
    source_count = len(frame)
    frame['Date'] = pd.to_datetime(frame['Date'], errors='raise').dt.normalize()
    if frame['Date'].isna().any():
        raise ValueError('Missing call dates')
    frame = frame.loc[(frame['Date'] >= START) & (frame['Date'] < END)].copy()
    if set(frame['Date'].dt.month) != {1, 2, 3}:
        raise ValueError('Source does not contain all three requested months')
    for col, length in [('Call Id', 50), ('Agent', 100), ('Topic', 200)]:
        frame[col] = frame[col].astype('string').str.strip()
        if frame[col].isna().any() or frame[col].eq('').any():
            raise ValueError(f'Missing {col}')
        if frame[col].str.len().gt(length).any():
            raise ValueError(f'{col} exceeds SQL column length')
    frame = frame.drop_duplicates()
    if frame['Call Id'].duplicated().any():
        raise ValueError('Conflicting duplicate call IDs; refusing ambiguous records')
    for col in ['Answered (Y/N)', 'Resolved']:
        frame[col] = frame[col].astype('string').str.strip().str.upper()
        if not frame[col].isin(['Y', 'N']).all():
            raise ValueError(f'Invalid flag in {col}')
    for col in ['Speed of answer in seconds', 'Satisfaction rating']:
        frame[col] = pd.to_numeric(frame[col], errors='raise')
        values = frame[col].dropna()
        if (values < 0).any() or (values % 1 != 0).any():
            raise ValueError(f'Invalid numeric value in {col}')
    if not frame['Satisfaction rating'].dropna().between(1, 5).all():
        raise ValueError('Satisfaction rating outside 1-5')
    records = []
    for row in frame.to_dict('records'):
        time_value = row['Time']
        if pd.isna(time_value):
            raise ValueError('Missing call time')
        time_value = time_value if isinstance(time_value, dt.time) else dt.time.fromisoformat(str(time_value).strip())
        number = lambda key: None if pd.isna(row[key]) else int(row[key])
        records.append((str(row['Call Id']), str(row['Agent']),
                        dt.datetime.combine(row['Date'].date(), time_value),
                        str(row['Topic']), row['Answered (Y/N)'] == 'Y',
                        row['Resolved'] == 'Y', number('Speed of answer in seconds'),
                        seconds(row['AvgTalkDuration']), number('Satisfaction rating'), DATASET))
    print(f'Source rows: {source_count}; cleaned three-month rows: {len(records)}')
    print(frame.groupby(frame['Date'].dt.to_period('M')).size().to_string())
    return records


DDL = """
IF OBJECT_ID(N'dbo.CallCenterCalls', N'U') IS NULL
CREATE TABLE dbo.CallCenterCalls (
    CallID nvarchar(50) NOT NULL PRIMARY KEY,
    Agent nvarchar(100) NOT NULL,
    CallDateTime datetime2(0) NOT NULL,
    Topic nvarchar(200) NOT NULL,
    Answered bit NOT NULL,
    Resolved bit NOT NULL,
    AnswerSpeedSeconds int NULL CHECK (AnswerSpeedSeconds >= 0),
    TalkDurationSeconds int NULL CHECK (TalkDurationSeconds >= 0),
    SatisfactionRating int NULL CHECK (SatisfactionRating BETWEEN 1 AND 5),
    SourceDataset nvarchar(200) NOT NULL,
    ImportedAtUTC datetime2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
"""
INSERT = """
INSERT INTO dbo.CallCenterCalls
 (CallID,Agent,CallDateTime,Topic,Answered,Resolved,AnswerSpeedSeconds,
  TalkDurationSeconds,SatisfactionRating,SourceDataset)
SELECT ?,?,?,?,?,?,?,?,?,?
WHERE NOT EXISTS (
 SELECT 1 FROM dbo.CallCenterCalls WITH (UPDLOCK,HOLDLOCK) WHERE CallID=?
);
"""


def odbc_value(value):
    return '{' + value.replace('}', '}}') + '}'


def load(records):
    import pyodbc
    driver = 'ODBC Driver 18 for SQL Server'
    if driver not in pyodbc.drivers():
        raise RuntimeError('Install Microsoft ODBC Driver 18 for SQL Server first')
    password = os.environ.get('WINHOST_SQL_PASSWORD') or getpass.getpass('Winhost SQL password: ')
    connection_string = ';'.join([
        'DRIVER=' + odbc_value(driver), 'SERVER=s18.winhost.com',
        'DATABASE=DB_97863_as', 'UID=DB_97863_as_user',
        'PWD=' + odbc_value(password), 'Encrypt=yes', 'TrustServerCertificate=yes'])
    connection = pyodbc.connect(connection_string, timeout=30, autocommit=False)
    try:
        cursor = connection.cursor()
        cursor.execute('SET XACT_ABORT ON;')
        cursor.execute(DDL)
        inserted = 0
        for record in records:
            cursor.execute(INSERT, *(record + (record[0],)))
            inserted += max(cursor.rowcount, 0)
        connection.commit()
        print(f'Committed {inserted} new calls; {len(records)-inserted} IDs already existed.')
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', help='Download and validate only; no SQL connection')
    parser.add_argument('--file', type=Path, help='Use an already downloaded workbook')
    args = parser.parse_args()
    if args.file:
        records = clean(args.file)
    else:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        with tempfile.TemporaryDirectory(prefix='callcenter_') as folder:
            api.dataset_download_files(DATASET, path=folder, unzip=True, quiet=False)
            files = list(Path(folder).rglob('*.xlsx'))
            if len(files) != 1:
                raise ValueError(f'Expected one Excel workbook, found {len(files)}')
            records = clean(files[0])
    if args.dry_run:
        print('Dry run complete. No database changes made.')
    else:
        load(records)


if __name__ == '__main__':
    main()
