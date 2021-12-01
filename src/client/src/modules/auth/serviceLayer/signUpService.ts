import {SignUpRequestParams} from "../interface/signUp/SignUpRequestParams";
import NetworkLayer from "../../networkLayer/networkLayer";
class SignUpService {
    constructor() {
        console.log("Sign Up Service Created")
    }
    getFormattedDate(date: Date): string {
        const year = date.getFullYear();

        let month = (1 + date.getMonth()).toString();
        month = month.length > 1 ? month : '0' + month;

        let day = date.getDate().toString();
        day = day.length > 1 ? day : '0' + day;

        return month + '/' + day + '/' + year;
    }
    async signUp(name: string,
                 email: string,
                 phone: string,
                 birthdate: Date,
                 password: string): Promise<any> {
        const birthdayString = this.getFormattedDate(birthdate);
        const requestParams = new SignUpRequestParams(name, email, phone, password, birthdayString);
        const response = await NetworkLayer.apiRequest("post",
            "auth/signup",
            undefined,
            requestParams.params());
        console.log("GOT API Response:", JSON.stringify(response));
        return response;
    }
}

export default new SignUpService();