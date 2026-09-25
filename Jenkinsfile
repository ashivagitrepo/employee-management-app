pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Creating virtual environment..."
                    python3 -m venv venv

                    echo "Installing dependencies..."
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "Running application syntax test..."
                    ./venv/bin/python -m py_compile app.py

                    echo "Test completed successfully."
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'

                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=Employee-Management \
                              -Dsonar.projectName=Employee-Management \
                              -Dsonar.sources=app.py,templates \
                              -Dsonar.exclusions=venv/**,**/__pycache__/**
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t employee-management:latest .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker tag employee-management:latest \
                            dockerymal/employee-management:latest

                        docker push dockerymal/employee-management:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Stopping old application container..."
                    docker rm -f employee-management || true

                    echo "Pulling latest image from Docker Hub..."
                    docker pull dockerymal/employee-management:latest

                    echo "Starting new application container..."
                    docker run -d \
                        --name employee-management \
                        -p 5001:5000 \
                        --restart unless-stopped \
                        dockerymal/employee-management:latest

                    echo "Deployment completed."
                '''
            }
        }
    }
}
