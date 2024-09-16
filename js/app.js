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
    let mainContent = $("#main-content");

    let request = new Request(preload.API_HOST + "/api/login/", {
        method: "POST",
        headers: {
            "X-CSRFToken": preload._csrfToken ?? await (preload.obtainCSRFToken()),
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
        let taskTemplate = await (await fetch("../html/tasks.html")).text();
        mainContent.html(taskTemplate);
        await replaceButtons();
        await preload.logUserInOnLoad();
    } else {
        errorElem.html("Could not log in with these credentials.");
        errorElem.removeAttr("hidden");
    }
}

async function logout() {
    $("#top").html(originalBtnHtml);
    $("#main-content").html('');
    return await fetch(preload.API_HOST + "/api/logout/");
}

async function replaceButtons() {
    let topElem = $("#top");
    originalBtnHtml = topElem.html();
    window.originalBtnHtml = originalBtnHtml;
    topElem.html(await (await fetch("../html/loggedInBtns.html")).text());
}

async function deleteTask(id) {
    let request = new Request(
        preload.API_HOST + "/api/tasks/delete/" + String(id) + '/', {
            method: "DELETE",
            credentials: "include"
        }
    );

    let response = await fetch(request);

    if (response.ok) {
        preload.logUserInOnLoad();
    } else {
        alert("Something went wrong");
    }
}

async function displayTask(task) {
    let request = new Request(
        preload.API_HOST + "/api/tasks/" + String(task.id) + '/', {
            method: "GET",
            credentials: "include"
        }
    );

    let response = await fetch(request);

    if (response.ok) {
        let json = await response.json();
        let taskTemplate = await (await fetch("../html/task.html")).text();
        $("#main-content").html(taskTemplate);
        $("#task-title").html(`<h2>${json["title"]}</h2>`);
        $("#task-description").html(`<p>${json["description"]}</p>`);
        $("#task-completed").html(`<p>Completed: ${json["completion_status"]}</p>`);
        $("#delete-btn").html(`<button type="button" class="btn btn-danger" onclick="deleteTask(${String(task.id)});">Delete</button>`);
        $("#edit-btn").html(`<button type="button" class="btn btn-secondary" onclick='editTaskTemplate(${JSON.stringify(task)});'>Edit</button>`);
        $("#complete-btn").html(`<button type="button" class="btn btn-success" onclick="completeTask(${String(task.id)});">Complete</button>`);
    }
}

async function completeTask(id) {
    let request = new Request(preload.API_HOST + "/api/tasks/complete/" + id + "/", {
        method: "PATCH",
        credentials: "include"
    });
    
    let response = await fetch(request);
    if (response.ok) {
        displayTask(id);
    }
}

async function editTask() {
    let title = $("#title-field").val();
    let descr = $("#descr-field").val();
    let id = $("#task-id").val();

    let request = new Request(preload.API_HOST + "/api/tasks/edit/" + id + '/', {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({
            "title": title,
            "description": descr
        })
    });

    let response = await fetch(request);

    if (response.ok) {
        let editSuccessElem = $("#edit-success");
        editSuccessElem.html("Success!");
        editSuccessElem.removeAttr("hidden");
    } else if (response.status === 400) {
        let editErrorElem = $("#edit-errors");
        editErrorElem.html("Bad request");
        editErrorElem.removeAttr("hidden");
    } else if (response.status === 500) {
        let editErrorElem = $("#edit-errors");
        editErrorElem.html("Internal server error");
        editErrorElem.removeAttr("hidden");
    }
}

window.registerUser = registerUser;
window.loginUser = loginUser;
window.logout = logout;
window.replaceButtons = replaceButtons;
window.deleteTask = deleteTask;
window.displayTask = displayTask;
window.completeTask = completeTask;
window.editTask = editTask;