import {SignUpRequestParams} from "../interface/signUp/SignUpRequestParams";
import NetworkLayer from "../../networkLayer/networkLayer";
class SignUpService {
    constructor() {
        console.log("Sign Up Service Created")
    }
    async signUp(name: string,
                 email: string,
                 phone: string,
                 birthdate: Date,
                 password: string) {
        const requestParams = new SignUpRequestParams(name, email, phone, password, birthdate.toDateString());
        const response = await NetworkLayer.apiRequest("post",
            "signup",
            undefined,
            requestParams.params());
        console.log("GOT API Response:", JSON.stringify(response))
    }
}

export default new SignUpService();