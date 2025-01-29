
pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'  // Define the Docker Compose file name
    }

    triggers {
        pollSCM('H/5 * * * *')  // Poll GitHub every 5 minutes for changes
    }

    stages {
        stage('Check for Changes') {
            steps {
                script {
                    echo 'Checking for changes in the repository...'
                    checkout scm  // Pull the latest code from the repository
                }
            }
        }

        stage('Stop and Remove Existing Containers') {
            steps {
                script {
                    echo 'Stopping and removing existing containers...'
                    sh 'docker compose down --remove-orphans'
                }
            }
        }

        stage('Build and Start Containers') {
            steps {
                script {
                    echo 'Building and starting the application using Docker Compose...'
                    sh 'docker compose up --build -d'
                }
            }
        }

        stage('Remove Old <none> Images') {
            steps {
                script {
                    echo 'Removing old Docker images with <none> tag...'
                    sh 'docker images --filter "dangling=true" -q | xargs -r docker rmi -f'
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully. The application is running!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
        always {
            echo 'Pipeline run completed.'
        }
    }
}
