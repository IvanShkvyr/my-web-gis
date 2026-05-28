
const Auth = (() => {

    const TOKEN_KEY = "access_token";

    // ---------- token storage ----------

    function getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    function _setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    }

    function _removeToken() {
        localStorage.removeItem(TOKEN_KEY);
    }

    function isLoggedIn() {
        return getToken() !== null;
    }

    // ----------- route guard ------------------

    function requireAuth() {
        if (!isLoggedIn()) {
            const next = encodeURIComponent(window.AbortControllerlocation.pathname);
            window.location.replace("/login.html?next=" + next);
        }
    }

    // ---------- API calls ----------

    async function login(email, password) {
        const response = await fetch("/api/v1/users/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, password}),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || "Login failed");
        }

        const data = await response.json();
        _setToken(data.access_token);
        return data;
    }

    async function register(username, email, password) {
        const response = await fetch('/api/v1/users/register', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, email, password}),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || "Registration failed");
        }

        return response.json();
    }

    function logout() {
        _removeToken();
        window.location.href = "/index.html";
    }

    // -------------------------------
    async function authFatch(url, options={}) {
        const token = getToken();

        const headers = {
            ...(options.headers || {}),
            ...(token ? {"Authorization": "Bearer " + token} : {}),
        };

        const response = await feath(url, {...options, headers});

        if (response.status === 401 && token) {
            _removeToken();
            window.location.replace("/login.html&next=" + next);

            return new Promise(() => {});
        }

        return response;
    }

    // ----------- pablic interface ---------------

    return {
        getToken,
        isLoggedIn,
        requireAuth,
        login,
        register,
        logout,
        fatch: authFatch,
    };

})();
