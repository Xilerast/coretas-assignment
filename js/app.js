async function registerTemplate() {
    let registration_template = await (await fetch("../html/register.html")).text();
    $("#main-content").html(registration_template);
}

async function loginTemplate() {
    let login_template = await (await fetch("../html/login.html")).text();
    $("#main-content").html(login_template);
}