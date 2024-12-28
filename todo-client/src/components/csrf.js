export const getCsrfToken = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/csrf/', {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      return data.csrfToken;
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
    }
  };
  