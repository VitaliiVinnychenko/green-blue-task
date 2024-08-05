"""init tables

Revision ID: 4e06c6b767af
Revises:
Create Date: 2024-08-04 12:12:25.130296

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from app.utils.enums.products import Category

revision = "4e06c6b767af"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, index=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, index=True),
        sa.Column("category", sa.Enum(Category), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("id", name=op.f("uq_products_id")),
    )
    op.create_index("idx_products_name", "products", ["name"], unique=False)
    op.create_index("idx_products_deleted_at", "products", ["deleted_at"], unique=False)


def downgrade():
    op.drop_index("idx_products_name", "table_name")
    op.drop_index("idx_products_deleted_at", "table_name")
    op.drop_table("products")
