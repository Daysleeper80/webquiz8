/**
 * The session manager is a singleton object that manages user state
 * on the frontend (client side). It provides a client-side user 
 * management API. It has methods to authenticate a user, log in the
 * user, log out, query its state, and so on.
 * The API acts as front end to a server-side API. Communication
 * is done by the FETCH API.
 * 
 * (c) Joao Galamba, 2022
 * $LICENSE(MIT)
 */

////////////////////////////////////////////////////////////////////////////////
///
///     USER MANAGEMENT (CLIENT-SIDE) API
///
////////////////////////////////////////////////////////////////////////////////

// The authentication process simulated here uses JWTs, HTTP-only 
// cookies and plain and private JavaScript objects to authenticate 
// and store local information about the current user.
//
// On the client side, we avoid using localStorage in order to prevent
// XSS attacks. We also use HTTP-only secure cookies to further prevent
// XSS attacks. CSRF attacks are mitigated by the use of SameSite cookies.

export const sessionManager = (function() {
    let currentUser = undefined;
    let that = {};
    const backendURL = 'http://localhost:5000';

    // *************** PUBLIC METHODS ***************

    that.isLoggedIn = async function() {
        if (currentUser === undefined) {
            restoreCurrentUser(await backendGetCurrentUser());
        }
        return currentUser !== undefined;
    };

    that.login = async function(username, password) {
        if (await that.isLoggedIn()) {
            throw new LoginError('Already logged in.');
        }
        const serverUserInfo = await backendLogin(username, password);
        if (!serverUserInfo) {
            throw new LoginError(`Invalid login for user ${username}.`);
        }
        restoreCurrentUser(serverUserInfo);
    };

    that.getUser = async function () {
        if (!await that.isLoggedIn()) {
            throw new UserError('Currently no user is logged in.');
        }
        return {...currentUser};  // return a clone of our private object
    };

    that.createUser = async function(userDetails) {
        if (await that.isLoggedIn()) {
            throw new UserError('Already logged in.');
        }
        const serverUserInfo = await backendCreateUser(userDetails);
        if (!serverUserInfo) {
            throw new UserError('Unable to create user');
        }
        restoreCurrentUser(serverUserInfo);
        return {...currentUser};
    };

    that.logout = async function() {
        if (!await that.isLoggedIn()) {
            throw new LogoutError('No login session.');
        }
        await backendLogout();
        currentUser = undefined;
    };

    that[Symbol.toStringTag] = 'SessionManager';

    // Return an immutable object.
    return Object.freeze(that);

    // *************** PRIVATE METHODS ***************

    async function backendLogin(username, password) {
        const url = `${backendURL}/user/login`;
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            body: JSON.stringify({username, password}),
            headers: {
                'Content-Type': 'application/json'
            },
        });
        if (response.status !== 200) {
            throw new BackendError('Unable to fetch resource: ' + url);
        }
        return await response.json();
    }

    async function backendLogout() {
        const url = `${backendURL}/user/login`;
        const response = await fetch(url, {
            method: 'DELETE',
            mode: 'cors',
            credentials: 'include',
        });
        if (response.status !== 200) {
            throw new BackendError('Unable to fetch resource: ' + url);
        }
    }

    async function backendGetCurrentUser() {
        const url = `${backendURL}/user/current`;
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            credentials: 'include',
        });
        if (response.status !== 200) {
            throw new BackendError('Unable to fetch resource: ' + url);
        }
        return await response.json();
    }

    async function backendCreateUser(userDetails) {
        const url = `${backendURL}/user/current`;
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            body: JSON.stringify(userDetails),
            headers: {
                'Content-Type': 'application/json'
            },
        });
        if (response.status !== 200) {
            throw new BackendError('Unable to fetch resource: ' + url);
        }
        return await response.json();
    }

    function restoreCurrentUser(serverSideUserInfo) {
        if (!serverSideUserInfo) {
            currentUser = undefined;
            return;
        }
        currentUser = {
            ...serverSideUserInfo,
            [Symbol.toStringTag]: 'WebQuizUser',
        };
    }
})();

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
export class SessionManagerError extends Error {
    constructor(...params) {
        super(...params);
        this.name = this.constructor.name;
    }
}

export class BackendError extends SessionManagerError {}
export class UserError extends SessionManagerError {}
export class LoginError extends UserError {}
export class LogoutError extends UserError {}
