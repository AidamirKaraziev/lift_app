"""Удалил таблицу старого юзера 

Revision ID: d7f9eb91b03e
Revises: dd975f0d2a3d
Create Date: 2023-03-27 15:01:07.653707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7f9eb91b03e'
down_revision = 'dd975f0d2a3d'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_table('activity_spheres')
    # op.drop_table('activity_spheres_of_project')
    # op.drop_table('area_of_responsibility')
    # op.drop_table('partner_competencies')
    # op.drop_table('partner_competencies_of_project')
    # op.drop_table('projects')
    # op.drop_table('stage_of_implementation')

    # # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('users',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('tel', sa.String(), nullable=True),
    # sa.Column('first_name', sa.String(), nullable=True),
    # sa.Column('last_name', sa.String(), nullable=True),
    # sa.Column('birthday', sa.Date(), nullable=True),
    # sa.Column('location_id', sa.Integer(), nullable=True),
    # sa.Column('photo_main', sa.String(), nullable=True),
    # sa.Column('photo_1', sa.String(), nullable=True),
    # sa.Column('photo_2', sa.String(), nullable=True),
    # sa.Column('basic_about_me', sa.String(), nullable=True),
    # sa.Column('job_title', sa.String(), nullable=True),
    # sa.Column('company', sa.String(), nullable=True),
    # sa.Column('about_me', sa.String(), nullable=True),
    # sa.Column('contact_phone', sa.String(), nullable=True),
    # sa.Column('telegram', sa.String(), nullable=True),
    # sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='SET NULL'),
    # sa.PrimaryKeyConstraint('id'),
    # sa.UniqueConstraint('tel')
    # )
    # op.create_foreign_key(None, 'device', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'device', type_='foreignkey')
    # op.drop_table('users')
    pass
    # ### end Alembic commands ###
