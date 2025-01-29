pipeline {
    agent any

    environment {
        IMAGE_NAME = 'local-python-app'     // Name of the Docker image
        CONTAINER_NAME = 'python-app-container'  // Name of the Docker container
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
        stage('Delete Existing Docker Image') {
            steps {
                script {
                    echo 'Deleting existing Docker image (if it exists)...'
                    sh """
                        docker image rmi --force ${IMAGE_NAME}:latest || true
                    """
                }
            }
        }
        stage('Build New Docker Image') {
            steps {
                script {
                    echo 'Building new Docker image...'
                    sh """
                        docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }
        stage('Stop and Remove Existing Container') {
            steps {
                script {
                    echo 'Stopping and removing existing Docker container (if it exists)...'
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }
        stage('Deploy New Container') {
            steps {
                script {
                    echo 'Deploying the new Docker container...'
                    sh """
                        docker run -d --name ${CONTAINER_NAME}  ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully. New image is running!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
        always {
            echo 'Pipeline run completed.'
        }
    }
}
