export class SnippetSearchRequestParams {
    constructor(
        public email: string,
        public searchString: string,
    ) {}
    params(): Record<string, string> {
        return {
            email: this.email,
            search_string: this.searchString
        };
    }
}