"""Add initial permissions and roles

Revision ID: ed7b70400769
Revises: bd05af4f4227
Create Date: 2025-09-05 20:39:23.235118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ed7b70400769'
down_revision: Union[str, Sequence[str], None] = 'bd05af4f4227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed initial roles and permissions."""
    # Define table structure for bulk insert
    roles_table = sa.table('roles',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('school_id', sa.Integer)
    )
    permissions_table = sa.table('permissions',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )

    # Seed Permissions
    op.bulk_insert(permissions_table,
        [
            {'id': 1, 'name': 'system:admin'},
            {'id': 2, 'name': 'schools:manage'},
            {'id': 3, 'name': 'users:manage'},
            {'id': 4, 'name': 'roles:manage'},
        ]
    )

    # Seed Roles (platform-level roles have no school_id)
    op.bulk_insert(roles_table,
        [
            {'id': 1, 'name': 'PLATFORM_ADMIN', 'school_id': None},
            {'id': 2, 'name': 'SCHOOL_ADMIN', 'school_id': None}, # Template role
            {'id': 3, 'name': 'TEACHER', 'school_id': None},      # Template role
            {'id': 4, 'name': 'STUDENT', 'school_id': None},      # Template role
            {'id': 5, 'name': 'PARENT', 'school_id': None},       # Template role
        ]
    )

def downgrade() -> None:
    """Remove initial roles and permissions."""
    # Delete the specific seeded data.
    # Using "in" clause for safety, to only delete what we added.
    op.execute("DELETE FROM roles WHERE id IN (1, 2, 3, 4, 5)")
    op.execute("DELETE FROM permissions WHERE id IN (1, 2, 3, 4)")
