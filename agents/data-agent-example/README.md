# Data Agent Example

A simple Agent that contains actions that leverage Data Access.

## Datasources

Template builds on a demo PostgreSQL database, which everyone can access (read only) using these details:
Data Source: `PostgresCustomersDataSource` expects 
- **NAME**: public_demo
- **HOST**: data-access-public-demo-instance-1.chai8y6e2qqq.us-east-2.rds.amazonaws.com
- **PORT**: 5432
- **DATABASE**: postgres
- **USER**: demo_user
- **PASSWORD**: xyzxyzxyz

Two file data sources are:
* `FileSalesDataSource`: actions/MyActions/data-access-queries-template/files/sales_data.csv
* `FileChurnDataSource`: actions/MyActions/data-package-with-churn-prediction/files/customer-churn.csv


👉 Check [Action Server](https://github.com/Sema4AI/actions/tree/master/action_server/docs) and [Actions](https://github.com/Sema4AI/actions/tree/master/actions/docs) docs for more information.