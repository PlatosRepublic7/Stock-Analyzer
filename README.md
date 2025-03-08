# Stock-Analyzer

Stock-Analyzer is a simple web application designed to visualize Dow Jones Industrial Average Stock data. Specifically, it aims to make use of OHLCV data (daily "candles") in order to forecast what these candles will be in the future. It is a project aimed to develop my skills in a variety of areas, and is not intended to be a comprehensive real-time market analysis tool.

## Features
- **Data Collection:** Retrieve OHLCV data from [AlphaVenture](https://www.alphavantage.co/) and [Finnhub](https://finnhub.io/).
- **Data Processing:** Clean and transform raw data for analysis.
- **Analytical Tools:** Apply various statistical models for future stock pricing. (Actively Developing)
- **Visualization:** Create interactive charts and graphs for a clearer understanding of stock data, and forecasting analysis. (Coming Soon...)
- **Reporting:** Generate detailed reports summarizing analytical insights. (Coming Soon...)

## Getting Started

## Prerequisites

- Python 3.8 or higher
- Requred Python libraries (see [requirements.txt](requirements.txt))
- API Keys for AlphaVantage and Finnhub (free-tier for both)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/PlatosRepublic7/Stock-Analyzer.git
    ```

2. **Install the necessary dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up database and environment variables:** This project uses [PostgreSQL](https://www.postgresql.org/download/) for a database solution. Once this is installed on your system, create a new database (for example `market_data`) with a blank schema. To ensure proper connectivity for the application, create a file in the root of the application directory called `.env` and put in the database and api-key information:
    ```bash
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=your_password_goes_here
    DB_NAME=market_data
    FINNHUB_API_KEY=your_finnhub_api_key_goes_here
    ALPHA_VANTAGE_API_KEY=your_alphavantage_api_key_goes_here
    DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
    ```

4. **Set up Alembic and migrate database models:** This project makes use of SQLAlchemy's ORM functionality, as well as Alembic for database migrations. In order to apply the current database schema, some preliminary setup for Alembic is required. Upon installing the requirements for this project, a file names `alembic.ini` will be created in the root directory. The only alteration to this file that is required is the following:
    ```bash
    ...
    # the output encoding used when revision files
    # are written from script.py.mako
    # output_encoding = utf-8

    sqlalchemy.url = postgresql://postgres:your_password_goes_here@localhost:5432/market_data
    ```

Once you have made this update, run the following commands to apply the initial migration:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```
    ```bash
    alembic upgrade head
    ```
    

## Running the project

To run the application, simply run the following command:
```bash
python -m app.main
```