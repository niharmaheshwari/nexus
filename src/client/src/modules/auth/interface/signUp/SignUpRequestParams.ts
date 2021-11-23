export class SignUpRequestParams {
    constructor(
        public name: string,
        public email: string,
        public phone: string,
        public password: string,
        public birthdate: string
    ) {}
    params(): Record<string, string> {
        return {
            email: this.email,
            name: this.name,
            birthdate: this.birthdate,
            phone_number: this.phone,
            password: this.password
        };
    }
}