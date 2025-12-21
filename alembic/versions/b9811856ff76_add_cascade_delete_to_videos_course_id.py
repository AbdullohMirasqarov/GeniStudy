"""add cascade delete to videos.course_id

Revision ID: b9811856ff76
Revises: 7c9e5aacfa32
Create Date: 2025-12-21 10:31:22.508302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9811856ff76'
down_revision: Union[str, Sequence[str], None] = '7c9e5aacfa32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Faqat foreign keyni o'zgartirish
    op.drop_constraint('videos_course_id_fkey', 'videos', type_='foreignkey')
    op.create_foreign_key(
        'videos_course_id_fkey', 'videos', 'courses',
        ['course_id'], ['id'],
        ondelete='CASCADE'
    )



def downgrade():
    op.drop_constraint('videos_course_id_fkey', 'videos', type_='foreignkey')
    op.create_foreign_key(
        'videos_course_id_fkey', 'videos', 'courses',
        ['course_id'], ['id']
    )
