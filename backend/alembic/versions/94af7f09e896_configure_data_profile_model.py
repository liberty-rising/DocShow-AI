"""configure data profile model

Revision ID: 94af7f09e896
Revises: a7364adb18ea
Create Date: 2024-01-20 22:03:53.600966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "94af7f09e896"
down_revision = "a7364adb18ea"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "data_profiles", "description", new_column_name="extract_instructions"
    )
    op.add_column("data_profiles", sa.Column("table_id", sa.Integer))


def downgrade():
    op.alter_column(
        "data_profiles", "extract_instructions", new_column_name="description"
    )
    op.drop_column("data_profiles", "table_id")
