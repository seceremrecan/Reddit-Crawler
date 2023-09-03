
# Flask Reddit Crawler

Flask Reddit Crawler is a Flask application used to view and save Reddit posts through a user-friendly interface. The application allows users to connect to the Reddit API, log in, and view posts from the 'tennis' subreddit. It is built using the Flask web framework, SQLAlchemy for database management, and praw as the Reddit API wrapper.

## Features

- User Registration: Users can create an account by providing their username and password. The registration data is securely stored in a PostgreSQL database.

- User Login: Registered users can log in to their accounts using their username and password. The application verifies the user's credentials against the stored data in the database.

- User Control Panel: After logging in, users are greeted with a message and automatically redirected to a page displaying the posts. They can view all the posts available in the database.

- Reddit API Integration: The application connects to the Reddit API using praw. It crawls the 'tennis' subreddit and adds new posts to the PostgreSQL database. 

## Technologies Used

- Flask: A micro web framework used for developing web applications.

- Flask-Login: A Flask extension used for user authentication and session management.

- praw: A Python wrapper for the Reddit API that facilitates interaction with Reddit's features and data.

- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library used for database management.

- PostgreSQL: An open-source relational database management system used for storing user and post data.

- Docker: A container platform used for containerization and portability of the application.

## Installation

To run the Flask Reddit Crawler locally, follow these steps:

1. Clone the repository: `https://github.com/seceremrecan/Reddit-Crawler.git`

2. Install the required dependencies:  `pip install -r requirements.txt`

3. Configure your Reddit API keys and PostgreSQL database settings in the `config.ini` file.

4. Run the application: `python app.py`

5. Open your web browser and access the application at `http://localhost:5000`.

or

## Docker Installation

1. Install Docker: (https://docs.docker.com/get-docker/)

2. In the terminal, navigate to the directory containing the Dockerfile and build the Docker image using the following command:
      
    `docker build -t myflaskapp .`
    
3. Run the application using Docker-compose:

   ```shell
   docker-compose up --build
   
  -> This command will start the services defined in the docker-compose.yml file (web and db). The application will be running at http://localhost:5000.

4. Access the application by visiting http://localhost:5000 in your web browser.

