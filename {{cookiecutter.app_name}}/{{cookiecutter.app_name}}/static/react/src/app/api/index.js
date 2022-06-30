import Axios from 'axios';

const instance = Axios.create({
  headers: {'Content-Type': 'application/json'},
  transformResponse: [function (responseData) {
    return JSON.parse(responseData)
  }]
});

// Handle 401
instance.interceptors.response.use( (response) => {
  return response;
}, (error) => {
  if (error.response.status === 401) {
    return window.location = '/login'
  } else {
    return Promise.reject(error);
  }
})

const Api = {
  // data should be passed in every request, else Axios removes the 'Content-Type'
  // header
  user: () => instance.get("/user", {data: null}),
};

export default Api;
