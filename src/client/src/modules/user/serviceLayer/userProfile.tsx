class UserProfile {
    private static instance: UserProfile
    private name?: string
    private _email?: string
    private isAuthenticated: boolean
    private token?: AuthToken

    get authenticated(): boolean {
        return this.isAuthenticated
    }

    get idToken(): string | undefined {
        return this.token?.idToken
    }

    get email(): string | undefined {
        return this._email;
    }

    private constructor() {
        this.isAuthenticated = false;
    }

    public static shared(): UserProfile {
        if (!UserProfile.instance) {
            UserProfile.instance = new UserProfile();
        }
        return UserProfile.instance;
    }

    public updateAuthStatus(authenticated: boolean, token?: AuthToken) {
        this.isAuthenticated = authenticated;
        this.token = token;
    }

    public updateUserDetails(name?: string, email?: string) {
        this.name = name;
        this._email = email;
    }
}

export class AuthToken {
    private access_token?: string
    private expires_in?: number
    private id_token?: string
    private refresh_token?: string
    private token_type?: string

    get accessToken(): string | undefined {
        return this.access_token;
    }

    get tokenExpiry(): number | undefined {
        return this.expires_in;
    }

    get idToken(): string | undefined {
        return this.id_token;
    }

    get refreshToken(): string | undefined {
        return this.refresh_token;
    }

    get tokenType(): string | undefined {
        return this.token_type;
    }
}

export default UserProfile.shared();