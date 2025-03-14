# Web Scraper UI with FastAPI Backend

## Overview
This project is a web scraping tool with a user-friendly frontend built in React and a backend powered by FastAPI. It allows users to scrape websites, extract media, fetch data, and manage scraping history. The backend provides a robust API for scraping and data extraction, while the frontend offers an intuitive interface for interacting with the API.

## Features

### Frontend Features
- **Scrape Single Page:** Extract data from a single webpage.
- **Scrape Multiple Pages:** Scrape multiple pages with customizable parameters.
- **Extract Media:** Extract images, videos, and other media from a webpage.
- **Fetch Data:** Fetch data from a URL or multiple URLs.
- **History Management:** View, copy, and delete scraping history.
- **Responsive Design:** Sleek, modern UI with dark mode support.

### Backend Features
- **FastAPI Endpoints:** RESTful API for scraping, fetching, and data extraction.
- **CORS Support:** Secure cross-origin requests for the frontend.
- **Error Handling:** Detailed error messages for API failures.
- **Scalable:** Designed to handle multiple scraping requests efficiently.

## Tech Stack

### Frontend
- **React:** Frontend framework for building the UI.
- **TypeScript:** For type-safe development.
- **Tailwind CSS:** For modern, responsive styling.
- **Axios:** For making API requests.

### Backend
- **FastAPI:** High-performance backend framework.
- **Python:** Backend programming language.
- **BeautifulSoup:** For web scraping.
- **Uvicorn:** ASGI server for running the backend.

## Setup Instructions

### Prerequisites
- **Node.js** (v16 or higher) for the frontend.
- **Python** (v3.8 or higher) for the backend.
- **Git** for version control.

### Frontend Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/web-scraper-ui.git
    cd web-scraper-ui/frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run dev
    ```
4. Open the app in your browser at `http://localhost:5173`.

### Backend Setup
1. Navigate to the backend directory:
    ```bash
    cd ../backend
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the FastAPI server:
    ```bash
    uvicorn main_route:app --reload
    ```
5. The backend will be available at `http://localhost:8000`.

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

1. **Scrape Single Page**
    - **URL:** `/scrape_single_page/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "url": "https://example.com"
        }
        ```
    - **Response:**
        ```json
        {
          "data": "Scraped content from the page"
        }
        ```

2. **Scrape Multiple Pages**
    - **URL:** `/scrape/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "url": "https://example.com",
          "whitelist": ["blog", "news"],
          "blacklist": ["login", "admin"],
          "link_limit": 10
        }
        ```
    - **Response:**
        ```json
        {
          "all_links": ["https://example.com/blog", "https://example.com/news"]
        }
        ```

3. **Extract Media from Single Page**
    - **URL:** `/single_page_media/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "url": "https://example.com"
        }
        ```
    - **Response:**
        ```json
        {
          "media": ["https://example.com/image.jpg", "https://example.com/video.mp4"]
        }
        ```

4. **Fetch Data**
    - **URL:** `/fetch/`
    - **Method:** `GET`
    - **Query Parameter:**
        ```
        ?url=https://example.com
        ```
    - **Response:**
        ```json
        {
          "data": "Fetched data from the URL"
        }
        ```

5. **Fetch Multiple URLs**
    - **URL:** `/fetch_multiple/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "urls": ["https://example.com", "https://another.com"]
        }
        ```
    - **Response:**
        ```json
        {
          "data": {
            "https://example.com": "Fetched data",
            "https://another.com": "Fetched data"
          }
        }
        ```

6. **Extract Links**
    - **URL:** `/extract_links/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "url": "https://example.com"
        }
        ```
    - **Response:**
        ```json
        {
          "links": ["https://example.com/page1", "https://example.com/page2"]
        }
        ```

7. **Extract Related Links**
    - **URL:** `/extract_related_links/`
    - **Method:** `POST`
    - **Request Body:**
        ```json
        {
          "url": "https://example.com"
        }
        ```
    - **Response:**
        ```json
        {
          "related_links": ["https://example.com/about", "https://example.com/contact"]
        }
        ```

## Usage Examples

### Scrape a Single Page
1. Enter the URL in the frontend.
2. Select the "Scrape Single Page" action.
3. View the scraped data in the results section.

### Fetch Data from Multiple URLs
1. Enter multiple URLs (comma-separated) in the frontend.
2. Select the "Fetch Multiple URLs" action.
3. View the fetched data in the results section.

### Manage History
1. Navigate to the History Page.
2. View, copy, or delete scraping history.

## Screenshots

### Home Page
![Home Page](path/to/homepage-screenshot.png)

### History Page
![History Page](path/to/historypage-screenshot.png)

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, please contact:
- **Your Name:** your.email@example.com
- **GitHub:** [your-username](https://github.com/your-username)

This README provides a complete guide to setting up, using, and contributing to the project. Let me know if you need further assistance! 🚀
