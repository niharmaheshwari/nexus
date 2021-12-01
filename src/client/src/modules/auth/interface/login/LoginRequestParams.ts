export class LoginRequestParams {
    constructor(
        public email: string,
        public password: string,
    ) {}
    params(): Record<string, string> {
        return {
            email: this.email,
            password: this.password
        };
    }
}