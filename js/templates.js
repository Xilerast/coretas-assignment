async function registerTemplate() {
    let registrationTemplate = await (await fetch("../html/register.html")).text();
    $("#main-content").html(registrationTemplate);
}

async function loginTemplate() {
    let loginTemplate = await (await fetch("../html/login.html")).text();
    $("#main-content").html(loginTemplate);
}

async function createTaskTemplate() {
    let createTemplate = await (await fetch("../html/createTask.html")).text();
    $("#main-content").html(createTemplate);
}

async function editTaskTemplate(task) {
    let editTaskTemplate = await (await fetch("../html/editTask.html")).text();
    $("#main-content").html(editTaskTemplate);
    $("#task-id").val(task.id);
    $("#title-field").val(task.title);
    $("#descr-field").val(task.description);
}