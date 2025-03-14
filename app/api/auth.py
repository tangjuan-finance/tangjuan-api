from app.api import bp
from app.api.errors.bad_request import (
    EmailNotFoundError,
    PasswordNotFoundError,
    AccountNotFoundError,
    PasswordInvalidError,
    UserNameNotFoundError,
)
from app.api.errors.unauthorized import InvalidRegistrationTokenError
from cryptography.fernet import InvalidToken
from flask import request, jsonify, url_for
from app import db
from app.models import Account
import sqlalchemy as sa

from app.api.utils.encryption import encrypt_data
from app.api.utils.validation import (
    validate_username,
    validate_email,
    validate_token,
    validate_email_format,
)
from app.api.services.redis_service import save_session_token
from app.api.services.email_service import send_email


# from app.api.services.email_service import send_email
# from app.api.services.redis_service import save_session_token, get_session_token


@bp.route("/login", methods=["POST"])
def login():
    """Step 1: Receive user info and send registration link."""
    email = request.json.get("email")

    if not email:
        # Raise a BadRequest with a custom error message
        raise EmailNotFoundError(errors={"email": "Email is required"})

    validate_email_format(email)

    password = request.json.get("password")

    if not password:
        # Raise a BadRequest with a custom error message
        raise PasswordNotFoundError(errors={"password": "Password is required"})

    account = db.session.scalar(sa.select(Account).where(Account.email == email))
    if account is None:
        raise AccountNotFoundError(errors={"account": "Account is not founded"})

    if not account.check_password(password):
        raise PasswordInvalidError(errors={"password": "Password is incorrect"})
        #     flash("使用者名稱或密碼錯誤")
        #     return redirect(url_for("auth.login"))
        # login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get("next")

    # Generate session token and save to Redis
    session_token = encrypt_data({"accountid": account.id}, mode="authentication")
    session_id = save_session_token(session_token)

    # Return session ID to frontend
    return jsonify(
        {
            "message": "Login successful",
            "payload": {"session_id": session_id},
        }
    ), 200


# @bp.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("main.index"))


@bp.route("/register", methods=["POST"])
def create_registration():
    """Step 1: Receive email and send registration link."""
    email = request.json.get("email")
    if not email:
        # Raise a BadRequest with a custom error message
        raise EmailNotFoundError(errors={"email": "Email is required"})

    # Validate the email
    validate_email_format(email)
    validate_email(email)

    # Encrypt a registration token
    token = encrypt_data({"email": email}, mode="registration")
    register_url = url_for("api_v1.complete_registration", token=token, _external=True)

    # Only for dev, should delete later
    print("register_url: " + register_url)
    # Send email
    send_email(
        email, "Complete Your Registration.", f"Click here to register: {register_url}"
    )

    return jsonify({"message": "Registration email sent"}), 200


@bp.route("/register/<token>", methods=["POST"])
def complete_registration(token):
    """Step 2: Register the account with username and password."""
    # Validate the token
    try:
        data = validate_token(token, mode="registration")
    except InvalidToken:
        raise InvalidRegistrationTokenError(
            errors={"token": "Invalid or expired registration token"}
        )

    username = request.json.get("username")
    password = request.json.get("password")
    # Check if both username and password provided
    if not username:
        raise UserNameNotFoundError(errors={"username": "Username is required"})
    elif not password:
        raise PasswordNotFoundError(errors={"password": "Password is required"})

    # Validate the username
    validate_username(username)

    # Create user
    new_account = Account(email=data["email"], username=username)
    new_account.set_password(password)

    # Save user to database
    db.session.add(new_account)
    db.session.commit()
    verified_account = db.session.scalar(
        sa.select(Account).where(Account.username == new_account.username)
    )
    # Generate session token and save to Redis
    session_token = encrypt_data(
        {"accountid": verified_account.id}, mode="authentication"
    )
    session_id = save_session_token(session_token)

    # Return session ID to frontend
    return jsonify(
        {
            "message": "Registration successful",
            "payload": {"session_id": session_id},
        }
    ), 200
