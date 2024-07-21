pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment {
        registry = 'nguyenbao19/chat-with-docs'
        registryCredentialDockerhub = 'dockerhub_connection'
        imageVersion = "0.${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out latest code...'
                    checkout scm
                }
            }
        }
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
        stage('Deploy application to k8s') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'nguyenbao19/jenkins:latest' // The image containing helm
                        alwaysPullImage true // Always pull image in case of using the same tag
                    }
                }
            }
            steps {
                script {
                    container("helm") {
                        echo "Ready to deploy ..."
                        sh "helm upgrade --install model-release ./helm/model-serving --namespace model-serving"
                        echo "Deploy successfully, ready to serve request ..."
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
