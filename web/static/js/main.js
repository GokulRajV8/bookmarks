/* UI functions */

function getEditButton(siteId) {
    const button = document.createElement('button');
    button.textContent = 'Edit';
    button.addEventListener('click', () => {
        location = '/bookmarks/edit/?id=' + siteId;
    });

    return button;
}

function getDeleteButton(siteId, siteTitle) {
    const button = document.createElement('button');
    button.textContent = 'Delete';
    button.addEventListener('click', () => {
        response = confirm('Are you sure you want to delete link : ' + siteTitle);
        if (response) {
            fetch('/bookmarks/api/site?id=' + siteId, { method: 'DELETE' });
            location.reload();
        }
    });

    return button;
}

function activateSubmitButton(form) {
    const button = document.querySelector('#submit-button');
    if (form.url.value == '' || form.name.value == '' || form.tags.value == '') {
        button.disabled = true;
    } else {
        button.disabled = false;
    }
}

/* API contacting functions */

async function getTags() {
    const mainArea = document.querySelector('main');
    try {
        const response = await fetch('/bookmarks/api/tags');
        const tags = await response.json();

        const list = document.createElement('ul');
        mainArea.appendChild(list);
        for (const tag of tags) {
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            link.href = '/bookmarks/sites/?tags=' + tag;
            link.textContent = tag;

            listItem.appendChild(link);
            list.appendChild(listItem);
        }
    } catch {
        mainArea.textContent = 'Unable to fetch data from API';
    }
}

async function getTitleFromURL() {
    const titleInput = document.querySelector('#sname');
    const button = document.querySelector('#get-title-button');

    button.disabled = true;
    try {
        const siteData = await fetch('/bookmarks/api/sitetitle', { method: 'POST', body: document.querySelector('#surl').value });
        const textData = await siteData.text();
        titleInput.value = textData;
    } catch {
        titleInput.value = 'Unable to fetch URL title';
    }
    button.disabled = false;
}

async function formSubmitCreate(event) {
    const messageArea = document.querySelector('#message');
    const message = document.createElement('p');

    try {
        const response = await fetch('/bookmarks/api/site', { method: 'POST', body: new FormData(event.target) });
        if (response.ok)
            message.textContent = 'Data added successfully!';
        else
            message.textContent = 'Data cannot be added!';
    } catch {
        message.textContent = 'Unable to process request!';
    } finally {
        messageArea.innerHTML = '';
        messageArea.appendChild(message);
        event.target.reset();
    }
}

async function getSitesForTags(tags) {
    document.querySelector('#stags').value = tags;
    if (tags == null) return;
    const responseFromServer = await fetch('/bookmarks/api/site?tags=' + encodeURI(tags).replace(/%20/g, '+'));
    const sites = await responseFromServer.json();

    const mainArea = document.querySelector('main');
    const dataSection = document.createElement('ul');
    mainArea.appendChild(dataSection);

    for (const site of sites) {
        const listItem = document.createElement('li');

        const link = document.createElement('a');
        link.href = site.url;
        link.textContent = site.title;
        link.target = '_blank';
        const editButton = getEditButton(site.id);
        const deleteButton = getDeleteButton(site.id, site.title);

        listItem.appendChild(link);
        listItem.appendChild(editButton);
        listItem.appendChild(deleteButton);
        dataSection.appendChild(listItem);
    }
}

async function populateEditForm(form, siteId) {
    const response = await fetch('/bookmarks/api/site?id=' + siteId);
    const siteData = await response.json();

    form.name.value = siteData.title;
    form.url.value = siteData.url;
    form.tags.value = siteData.tags;

    activateSubmitButton(form);
}

async function formSubmitEdit(form, siteId) {
    const messageArea = document.querySelector('#message');
    const message = document.createElement('p');

    try {
        const response = await fetch('/bookmarks/api/site?id=' + siteId, { method: 'PUT', body: new FormData(form) });
        if (response.ok)
            message.textContent = 'Data updated successfully!';
        else
            message.textContent = 'Data cannot be updated!';
    } catch {
        message.textContent = 'Unable to process request!';
    } finally {
        messageArea.innerHTML = '';
        messageArea.appendChild(message);
    }
}

/* Init page functions */

function initTagsPage() {
    getTags();
}

function initCreatePage() {
    const form = document.querySelector('form');

    document.querySelector('#get-title-button').addEventListener('click', getTitleFromURL);
    form.addEventListener('submit', (event) => {
        formSubmitCreate(event);
        event.preventDefault();
    });
    form.addEventListener('change', () => {
        activateSubmitButton(form);
    });
}

function initSitesPage() {
    const urlParams = new URLSearchParams(location.search);
    getSitesForTags(urlParams.get('tags'));
}

function initEditPage() {
    const urlParams = new URLSearchParams(location.search);
    const id = urlParams.get('id');
    const form = document.querySelector('form');
    populateEditForm(form, id);

    form.addEventListener('submit', (event) => {
        formSubmitEdit(form, id);
        event.preventDefault();
    });
    form.addEventListener('change', () => {
        activateSubmitButton(form);
    });
}
