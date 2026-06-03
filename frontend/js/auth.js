
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
        const token = getToken();
        return token !== null && !_isTokenExpired(token);
    }

    function getRole() {
        const token = getToken();
        if (!token) return null;
        const payload = _decodeJwtPayload(token);
        return payload?.role ?? null;
    }


    // ---------- JWT helpers ----------
    function _decodeJwtPayload(token) {
        try {
            const base64Url = token.split(".")[1];
            if (!base64Url) return null;
            const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
            const json = decodeURIComponent(
                atob(base64)
                    .split("")
                    .map(c => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
                    .join("")
            );
            return JSON.parse(json);
        } catch {
            return null;
        }
    }

    function _isTokenExpired(token) {
        const payload = _decodeJwtPayload(token);
        if (!payload || typeof payload.exp !== "number") return true;
        return payload.exp * 1000 <= Date.now();
    }



    // ----------- route guard ------------------

    function requireAuth() {
        if (!isLoggedIn()) {
            const next = encodeURIComponent(window.location.pathname);
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
    async function authFetch(url, options={}) {
        const token = getToken();

        const headers = {
            ...(options.headers || {}),
            ...(token ? {"Authorization": "Bearer " + token} : {}),
        };

        const response = await fetch(url, {...options, headers});

        if (response.status === 401) {
            _removeToken();
            const next = encodeURIComponent(window.location.pathname);
            window.location.replace("/login.html?next=" + next);
            return new Promise(() => {});
        }

        return response;
    }

    // ----------- public interface ---------------

    return {
        getToken,
        getRole,
        isLoggedIn,
        requireAuth,
        login,
        register,
        logout,
        fetch: authFetch,
    };

})();
