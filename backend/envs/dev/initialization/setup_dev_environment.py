from databases.database_managers import AppDatabaseManager,ClientDatabaseManager
from databases.dashboard_manager import DashboardManager
from databases.sql_executor import SQLExecutor
from databases.organization_manager import OrganizationManager
from databases.user_manager import UserManager
from models.app_models import Organization, User
from models.client_models import Chart, Dashboard
from security import get_password_hash
from utils.utils import get_app_logger

logger = get_app_logger(__name__)

def create_sample_organization():
    """Creates a sample organization if it doesn't already exist."""
    organization = Organization(
        name = 'DocShow AI'
    )

    with AppDatabaseManager() as session:
        org_manager = OrganizationManager(session)
        existing_org = org_manager.get_organization_by_name(organization.name)
        if not existing_org:
            org_manager.create_organization(organization)
            logger.debug("Sample organization created.")
        else:
            logger.debug("Sample organization already exists.")

def create_admin_user():
    """Creates an admin user if it doesn't already exist."""
    admin_user = User(
        username = 'admin',
        hashed_password = get_password_hash('admin'),
        email = 'admin@docshow.ai',
        organization_id = 1,
        role = 'admin'
    )

    with AppDatabaseManager() as session:
        user_manager = UserManager(session)
        existing_user = user_manager.get_user(admin_user.username)
        if not existing_user:
            user_manager.create_user(admin_user)
            logger.debug("Admin user created.")
        else:
            logger.debug("Admin user already exists.")

def create_sample_dashboard():
    dashboard = Dashboard(
        name="Sample Dashboard",
        description="Sample dashboard for development",
        organization="DocShow AI"
    )

    with ClientDatabaseManager() as session:
        manager = DashboardManager(session)
        existing_dashboard = manager.get_dashboard_by_name(dashboard.name, dashboard.organization)
        if not existing_dashboard:

            sql_executor = SQLExecutor(session)
            charts = create_sample_charts(sql_executor)

            dashboard.charts.extend(charts)  # Directly append the list of charts
            manager.create_dashboard(dashboard)
            logger.debug("Sample dashboard with charts created.")
        else:
            logger.debug("Sample dashboard already exists.")

def create_sample_charts(sql_executor: SQLExecutor):
    # Add more chart creation logic here as needed
    return [
        create_sample_bar_chart(sql_executor),
        create_sample_pie_chart(sql_executor),
        create_sample_line_chart(sql_executor)
    ]

def create_sample_bar_chart(sql_executor: SQLExecutor):
    query = """
        SELECT productline, SUM(sales) FROM sample_sales
        GROUP BY productline
    """

    sales_per_product = sql_executor.execute_select_query(query)

    # Transforming the data for the bar chart
    chart_data = [{"productline": row['productline'], "sales": row['sum']} for row in sales_per_product]

    bar_chart_config = {
        "type": "bar",
        "title": "Sales Per Product",
        "nivoConfig": {
            "keys": ["sales"],
            "indexBy": "productline",
            "data": chart_data, 
        }
    }

    bar_chart = Chart(
        order=1,
        config=bar_chart_config
    )

    return bar_chart

def create_sample_pie_chart(sql_executor: SQLExecutor):
    query = """
        SELECT country, ROUND(SUM(sales)::numeric,2) AS total_sales FROM sample_sales
        GROUP BY country
        ORDER BY total_sales DESC
        LIMIT 10
    """

    sales_by_country = sql_executor.execute_select_query(query)

    # Transforming the data for the pie chart
    chart_data = [{"id": row['country'], "value": float(row['total_sales'])} for row in sales_by_country]

    pie_chart_config = {
        "type": "pie",
        "title": "Sales By Country",
        "data": chart_data,
        "options": {
            # Additional options like color schemes, etc.
        }
    }

    return Chart(
        order=2,
        config=pie_chart_config
    )

def create_sample_line_chart(sql_executor: SQLExecutor):
    query = """
        SELECT year_id, SUM(sales) AS yearly_sales FROM sample_sales
        GROUP BY year_id
        ORDER BY year_id
    """

    yearly_sales = sql_executor.execute_select_query(query)

    # Transforming the data for the line chart
    chart_data = [{"x": str(row['year_id']), "y": row['yearly_sales']} for row in yearly_sales]

    line_chart_config = {
        "type": "line",
        "title": "Yearly Sales",
        "data": [
            {
                "id": "yearly_sales",
                "data": chart_data
            }
        ],
        "options": {
            # Additional options like axis settings, etc.
        }
    }

    return Chart(
        order=3,
        config=line_chart_config
    )