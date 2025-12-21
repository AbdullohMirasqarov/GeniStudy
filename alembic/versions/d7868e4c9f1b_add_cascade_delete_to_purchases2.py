"""add cascade delete to purchases2

Revision ID: d7868e4c9f1b
Revises: ca9e0e68ad5d
Create Date: 2025-12-21 10:42:14.753878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd7868e4c9f1b'
down_revision: Union[str, Sequence[str], None] = 'ca9e0e68ad5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # purchases.course_id FKni o'chirib, qayta yaratamiz
    op.drop_constraint('purchases_course_id_fkey', 'purchases', type_='foreignkey')
    op.create_foreign_key(
        'purchases_course_id_fkey', 
        'purchases', 
        'courses',
        ['course_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # agar kerak bo'lsa oldingi holatga qaytarish
    op.drop_constraint('purchases_course_id_fkey', 'purchases', type_='foreignkey')
    op.create_foreign_key(
        'purchases_course_id_fkey', 
        'purchases', 
        'courses',
        ['course_id'], ['id']
    )