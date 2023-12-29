from database.data_profile_manager import DataProfileManager
from database.database_manager import DatabaseManager
from database.dashboard_manager import DashboardManager
from database.table_manager import TableManager
from database.organization_manager import OrganizationManager
from database.user_manager import UserManager
from models.organization import Organization
from models.user import User
from models.chart import Chart
from models.dashboard import Dashboard
from models.data_profile import DataProfile
from security import get_password_hash
from utils.utils import get_app_logger

logger = get_app_logger(__name__)


def create_sample_organization():
    """Creates a sample organization if it doesn't already exist."""
    organization = Organization(name="DocShow AI")

    with DatabaseManager() as session:
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
        username="admin",
        hashed_password=get_password_hash("admin"),
        email="admin@docshow.ai",
        organization_id=1,
        role="admin",
    )

    with DatabaseManager() as session:
        user_manager = UserManager(session)
        existing_user = user_manager.get_user_by_username(admin_user.username)
        if not existing_user:
            user_manager.create_user(admin_user)
            logger.debug("Admin user created.")
        else:
            logger.debug("Admin user already exists.")


def create_sample_dashboard():
    dashboard = Dashboard(
        name="Sample Dashboard",
        description="Sample dashboard for development",
        organization="DocShow AI",
    )

    with DatabaseManager() as session:
        manager = DashboardManager(session)
        existing_dashboard = manager.get_dashboard_by_name(
            dashboard.name, dashboard.organization
        )
        if not existing_dashboard:
            table_manager = TableManager(session)
            charts = create_sample_charts(table_manager)

            dashboard.charts.extend(charts)  # Directly append the list of charts
            manager.save_dashboard(dashboard)
            logger.debug("Sample dashboard with charts created.")
        else:
            logger.debug("Sample dashboard already exists.")


def create_sample_charts(table_manager: TableManager):
    # Add more chart creation logic here as needed
    return [
        create_sample_bar_chart(table_manager),
        create_sample_pie_chart(table_manager),
        create_sample_line_chart(table_manager),
    ]


def create_sample_bar_chart(table_manager: TableManager):
    query = """
        SELECT productline, SUM(sales) FROM sample_sales
        GROUP BY productline
    """

    sales_per_product = table_manager.execute_select_query(query)

    # Transforming the data for the bar chart
    chart_data = [
        {"productline": row["productline"], "sales": row["sum"]}
        for row in sales_per_product
    ]

    bar_chart_config = {
        "type": "bar",
        "title": "Sales Per Product",
        "nivoConfig": {
            "keys": ["sales"],
            "indexBy": "productline",
            "data": chart_data,
        },
    }

    bar_chart = Chart(order=1, config=bar_chart_config)

    return bar_chart


def create_sample_pie_chart(table_manager: TableManager):
    query = """
        SELECT country, ROUND(SUM(sales)::numeric,2) AS total_sales FROM sample_sales
        GROUP BY country
        ORDER BY total_sales DESC
        LIMIT 10
    """

    sales_by_country = table_manager.execute_select_query(query)

    # Transforming the data for the pie chart
    chart_data = [
        {"id": row["country"], "value": float(row["total_sales"])}
        for row in sales_by_country
    ]

    pie_chart_config = {
        "type": "pie",
        "title": "Sales By Country",
        "data": chart_data,
        "options": {
            # Additional options like color schemes, etc.
        },
    }

    return Chart(order=2, config=pie_chart_config)


def create_sample_line_chart(table_manager: TableManager):
    query = """
        SELECT year_id, SUM(sales) AS yearly_sales FROM sample_sales
        GROUP BY year_id
        ORDER BY year_id
    """

    yearly_sales = table_manager.execute_select_query(query)

    # Transforming the data for the line chart
    chart_data = [
        {"x": str(row["year_id"]), "y": row["yearly_sales"]} for row in yearly_sales
    ]

    line_chart_config = {
        "type": "line",
        "title": "Yearly Sales",
        "data": [{"id": "yearly_sales", "data": chart_data}],
        "options": {
            # Additional options like axis settings, etc.
        },
    }

    return Chart(order=3, config=line_chart_config)


def create_sample_dataprofile():
    """Creates a sample data profile if it doesn't already exist."""
    # Create a sample DataProfile instance
    sample_profile = DataProfile(
        id=1,  # You can set a specific ID or let it be auto-generated if configured
        name="Sample Profile",
        file_type="pdf",
        organization_id=1,
        description="Sample Description",
    )
    # Using DatabaseManager to manage the database session
    with DatabaseManager() as session:
        profile_manager = DataProfileManager(session)
        existing_profile = profile_manager.get_dataprofile_by_name(sample_profile.name)
        if not existing_profile:
            profile_manager.create_dataprofile(sample_profile)
            logger.debug("Sample data profile created.")
        else:
            logger.debug("Sample data profile already exists.")
