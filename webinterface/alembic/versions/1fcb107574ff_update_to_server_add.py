"""Update to Server (add RPC bitmask) and pushstatus (add version string)


Revision ID: 1fcb107574ff
Revises: 1eba4fe66575
Create Date: 2014-01-31 13:07:54.306328

"""

# revision identifiers, used by Alembic.
revision = '1fcb107574ff'
down_revision = '1eba4fe66575'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Pushstatus', sa.Column('version', sa.String(20), nullable=True))
    op.add_column('Server', sa.Column('rpc', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Server', 'rpc')
    op.drop_column('Pushstatus', 'version')
    ### end Alembic commands ###
