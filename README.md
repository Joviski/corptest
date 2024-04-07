# File Analysis Project

This project consists of a React frontend and a Flask backend that perform data analysis based on the uploaded file type. Here's how to get started and use the application.

## Getting Started

To run the application, you need to have Docker and Docker Compose installed on your machine. Once you have those installed, follow these steps:

### Running the Application

1. Open a terminal or command prompt.
2. Navigate to the project directory where `docker-compose.yml` is located.
3. Run the following command to build and start the containers:

   ```bash
   docker-compose up --build

This will start the frontend and backend services in containers and expose them on your local machine.

### Accessing the Application

- Frontend URL: http://localhost:3000

    The frontend allows you to upload CSV, PNG, and TXT files for analysis.
    
- Backend URL: POST http://localhost:5000/analyze

    The backend provides an API endpoint for analyzing the uploaded files.
    
### Expected Responses

- CSV Input: Uploading a CSV file through the frontend will trigger a JSON output in the console representing the analyzed data.
- PNG Input: Uploading a PNG image will result in a download prompt for the histogram image.
- TXT Input: Uploading a text file will cause a download prompt for the T-SNE visualization result.

### Difficulties Faced

- Response Generation: Initially, there was a challenge in figuring out how to generate and handle the appropriate response for each file type, but this was eventually resolved through iterative development and testing.
- Deployment and CORS: Deployment succeeded, but currently facing a Cross-Origin Resource Sharing (CORS) issue. Despite configuring CORS in the Flask app, the problem persists, indicating a potential configuration issue or misunderstanding of CORS behavior in the production environment.