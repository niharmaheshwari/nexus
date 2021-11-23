class UserProfile {
    private static instance: UserProfile
    private name?: string
    private email?: string

    private constructor() {
    }

    public static shared(): UserProfile {
        if (!UserProfile.instance) {
            UserProfile.instance = new UserProfile();
        }
        return UserProfile.instance;
    }

    public updateUserDetails(name?: string, email?: string) {
        this.name = name
        this.email = email
    }
}

export default UserProfile.shared();