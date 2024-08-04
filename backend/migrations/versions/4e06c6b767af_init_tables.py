"""init tables

Revision ID: 4e06c6b767af
Revises:
Create Date: 2024-08-04 12:12:25.130296

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4e06c6b767af"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product_categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_categories")),
        sa.UniqueConstraint("id", name=op.f("uq_product_categories_id")),
        sa.UniqueConstraint("name", name=op.f("uq_product_categories_name")),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, index=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, index=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"], ["product_categories.id"], name=op.f("fk_products_categories_id_category")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("id", name=op.f("uq_products_id")),
    )
    op.create_index("idx_products_name", "products", ["name"], unique=False)
    op.create_index("idx_products_deleted_at", "products", ["deleted_at"], unique=False)


def downgrade():
    op.drop_index("idx_products_name", "table_name")
    op.drop_index("idx_products_deleted_at", "table_name")
    op.drop_table("products")
    op.drop_table("product_categories")
