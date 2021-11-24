import axios, {Method} from "axios";
import userProfile from "../user/serviceLayer/userProfile";

class NetworkLayer {
    private static instance: NetworkLayer

    private constructor() {
    }

    public static shared(): NetworkLayer {
        if (!NetworkLayer.instance) {
            NetworkLayer.instance = new NetworkLayer();
        }
        return NetworkLayer.instance;
    }

    public async apiRequest(method: Method,
                      relativeUrl: string,
                      queryParameters?: Record<string, string>,
                      bodyParameters?: Record<string, string>,
                      headers?: Record<string, string>,
                      defaultHeaders: boolean = true,
                      baseUrl: string | undefined = undefined,
                      ): Promise<any> {
        if (process.env.REACT_APP_SERVER !== undefined && baseUrl === undefined) {
            baseUrl = process.env.REACT_APP_SERVER
        }
        if (process.env.REACT_APP_SERVER === undefined && baseUrl === undefined) {
            baseUrl = "http://localhost:5000/api"
        }
        if (defaultHeaders) {
            headers = {...headers, "Content-type": "application/json"}
        }
        if (userProfile.authenticated && userProfile.idToken !== undefined) {
            headers = {...headers, "token": userProfile.idToken}
        }
        const response = await axios.request({
            method: method,
            baseURL: baseUrl,
            url: relativeUrl,
            headers: headers,
            params: queryParameters,
            data: bodyParameters
        })

        if (response.data.status_code !== undefined && response.data.status_code !== 200) {
            return Promise.reject(response);
        }
        return response;
    }

    public async uploadFile(method: Method,
                            relativeUrl: string, data: any = {},
                            file: any, headers?: Record<string, string>,
                            baseUrl: string | undefined = undefined): Promise<any> {
        if (process.env.REACT_APP_SERVER !== undefined && baseUrl === undefined) {
            baseUrl = process.env.REACT_APP_SERVER
        }
        if (process.env.REACT_APP_SERVER === undefined && baseUrl === undefined) {
            baseUrl = "http://localhost:5000/api"
        }
        const formData = new FormData();
        formData.append("data", JSON.stringify(data));
        formData.append("file", file);
        headers = {...headers, 'Content-type': 'multipart/form-data'}

        console.log("Sending data:", JSON.stringify(data))

        if (userProfile.authenticated && userProfile.idToken !== undefined) {
            headers = {...headers, "token": userProfile.idToken}
        }

        const response = await axios.request({
            method: method,
            baseURL: baseUrl,
            url: relativeUrl,
            headers: headers,
            data: formData
        })
        if (response.data.status_code !== undefined && response.data.status_code !== 200) {
            return Promise.reject(response);
        }
        return response;
    }
}

export default NetworkLayer.shared()