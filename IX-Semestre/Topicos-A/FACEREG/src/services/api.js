import axios from 'axios';

var headers = {
"Acess-Control-Allow-Origin": "*",
"Acess-Control-Allow-Methods": "GET,POST, PUT,DELETE,PATCH,OPTIONS",
"Acess-Control-Allow-Headers":"X-Requested-With,content-type,Authorization",
'token': '8f1ce726defe4e9ba4d21d9a5709320f'};
const api = axios.create({ mode: "no-cors" ,baseURL: 'https://api.luxand.cloud/subject/',headers: headers});

export default api;