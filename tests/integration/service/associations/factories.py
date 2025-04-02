import faker

faker = faker.Faker()


def create_scenario_child_payload(scenario_id: str, child_id: str) -> dict:
    """Create a scenario child payload"""
    payload = {
        "scenario_id": scenario_id,
        "child_id": child_id,
        "birth_age": faker.random_int(min=20, max=50),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["independent_age"] = payload["birth_age"] + faker.random_int(min=20, max=30)
    return payload


def create_scenario_asset_payload(scenario_id: str, asset_id: str) -> dict:
    """Create a scenario asset payload"""
    payload = {
        "scenario_id": scenario_id,
        "asset_id": asset_id,
        "max_yearly_return_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.06, max_value=1.0
        ),
        "min_yearly_return_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=-1.0, max_value=0.05
        ),
        "allocation_percentage": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.00, max_value=1
        ),
        "start_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["end_age"] = payload["start_age"] + faker.random_int(min=0, max=30)
    return payload


def create_scenario_expense_payload(scenario_id: str, expense_id: str) -> dict:
    """Create a scenario expense payload"""
    payload = {
        "scenario_id": scenario_id,
        "expense_id": expense_id,
        "max_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
        ),
        "min_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        ),
        "start_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["end_age"] = payload["start_age"] + faker.random_int(min=0, max=30)
    return payload


def create_scenario_house_payload(scenario_id: str, house_id: str) -> dict:
    """Create a scenario house payload"""
    payload = {
        "scenario_id": scenario_id,
        "house_id": house_id,
        "down_payment": faker.random_int(min=10000, max=500000),
        "interest_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=1.0, max_value=5.0
        ),
        "loan_term": faker.random_int(min=10, max=40),
        "purchase_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["sale_age"] = payload["purchase_age"] + faker.random_int(min=0, max=30)
    return payload


def create_scenario_income_payload(scenario_id: str, income_id: str) -> dict:
    """Create a scenario income payload"""
    payload = {
        "scenario_id": scenario_id,
        "income_id": income_id,
        "max_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
        ),
        "min_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        ),
        "start_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["end_age"] = payload["start_age"] + faker.random_int(min=0, max=30)
    return payload


def create_scenario_liability_payload(scenario_id: str, liability_id: str) -> dict:
    """Create a scenario liability payload"""
    payload = {
        "scenario_id": scenario_id,
        "liability_id": liability_id,
        "interest_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.2
        ),
        "allocation_percentage": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.00, max_value=1
        ),
        "start_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["end_age"] = payload["start_age"] + faker.random_int(min=0, max=40)
    return payload


def create_scenario_risk_payload(scenario_id: str, risk_id: str) -> dict:
    """Create a scenario risk payload"""
    payload = {
        "scenario_id": scenario_id,
        "risk_id": risk_id,
        "min_loss": faker.random_int(min=5000, max=30000),
        "start_age": faker.random_int(min=20, max=65),
        "memo": faker.paragraph(nb_sentences=5),
    }
    payload["max_loss"] = payload["min_loss"] + faker.random_int(min=0, max=50000)
    payload["end_age"] = payload["start_age"] + faker.random_int(min=0, max=30)
    return payload
