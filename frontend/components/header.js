
// ----- CONFIGURATION -----
const NAV_LINKS = [
    {href: "/index.html",   label: "Main",      auth: "any"},
    {href: "/map.html",     label: "Map",       auth: "any"},
    {href: "/contacts.html",label: "Contacts",  auth: "any"},
    {href: "/track.html",   label: "Track",     auth: "user"},
    {href: "/data.html",    label: "My Data",   auth: "user"},
];

// ----- HELPERS ------

function isLoggedIn() {
    return localStorage.getItem("access_token") !== null;
}

function getActivePath() {
    const path = window.location.pathname;
    return path === "/"?"/index.html": path;
}


// ---------- HTML GENERATORS -------------


function renderNavItem(link, activePath) {
    const activeClass = link.href === activePath ? " active" : "";

    return `
            <li class="navigation-element">
              <div class="item-box">
                <a href="${link.href}" class="item${activeClass}">${link.label}</a>
                <div class="navigation-item-line"></div>
              </div>
            </li>`;
}




function renderAuthSection() {
    if (isLoggedIn()) {
        return `
            <div class="auth-group">
              <div class="item-box logout-box">
                <button class="item logout-btn" id="logout-btn" type="button">Log out</button>
                <div class="auth-item-line"></div>
              </div>
            </div>`;
    }
 
    return `
        <div class="auth-group">
          <ul class="log-in">
            <li class="log-in-element">
              <div class="item-box">
                <a href="/register.html" class="item">Sign up</a>
                <div class="auth-item-line"></div>
              </div>
            </li>
            <li class="log-in-element">
              <div class="item-box">
                <a href="/login.html" class="item">Log in</a>
                <div class="auth-item-line"></div>
              </div>
            </li>
          </ul>
        </div>`;
}


function renderHeader(activePath, userIsLoggedIn) {

    const visibleLinks = NAV_LINKS.filter(link => 
        link.auth === "any" || (link.auth === "user" && userIsLoggedIn)
    );

    const navItemsHTML = visibleLinks
            .map(link => renderNavItem(link, activePath))
            .join("");

    return `
        <div class="container main-display">
          <nav class="main-contact">
            <a href="/index.html" class="logo">
              <span class="first-part">My</span>Web
            </a>
            <ul class="navigation">
              ${navItemsHTML}
            </ul>
          </nav>
          ${renderAuthSection()}
        </div>`;
}


// ------------- DOM INJECTION ---------------

function mountHeader() {

    const hearedEl = document.getElementById("site-header");

    if (!hearedEl) {
        console.error(
            "[header.js] Element <header id=\"site-header\"> not found. " +
            "Make sure it is present in the HTML."
        );
        return;
    }

    hearedEl.innerHTML = renderHeader(getActivePath(), isLoggedIn());

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            if (typeof Auth !== "undefined") {
                Auth.logout();
            } else {
                localStorage.removeItem("access_token");
                window.location.href = "/index.html";
            }
        });
    }

}

mountHeader();
