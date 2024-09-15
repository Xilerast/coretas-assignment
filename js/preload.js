let _csrfToken = null;
const API_HOST = "http://127.0.0.1:8000";
var originalBtnHtml = null;
window.originalBtnHtml = originalBtnHtml;

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

async function logUserInOnLoad() {
    let request = new Request(
        API_HOST + "/api/tasks/",
        {
            method: "GET",
            credentials: "include"
        }
    );
    let response = await fetch(request);
    if (response.ok) {
        let taskTemplate = await (await fetch("../html/tasks.html")).text();
        $("#main-content").html(taskTemplate);
        replaceButtons();
        let json = await response.json();
        let taskList = document.getElementById("task-list");
        if (json["tasks"].length == 0 || json["tasks"] === undefined) {
            return;
        } else {
            taskList.innerHTML = "";
        }
        json["tasks"].forEach(task => {
            const taskDiv = document.createElement("div");
            taskDiv.className = "task";

            taskDiv.innerHTML = `<h5><a href="#" onclick="displayTask(${task.id});">${task.title}</a></h5>
            <button type="button" class="btn btn-danger" onclick="deleteTask(${task.id});">Delete</button>`;

            taskList.appendChild(taskDiv);
        });
    }
}

async function replaceButtons() {
    let topElem = $("#top");
    originalBtnHtml = topElem.html();
    window.originalBtnHtml = originalBtnHtml;
    topElem.html(await (await fetch("../html/loggedInBtns.html")).text());
}

async function createTask() {
    let title = $("#title-field").val();
    let descr = $("#descr-field").val();

    let request = new Request(API_HOST + "/api/tasks/create", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
            "title": title,
            "description": descr
        })
    });

    let response = await fetch(request);

    if (response.ok) {
        let createSuccessElem = $("#create-success");
        createSuccessElem.html("Success!");
        createSuccessElem.removeAttr("hidden");
    } else if (response.status === 400) {
        let createErrorElem = $("#create-errors");
        createErrorElem.html("Bad request");
        createErrorElem.removeAttr("hidden");
    } else if (response.status === 500) {
        let createErrorElem = $("#create-errors");
        createErrorElem.html("Internal server error");
        createErrorElem.removeAttr("hidden");
    }
}

await logUserInOnLoad();

window.createTask = createTask;

export { _csrfToken, API_HOST, obtainCSRFToken, logUserInOnLoad, createTask };