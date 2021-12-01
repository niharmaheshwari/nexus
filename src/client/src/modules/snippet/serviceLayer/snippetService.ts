import {SnippetSearchRequestParams} from "../interface/snippetSearch/SnippetSearchRequestParams";
import {SnippetUploadRequestParams} from "../interface/snippetUpload/SnippetUploadRequestParams";
import networkLayer from "../../networkLayer/networkLayer";
import userProfile from "../../user/serviceLayer/userProfile";
import {SnippetUpdateRequestParams} from "../interface/snippetUpdate/SnippetUpdateRequestParams";

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

    async fetchSnippet(url: string) {
        const response = await networkLayer.apiRequest("get",
            "",
            undefined,
            undefined,
            undefined,
            false,
            url)
        console.log("Fetch snippet data:", JSON.stringify(response));
        return response;
    }

    async deleteSnippet(id: string) {
        const queryParameters = {
            id
        }
        const response = await networkLayer.apiRequest("delete",
            "snippet",
            queryParameters,
            undefined,
            undefined,
            false)
        return response;
    }

    async uploadSnippet(description: string, tags: string, file: File) {
        if (userProfile.email === undefined) {
            console.log("User email is undefined")
            return Promise.reject("User email not defined")
        }
        const tagsList = tags.split(",")
        const requestParams = new SnippetUploadRequestParams(description, tagsList, userProfile.email)
        return await networkLayer.uploadFile("post",
            "snippet",
            requestParams, file);
    }

    async updateSnippet(id: string, description: string, tags: string, shares: string, file?: File) {
        if (userProfile.email === undefined) {
            console.log("User email is undefined")
            return Promise.reject("User email not defined")
        }
        const tagsList = tags.split(",")
        const shareList = shares.split(",")
        const requestParams = new SnippetUpdateRequestParams(id, description, tagsList, shareList, userProfile.email)
        return await networkLayer.uploadFile("put",
            "snippet",
            requestParams,
            file);
    }
}

export default new SnippetService();