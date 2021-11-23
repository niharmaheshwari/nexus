class UserProfile {
    private static instance: UserProfile
    private name?: string
    private _email?: string
    private isAuthenticated: boolean
    private token?: AuthTokens

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

    public updateAuthStatus(authenticated: boolean, token?: AuthTokens) {
        this.isAuthenticated = authenticated;
        this.token = token;
    }

    public updateUserDetails(name?: string, email?: string) {
        this.name = name;
        this._email = email;
    }
}

export class AuthTokens {
    private accessToken?: string
    private tokenExpiry?: number
    private idToken?: string
    private refreshToken?: string
    private tokenType?: string

    constructor(accessToken: string,
                expiry: number,
                idToken: string,
                refreshToken: string,
                tokenType: string) {
        this.accessToken = accessToken;
        this.tokenExpiry = expiry
        this.idToken = idToken
        this.refreshToken = refreshToken
        this.tokenType = tokenType
    }
}

export default UserProfile.shared();