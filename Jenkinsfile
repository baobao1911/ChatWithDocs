pipeline {
    agent any

    options {
        // Maximum number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment {
        registry = 'nguyenbao19/chat-with-docs'
        registryCredentialDockerhub = 'dockerhub_connection'
        imageVersion = "0.${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment...'
                    dockerImage = docker.build("${registry}:${imageVersion}")

                    echo 'Pushing image to DockerHub...'
                    docker.withRegistry('', registryCredentialDockerhub) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            cleanWs()
        }
    }
}
