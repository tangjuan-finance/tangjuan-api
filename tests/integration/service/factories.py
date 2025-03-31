import faker

faker = faker.Faker()


def create_expense_payload(owner_id: str) -> dict:
    payload = {
        "name": faker.text(max_nb_chars=20),
        "amount": faker.random_int(min=1000, max=100000),
        "max_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
        ),
        "min_yearly_growth_rate": faker.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        ),
        "start_age": faker.random_int(min=20, max=65),
        "owner_id": owner_id,
    }

    return payload
