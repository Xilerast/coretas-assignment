import * as preload from "./preload.js";

async function registerUser() {
    let username = $("#username-field").val();
    let email = $("#email-field").val();
    let password = $("#password-field").val();
    let passwordConfirm = $("#password-confirm-field").val();

    let errorElem = $("#registration-errors");
    let successElem = $("#registration-success");

    if (password !== passwordConfirm) {
        errorElem.html("Passwords do not match.");
        errorElem.removeAttr("hidden");
        return;
    }

    let headers = {
        "X-CSRFToken": preload._csrfToken ?? await (preload.obtainCSRFToken()),
        "content-type": "application/json"
    };

    let request = new Request(preload.API_HOST + "/api/register/", {
        method: "POST",
        credentials: "include",
        headers: headers,
        body: JSON.stringify({
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": passwordConfirm
        })
    });

    let response = await fetch(request);
    if (response.ok || response.status === 201) {
        successElem.removeAttr("hidden");
    } else if (response.status === 400) {
        errorElem.html("Bad request. One or more fields were probably empty.");
        errorElem.removeAttr("hidden");
    } else if (response.status === 409) {
        errorElem.html("User already exists.");
        errorElem.removeAttr("hidden");
    } else {
        errorElem.html("Internal server error. Try again.");
        errorElem.removeAttr("hidden");
    }

    return;
}

async function loginUser() {
    let username = $("#username-field").val();
    let password = $("#password-field").val();

    let errorElem = $("#login-errors");

    let request = new Request(preload.API_HOST + "/api/login/", {
        method: "POST",
        headers: {
            "content-type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
            "username": username,
            "password": password
        })
    });

    let response = await fetch(request);

    if (response.ok) {
        return;
    } else {
        errorElem.html("Could not log in with these credentials.");
        errorElem.removeAttr("hidden");
    }
}

window.registerUser = registerUser;
window.loginUser = loginUser;