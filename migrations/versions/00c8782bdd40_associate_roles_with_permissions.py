"""Associate roles with permissions

Revision ID: 00c8782bdd40
Revises: ed7b70400769
Create Date: 2025-09-05 20:49:51.184744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c8782bdd40'
down_revision: Union[str, Sequence[str], None] = 'ed7b70400769'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the role-permission associations."""
    role_permission_table = sa.table('role_permission_association',
        sa.column('role_id', sa.Integer),
        sa.column('permission_id', sa.Integer)
    )

    op.bulk_insert(role_permission_table,
        [
            # PLATFORM_ADMIN gets all permissions
            {'role_id': 1, 'permission_id': 1}, # system:admin
            {'role_id': 1, 'permission_id': 2}, # schools:manage
            {'role_id': 1, 'permission_id': 3}, # users:manage
            {'role_id': 1, 'permission_id': 4}, # roles:manage

            # SCHOOL_ADMIN gets user and role management permissions
            {'role_id': 2, 'permission_id': 3}, # users:manage
            {'role_id': 2, 'permission_id': 4}, # roles:manage
        ]
    )


def downgrade() -> None:
    """Remove the seeded role-permission associations."""
    op.execute(
        "DELETE FROM role_permission_association WHERE role_id IN (1, 2)"
    )
