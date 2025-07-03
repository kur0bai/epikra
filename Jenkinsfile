pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'epikra_app'
    }

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'main', url: 'https://github.com/kur0bai/epikra.git'
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    // if old container is running 
                    sh 'docker-compose down || true'

                    // creating images
                    //sh 'docker-compose build'
                    //sh 'docker-compose up -d'
                    sh 'docker-compose up --build'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Epikra deployed successfully.'
        }
        failure {
            echo '❌ Deployment failed. Check the logs.'
        }
    }
}
