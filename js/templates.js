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