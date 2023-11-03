import httpx
import streamlit as st


def handle_expired_session():
    """
    Handle the scenario where a user's session has expired.
    This function clears session-related data and prompts the user to re-login.
    """
    st.warning("Your session has expired. Please log in again.")
    
    # Clear session state related to authentication
    if 'access_token' in st.session_state:
        del st.session_state['access_token']
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
    
    # Redirect to login page (assuming you have a login function/page)
    st.experimental_rerun()  # This will rerun your Streamlit app from the top


def send_api_request(url: str, method: str, request_kwargs: dict) -> httpx.Response:
    """
    Send a request to the specified API endpoint.

    Args:
    - url (str): The endpoint URL.
    - method (str): The HTTP method ("GET", "PUT", "POST", "DELETE").
    - request_kwargs (dict): Additional arguments for the request.

    Returns:
    - httpx.Response: The response from the API.
    """
    with httpx.Client() as client:
        if method == "GET":
            response = client.get(url, **request_kwargs)
        elif method in ["PUT", "POST", "DELETE"]:
            response_func = getattr(client, method.lower())
            response = response_func(url, **request_kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response


def api_request(
        url: str, 
        method: str = "GET", 
        data: dict = None, 
        json: dict = None, 
        files: dict = None,
        params: dict = None, 
        timeout: float = None,
        headers: dict = None) -> dict:
    """
    Send an API request and handle potential errors and session expirations.

    Args:
    - url, method, data, json, files, params, timeout, headers: Parameters for the API request.

    Returns:
    - dict: The JSON response from the API.
    """
    request_kwargs = {
        "params": params,
        "headers": headers,
        "data": data,
        "json": json,
        "files": files,
        "timeout": timeout
    }
    # Remove keys where values are None
    request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}

    try:
        response = send_api_request(url, method, request_kwargs)

        # if response.status_code == 401:  # Unauthorized
        #     handle_expired_session()

        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response

    except httpx.RequestError as exc:
        st.exception(f"An error occurred while requesting {exc.request.url!r}.")
    except Exception as e:
        st.exception(f"An error occurred: {e}")

    return None

# Set up the headers with the token
if "access_token" in st.session_state:
    HEADERS = {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }
else:
    HEADERS = {}