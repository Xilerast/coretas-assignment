let _csrfToken = null;
const API_HOST = "http://127.0.0.1:8000";

async function obtainCSRFToken() {
    if (_csrfToken === null) {
        const response = await fetch(`${API_HOST}/api/csrf/`, {
            credentials:"include"
        });
        const data = await response.json();
        _csrfToken = data.csrfToken;
    }

    return _csrfToken;
}

export { _csrfToken, API_HOST, obtainCSRFToken };