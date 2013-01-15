"""create from scratch

Revision ID: 13037206f335
Revises: None
Create Date: 2013-01-15 13:57:36.273031

"""

# revision identifiers, used by Alembic.
revision = '13037206f335'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Deployment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('startDate', sa.DateTime(), nullable=True),
    sa.Column('endDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('NodeType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('seq', sa.Integer(), nullable=True),
    sa.Column('updated_seq', sa.Integer(), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('blink', sa.Boolean(), nullable=True),
    sa.Column('configured', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Weather',
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('outTemp', sa.Float(), nullable=True),
    sa.Column('outHum', sa.Float(), nullable=True),
    sa.Column('dew', sa.Float(), nullable=True),
    sa.Column('gust', sa.Float(), nullable=True),
    sa.Column('wSpeed', sa.Float(), nullable=True),
    sa.Column('wDir', sa.Float(), nullable=True),
    sa.Column('wChill', sa.Float(), nullable=True),
    sa.Column('apparentTemp', sa.Float(), nullable=True),
    sa.Column('rain', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Float(), nullable=True),
    sa.Column('tempIn', sa.Float(), nullable=True),
    sa.Column('humIn', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('time')
    )
    op.create_table('RoomType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SensorType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=50), nullable=True),
    sa.Column('units', sa.String(length=20), nullable=True),
    sa.Column('c0', sa.Float(), nullable=True),
    sa.Column('c1', sa.Float(), nullable=True),
    sa.Column('c2', sa.Float(), nullable=True),
    sa.Column('c3', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomTypeId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['roomTypeId'], ['RoomType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('House',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deploymentId', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('startDate', sa.DateTime(), nullable=True),
    sa.Column('endDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['deploymentId'], ['Deployment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('DeploymentMetadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deploymentId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('units', sa.String(length=255), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['deploymentId'], ['Deployment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('HouseMetadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('houseId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('units', sa.String(length=20), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['houseId'], ['House.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Occupier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('houseId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('contactNumber', sa.String(length=20), nullable=True),
    sa.Column('startDate', sa.DateTime(), nullable=True),
    sa.Column('endDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['houseId'], ['House.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.Column('houseId', sa.Integer(), nullable=True),
    sa.Column('nodeTypeId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nodeTypeId'], ['NodeType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('nodeId', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensorTypeId', sa.Integer(), nullable=True),
    sa.Column('nodeId', sa.Integer(), nullable=True),
    sa.Column('calibrationSlope', sa.Float(), nullable=True),
    sa.Column('calibrationOffset', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['nodeId'], ['Node.id'], ),
    sa.ForeignKeyConstraint(['sensorTypeId'], ['SensorType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('NodeHistory',
    sa.Column('nodeId', sa.Integer(), nullable=False),
    sa.Column('startDate', sa.DateTime(), nullable=False),
    sa.Column('endDate', sa.DateTime(), nullable=True),
    sa.Column('houseAddress', sa.String(length=255), nullable=True),
    sa.Column('roomType', sa.String(length=255), nullable=True),
    sa.Column('roomName', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['nodeId'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('nodeId', 'startDate')
    )
    op.create_table('NodeState',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('nodeId', sa.Integer(), nullable=True),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.Column('localtime', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['nodeId'], ['Node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('NodeState')
    op.drop_table('NodeHistory')
    op.drop_table('Sensor')
    op.drop_table('Reading')
    op.drop_table('Node')
    op.drop_table('Occupier')
    op.drop_table('HouseMetadata')
    op.drop_table('DeploymentMetadata')
    op.drop_table('House')
    op.drop_table('Room')
    op.drop_table('SensorType')
    op.drop_table('RoomType')
    op.drop_table('Weather')
    op.drop_table('NodeType')
    op.drop_table('Deployment')
    ### end Alembic commands ###
