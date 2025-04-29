import faker

fake = faker.Faker()


def create_account_payload() -> dict:
    payload = {
        "name": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }

    return payload


def create_child_payload(parent_id: str, child_saving_plan_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "birth_age": fake.random_int(min=20, max=50),
        "parent_id": parent_id,
        "child_saving_plan_id": child_saving_plan_id,
    }

    return payload


def create_child_saving_plan_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "independent_age": fake.random_int(min=18, max=26),
        "owner_id": owner_id,
    }

    return payload


def child_saving_amount_entries_payload(
    owner_id: str, child_saving_plan_id: str
) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "amount": fake.random_int(min=100000, max=400000),
        "start_age": fake.random_int(min=0, max=15),
        "owner_id": owner_id,
        "child_saving_plan_id": child_saving_plan_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=3)

    return payload


def create_asset_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "amount": fake.random_int(min=10000, max=1000000),
        "description": fake.paragraph(nb_sentences=5),
        "max_yearly_return_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.06, max_value=1.0
        ),
        "min_yearly_return_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-1.0, max_value=0.05
        ),
        "start_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=30)

    return payload


def create_expense_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "amount": fake.random_int(min=1000, max=100000),
        "description": fake.paragraph(nb_sentences=5),
        "max_yearly_growth_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
        ),
        "min_yearly_growth_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        ),
        "start_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=30)

    return payload


def create_house_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "amount": fake.random_int(min=100000, max=50000000),
        "description": fake.paragraph(nb_sentences=5),
        "down_payment": fake.random_int(min=10000, max=500000),
        "interest_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=1.0, max_value=5.0
        ),
        "loan_term": fake.random_int(min=10, max=40),
        "purchase_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["sale_age"] = payload["purchase_age"] + fake.random_int(min=0, max=30)

    return payload


def create_income_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "amount": fake.random_int(min=20000, max=200000),
        "description": fake.paragraph(nb_sentences=5),
        "max_yearly_growth_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
        ),
        "min_yearly_growth_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        ),
        "start_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=30)

    return payload


def create_liability_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "principal_amount": fake.random_int(min=1000, max=1000000),
        "interest_rate": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.2
        ),
        "start_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=40)

    return payload


def create_risk_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "amount": fake.random_int(min=0, max=20000),
        "probability": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0, max_value=0.8
        ),
        "start_age": fake.random_int(min=20, max=65),
        "owner_id": owner_id,
    }
    payload["end_age"] = payload["start_age"] + fake.random_int(min=0, max=30)

    return payload


def create_scenario_payload(owner_id: str) -> dict:
    payload = {
        "name": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=5),
        "asset_allocation_percentage": fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.0, max_value=1.0
        ),
        "retire_age": fake.random_int(min=50, max=80),
        "owner_id": owner_id,
    }

    return payload
