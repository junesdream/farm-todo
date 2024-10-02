# Farmstack

Farmstack is a simple to-do list application built using a modern frontend stack (React) and a backend powered by FastAPI. The backend communicates with a MongoDB database and the project is fully containerized using Docker. This project is still a work in progress.

## ⚙️ Technologies

- Frontend: React, JavaScript
- Backend: FastAPI, Python
- Database: MongoDB (hosted on MongoDB Atlas)
- Containerization: Docker, Docker-Compose

## 🚀 Current Status

The project is not fully complete, but the following features have been partially implemented:

- Create and delete to-do lists
- Add and remove items from a to-do list
- Mark items as completed
- Connect to a MongoDB database

## 📦 Setup & Installation

### Prerequisites

- You need Docker and Docker-Compose installed on your system.
- A MongoDB Atlas account (or a local MongoDB instance).

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/farmstack.git
   cd farmstack     
   ```
2. Create a `.env` file in the root directory with the following content:

   ```bash
   MONGODB_URI="mongodb+srv://username:password@cluster0.mongodb.net/todo"     
   ```
3. Start the application using Docker-Compose:

   ```bash
   docker-compose up --build
   ````
4. Access the application:

    Frontend: http://localhost:3000
    Backend: http://localhost:3001

The frontend runs on port 3000, and the backend on 3001. The NGINX configuration ensures that all API traffic is forwarded to the backend. 

## Stopping the Containers
To stop the containers after you're done with development, run:
   
   ```bash
   docker-compose down
   ```
🛠️ To-Do (Known Issues)

This project is still in development. Here are the known issues and the next steps:

    Frontend Issues: The rendering of the to-do list component is inconsistent.
    MongoDB Connection: Need to optimize the MongoDB connection.
    Deployment: Prepare the project for deployment to a live environment.

🤝 Contributing
Contributions are welcome! To contribute:

    Fork this repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes and commit (git commit -m 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a Pull Request.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.