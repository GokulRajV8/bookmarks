class BookmarksSection {
    // UI elements
    mainDiv = document.createElement('div');

    constructor(title, linksList) {
        const sectionTitle = document.createElement('h2');
        sectionTitle.textContent = title;
        this.mainDiv.appendChild(sectionTitle);
        const sectionContent = document.createElement('ul');
        this.mainDiv.appendChild(sectionContent);

        for (const link of linksList) {
            const linkElem = document.createElement('a');
            linkElem.textContent = link.title;
            linkElem.href = link.url;
            linkElem.target = "_blank";
            const linkListItem = document.createElement('li');
            linkListItem.appendChild(linkElem);
            sectionContent.appendChild(linkListItem);
        }
    }
}

function doWithData(fun) {
    fetch('data/items.json')
        .then((data) => data.json())
        .then((res) => {
            fun(res);
        });
}

function hydratePage(itemsList) {
    document.querySelector('main').innerHTML = '';
    for (const item of itemsList) {
        const bookmarksSection = new BookmarksSection(item.title, item.links);
        document.querySelector('main').appendChild(bookmarksSection.mainDiv);
    }
}

doWithData(hydratePage);
