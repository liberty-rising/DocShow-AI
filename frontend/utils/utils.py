import httpx
import streamlit as st

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
    Send an API request.

    Returns:
    - dict: The JSON response from the API.
    """

    try:
        with httpx.Client() as client:
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

            if method == "GET":
                response = client.get(url, **request_kwargs)
            elif method == "PUT":
                response = client.put(url, **request_kwargs)
            elif method == "POST":
                response = client.post(url, **request_kwargs)
            elif method == "DELETE":
                response = client.delete(url, **request_kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")

            # response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            # st.write('helllo', response)
            return response

    except httpx.RequestError as exc:
        st.exception(f"An error occurred while requesting {exc.request.url!r}.")
    except Exception as e:
        st.exception(f"An error occurred: {e}")

    return None

# Set up the headers with the token
headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}