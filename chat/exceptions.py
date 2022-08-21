from ninja.errors import HttpError

already_friends_error = HttpError(status_code=409, message="You are already friends")
