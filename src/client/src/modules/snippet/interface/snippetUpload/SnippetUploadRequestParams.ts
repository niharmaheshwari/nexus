export class SnippetUploadRequestParams {
    constructor(
        public desc: string,
        public tags: string[],
        public email: string
    ) {}
    params(): Record<string, any> {
        return {
            desc: this.desc,
            tags: this.tags,
            email: this.email
        };
    }
}