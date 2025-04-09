from nanoid import generate


def create_fake_id(size: int = 13) -> str:
    return generate(size=size)
