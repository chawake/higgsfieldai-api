#!groovy


pipeline {
    agent any
    stages {
        stage("Build and up") {
            steps {
                sh "docker compose up -d --build"
            }
        }
    }
}
