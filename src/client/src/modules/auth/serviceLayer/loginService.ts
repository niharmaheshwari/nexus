import {LoginRequestParams} from "../interface/login/LoginRequestParams";
import networkLayer from "../../networkLayer/networkLayer";

class LoginService {
    constructor() {
        console.log("Login Service Created");
    }

    async login(email: string, password: string) {
        const requestParams = new LoginRequestParams(email, password);
        const response = await networkLayer.apiRequest("post",
            "auth/login",
            undefined,
            requestParams.params());
        console.log("GOT API Response:", JSON.stringify(response));
        return response;
    }
}

export default new LoginService();