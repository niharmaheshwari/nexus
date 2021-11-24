import {SnippetSearchRequestParams} from "../interface/snippetSearch/SnippetSearchRequestParams";
import networkLayer from "../../networkLayer/networkLayer";
import userProfile from "../../user/serviceLayer/userProfile";

class SnippetService {
    constructor() {
        console.log("Snippet Service Created");
    }

    async search(query: string) {
        if (userProfile.email === undefined) {
            return Promise.reject("Email is missing")
        }
        const requestParams = new SnippetSearchRequestParams(userProfile.email, query);
        const response = await networkLayer.apiRequest("post",
            "search",
            undefined,
            requestParams.params());
        console.log("GOT API Response:", JSON.stringify(response));
        return response;
    }
}

export default new SnippetService();