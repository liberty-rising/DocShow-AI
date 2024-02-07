"""replace table_id with table_name in data profile model

Revision ID: f8ca6f4bf570
Revises: 94af7f09e896
Create Date: 2024-01-29 20:26:47.028083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8ca6f4bf570"
down_revision = "94af7f09e896"
branch_labels = None
depends_on = None


def upgrade():
    # Rename the column and change its type
    op.alter_column(
        "data_profiles",
        "table_id",
        new_column_name="table_name",
        type_=sa.String(),
        existing_nullable=True,
    )


def downgrade():
    # Reverse the changes made in the upgrade function
    op.alter_column(
        "data_profiles",
        "table_name",
        new_column_name="table_id",
        type_=sa.Integer(),
        existing_nullable=True,
    )
