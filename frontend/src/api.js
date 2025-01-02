import axios from 'axios';

const isDevelopment = import.meta.env.MODE === 'development';
const baseURL = isDevelopment ? 'http://localhost:8000' : 'http://jncweb.duckdns.org:8000'

const api = axios.create({
  baseURL,
});

export default api;
