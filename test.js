import axios from 'axios';

class APIBase {
    // Constructor to initialize APIBase with custom configuration
    constructor(config) {
        // Configuration defaults are set here, allowing for customization
        this.config = {
            baseURL         : config.baseURL || 'http://example.com', // Base URL for API requests
            defaultHeaders  : config.defaultHeaders || {},     // Default headers for all requests
            timeout         : config.timeout || 10000,               // Request timeout in milliseconds
            tokenKey        : config.tokenKey || 'jwtToken',        // Key for storing JWT token in local storage
            retryLimit      : config.retryLimit || 3,             // Number of retries for failed requests
            debounceDelay   : config.debounceDelay || 300,     // Delay for debouncing requests
            // Additional configurable parameters can be added here
        };

        // Creating an axios instance with the provided configuration
        this.apiClient = axios.create({
            baseURL: this.config.baseURL,
            headers: this.config.defaultHeaders,
            timeout: this.config.timeout,
        });

        // Interceptors for handling request and response
        this.apiClient.interceptors.request.use(
            this.handleRequestInterception,
            this.handleError
        );
        this.apiClient.interceptors.response.use(
            this.handleSuccessResponse,
            this.handleErrorResponse
        );
    }

    // Method to handle request interception, e.g., to add auth tokens
    handleRequestInterception = (config) => {
        const token = this.getToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    };

    // Method to handle successful responses
    handleSuccessResponse = (response) => {
        return response;
    };

    // Method to handle error responses
    handleErrorResponse = (error) => {
        if (error.response) {
            console.error("Error data:", error.response.data);
            console.error("Error status:", error.response.status);
            console.error("Error headers:", error.response.headers);
        } else if (error.request) {
            console.error("Error request:", error.request);
        } else {
            console.error("Error message:", error.message);
        }
        return Promise.reject(error);
    };

    // General method to make an API request
    async makeRequest(method, endpoint, data = null, headers = {}) {
        try {
            const response = await this.apiClient({
                method,
                url: endpoint,
                data,
                headers
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    // Specific methods for different HTTP verbs
    get(endpoint, params = {}, headers = {}) {
        return this.makeRequest('get', endpoint, null, { ...headers, params });
    }

    post(endpoint, data, headers = {}) {
        return this.makeRequest('post', endpoint, data, headers);
    }

    put(endpoint, data, headers = {}) {
        return this.makeRequest('put', endpoint, data, headers);
    }

    patch(endpoint, data, headers = {}) {
        return this.makeRequest('patch', endpoint, data, headers);
    }

    delete(endpoint, headers = {}) {
        return this.makeRequest('delete', endpoint, null, headers);
    }

    // Methods for token management in local storage
    getToken() {
        return localStorage.getItem(this.config.tokenKey);
    }

    setToken(token) {
        localStorage.setItem(this.config.tokenKey, token);
    }

    removeToken() {
        localStorage.removeItem(this.config.tokenKey);
    }

    // Utility method to format dates
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US');
    }

    // Utility method to parse JSON safely
    parseJSON(response) {
        try {
            return JSON.parse(response);
        } catch (error) {
            return null;
        }
    }

    // Utility method to serialize URL parameters
    serializeParams(params) {
        return Object.entries(params).map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join('&');
    }

    // Method to check if response status is successful
    checkStatus(response) {
        if (response.status >= 200 && response.status < 300) {
            return response;
        } else {
            throw new Error(response.statusText);
        }
    }

    // Method to extract error message from response
    extractErrorMessage(error) {
        return error.response ? error.response.data.message : error.message;
    }

    // Method to build Authorization header
    buildAuthHeader(token) {
        return { Authorization: `Bearer ${token}` };
    }

    // Utility method for logging requests
    logRequest(url, method, data) {
        console.log(`Requesting ${method.toUpperCase()} ${url} with data:`, data);
    }

    // Debounce utility to prevent rapid firing of requests
    debounceRequest(func) {
        let inDebounce;
        return (...args) => {
            clearTimeout(inDebounce);
            inDebounce = setTimeout(() => func.apply(this, args), this.config.debounceDelay);
        };
    }

    // Method for validating response schema (implementation pending)
    validateResponseSchema(response, schema) {
        // Implement schema validation logic if required
    }

    // Interceptor for token refresh logic
    tokenRefreshInterceptor(apiClient, refreshToken) {
        apiClient.interceptors.response.use(
            response => response,
            async error => {
                const originalRequest = error.config;
                if (error.response.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    // Implement token refresh logic here
                    return apiClient(originalRequest);
                }
                return Promise.reject(error);
            }
        );
    }
}
