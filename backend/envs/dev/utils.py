import pandas as pd
from database.database_manager import DatabaseManager
from database.table_manager import TableManager
from database.table_metadata_manager import TableMetadataManager
from utils.utils import get_app_logger

logger = get_app_logger(__name__)


def seed_db():
    """
    Asynchronously seed the client database with sample data from CSV files.

    The function only creates tables that don't already exist in the database.

    Internal Variables:
    - sample_tables: Dictionary mapping table names to corresponding CSV file names.
    - existing_tables: List of table names that already exist in the database.
    - session: Database session managed by DatabaseManager.
    - manager: Instance of TableManager for table operations.

    Workflow:
    1. Initialize `sample_tables` dictionary to hold table-to-file mappings.
    2. Use DatabaseManager to create a session and TableManager to get existing table names.
    3. Loop through `sample_tables` and create tables if they don't exist, using data from CSV files.
    """

    # Get existing tables
    with DatabaseManager() as session:
        table_manager = TableManager(session)
        existing_tables = table_manager.list_all_tables()

        # Create sample table if it doesn't exist
        if "sample_sales" not in existing_tables:
            df = pd.read_csv("envs/dev/sample_data/sample_sales_data.csv")
            df.columns = map(str.lower, df.columns)
            table_manager.create_table_from_df(
                df=df, org_id=1, table_name="sample_sales"
            )

            # Add metadata
            metadata_manager = TableMetadataManager(session)
            metadata_manager.add_table_metadata(
                table_name="sample_sales",
                create_query="""
                    CREATE TABLE sample_sales (
                        ordernumber BIGINT,
                        quantityordered BIGINT,
                        priceeach DOUBLE PRECISION,
                        orderlinenumber BIGINT,
                        sales DOUBLE PRECISION,
                        orderdate TEXT,
                        status TEXT,
                        qtr_id BIGINT,
                        month_id BIGINT,
                        year_id BIGINT,
                        productline TEXT,
                        msrp BIGINT,
                        productcode TEXT,
                        customername TEXT,
                        phone TEXT,
                        addressline1 TEXT,
                        addressline2 TEXT,
                        city TEXT,
                        state TEXT,
                        postalcode TEXT,
                        country TEXT,
                        territory TEXT,
                        contactlastname TEXT,
                        contactfirstname TEXT,
                        dealsize TEXT)
                """,
                description="""
                    The sample_sales table is designed for storing detailed sales transaction records.
                    It includes fields for order details (order number, quantity ordered, price per item, line number, total sales), date and status of the order, and temporal identifiers
                    (quarter, month, and year).
                    Product information is detailed through product line, manufacturer's suggested retail price (MSRP), and product code.
                    Customer information is comprehensive, encompassing name, contact details, and address (with provisions for a second address line),
                    along with geographical data like city, state, postal code, country, and sales territory.
                    Additional fields for contact person's name and the size of the deal are also included.
                    This table is suitable for categorizing detailed sales transactions and can support queries for sales analytics, customer segmentation, geographical sales trends,
                    and time-based sales performance.
                """,
            )
            logger.info('Created table "sample_sales".')
        logger.info('Sample table "sample_sales" already exists.')
