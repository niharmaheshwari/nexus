import {OtpRequestParams} from "../interface/opt/OtpRequestParams";
import networkLayer from "../../networkLayer/networkLayer";

class OtpService {
    constructor() {
        console.log("OTP service created")
    }

    async confirmOtp(email: string, otp: string) {
        const requestParams = new OtpRequestParams(email, otp);
        const response = await networkLayer.apiRequest("post",
            "auth/confirm-signup",
            undefined,
            requestParams.params());
        console.log("Got API response:" + JSON.stringify(response));
        return response;
    }
}

export default new OtpService();