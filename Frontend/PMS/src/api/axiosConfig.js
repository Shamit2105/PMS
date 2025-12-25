import axios from "axios";

const api = axios.create({
    baseURL:"http://localhost:8000",
    headers:{
        "Content-Type":"application/json",
    },
});

api.interceptors.request.use((config)=>{
    const access = localStorage.getItem("access");
    if(access)
        config.headers.Authorization=`Bearer ${access}`;
    return config;
});

api.interceptors.response.use(
    response=>response,
    async error =>{
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry)
        {
            originalRequest._retry = true;

            try
            {
                const refresh = localStorage.getItem("refresh");
                const res = await axios.post(
                    "http://localhost:8000/users/token/refresh/",
                    {refresh}
                );
                localStorage.setItem("access",res.data.access);
                originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
                return api(originalRequest);
            }
            catch{
                localStorage.clear();
                window.location.href="/login";
            }
        }
        return Promise.reject(error);
    }
);

export default api;