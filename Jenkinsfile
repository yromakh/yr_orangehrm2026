pipeline {
    agent any

    environment {
        ORANGEHRM_URL = 'http://localhost:8080/web/index.php/dashboard/index'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Install Playwright') {
            steps {
                bat 'python -m playwright install'
            }
        }

        stage('Run tests') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'orangehrm-credentials',
                        usernameVariable: 'ORANGEHRM_USERNAME',
                        passwordVariable: 'ORANGEHRM_PASSWORD'
                    )
                ]){                
                    bat 'python -m pytest --html=reports/report.html --self-contained-html'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/report.html',
                         allowEmptyArchive: true
        }
    }
}