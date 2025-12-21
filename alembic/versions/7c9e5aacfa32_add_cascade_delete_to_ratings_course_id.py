"""add cascade delete to ratings.course_id

Revision ID: 7c9e5aacfa32
Revises: 0200d70d8739
Create Date: 2025-12-21 10:25:18.207423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c9e5aacfa32'
down_revision: Union[str, Sequence[str], None] = '0200d70d8739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "ratings_course_id_fkey",
        "ratings",
        type_="foreignkey"
    )
    op.create_foreign_key(
        "ratings_course_id_fkey",
        "ratings",
        "courses",
        ["course_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(
        "ratings_course_id_fkey",
        "ratings",
        type_="foreignkey"
    )
    op.create_foreign_key(
        "ratings_course_id_fkey",
        "ratings",
        "courses",
        ["course_id"],
        ["id"]
    )

