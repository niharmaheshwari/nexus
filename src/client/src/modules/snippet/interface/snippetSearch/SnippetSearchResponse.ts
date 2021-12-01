export interface Snippets {
    snippets: Snippet[]
}

export interface Snippet {
    audit: Audit,
    author: string,
    desc: string,
    id: string,
    lang: string,
    shares: string[],
    tags: string[]
    uri: string
}

export interface Audit {
    creation_date: Date,
    creation_user: string,
    last_upd_date: Date,
    last_upd_user: string
}