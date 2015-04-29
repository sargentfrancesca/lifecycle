"""empty message

Revision ID: 10d829d3a353
Revises: 53a73e499be0
Create Date: 2015-02-10 15:49:19.974433

"""

# revision identifiers, used by Alembic.
revision = '10d829d3a353'
down_revision = '53a73e499be0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('page', 'author_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('page', 'content',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('page', 'content_html',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('page', 'image_url',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('page', 'pagetype',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('page', 'project_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('page', 'publish',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('page', 'title',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
#    op.create_index('ix_page_id', 'page', ['id'], unique=False)
#    op.drop_index('fkplantspecies', 'plant')
#    op.drop_index('id_2', 'species')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('id_2', 'species', [u'id'], unique=False)
    op.create_index('fkplantspecies', 'plant', [u'species_id'], unique=False)
    op.drop_index('ix_page_id', 'page')
    op.alter_column('page', 'title',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('page', 'publish',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.alter_column('page', 'project_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('page', 'pagetype',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('page', 'image_url',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('page', 'content_html',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('page', 'content',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('page', 'author_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    ### end Alembic commands ###