"""make providers.status nullable

Revision ID: fc499248b809
Revises: 92b5bfca23da
Create Date: 2025-10-03 17:05:05.036926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc499248b809'
down_revision: Union[str, Sequence[str], None] = '92b5bfca23da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    op.alter_column('providers', 'status',
                    existing_type=sa.String(),
                    nullable=True)

def downgrade():
    op.alter_column('providers', 'status',
                    existing_type=sa.String(),
                    nullable=False)
