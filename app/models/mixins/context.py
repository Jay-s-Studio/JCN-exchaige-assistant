from app.libs.contexts.api_context import get_api_context


def get_current_username():
    try:
        return get_api_context().username
    except:
        return None


def get_current_id():
    try:
        return get_api_context().user_id
    except:
        return None
