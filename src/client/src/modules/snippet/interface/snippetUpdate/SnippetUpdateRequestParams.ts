export class SnippetUpdateRequestParams {
    constructor(
        public desc: string,
        public tags: string[],
        public shares: string[],
        public email: string
    ) {}
    params(): Record<string, any> {
        return {
            desc: this.desc,
            tags: this.tags,
            email: this.email,
            shares: this.shares
        };
    }
}