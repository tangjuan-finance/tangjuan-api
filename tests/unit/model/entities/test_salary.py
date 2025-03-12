# from app import db
# from app.models import Salary
# import sqlalchemy as sa
# from .factories import create_entity


# class TestSalaryModelCase:
#     def test_create_salary(self, default_user):
#         # Arrange
#         amount = 50000
#         start_year = 30
#         name = "Good Job"
#         salary = create_entity(
#             Salary, owner=default_user, start_year=start_year, name=name, amount=amount
#         )
#         # Act
#         salary_from_db = db.session.scalar(
#             sa.select(Salary).where(Salary.amount == salary.amount)
#         )

#         # Assert
#         assert salary_from_db.amount == salary.amount
#         assert salary_from_db.owner_id == salary.owner_id
