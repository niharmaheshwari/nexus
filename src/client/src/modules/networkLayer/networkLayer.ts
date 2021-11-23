import axios, {AxiosResponse, Method} from "axios";

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
                      baseUrl: string = "http://localhost.charlesproxy.com:5000/api",
                      ): Promise<any> {
        if (defaultHeaders) {
            headers = {...headers, "Content-type": "application/json"}
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
}

export default NetworkLayer.shared()