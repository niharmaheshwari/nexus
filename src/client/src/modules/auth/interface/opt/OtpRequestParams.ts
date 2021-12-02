export class OtpRequestParams {
    constructor(
        public email: string,
        public code: string,
    ) {}
    params(): Record<string, string> {
        return {
            email: this.email,
            code: this.code
        };
    }
}