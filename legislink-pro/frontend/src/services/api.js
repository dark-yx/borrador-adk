import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api/v1', // La URL base de tu API de Flask
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  delegateTask(query, inputData = {}) {
    return apiClient.post('/delegate', { query, input_data: inputData });
  }
}; 