pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        HEADLESS = 'true'
        PYTHON = 'D:\\anconda\\python.exe'
    }

    stages {
        stage('准备环境') {
            steps {
                bat """
                    if not exist .venv\\Scripts\\python.exe %PYTHON% -m venv .venv
                    if not exist reports mkdir reports
                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                """
            }
        }

        stage('语法检查') {
            steps {
                bat ".venv\\Scripts\\python.exe -m compileall config pages utils tests scripts"
            }
        }

        stage('浏览器回归测试') {
            steps {
                bat ".venv\\Scripts\\python.exe -m pytest --junitxml=reports\\junit.xml"
            }
        }
    }

    post {
        always {
            node {
                script {
                    if (fileExists('reports/junit.xml')) {
                        junit testResults: 'reports/junit.xml'
                    }
                }
                archiveArtifacts artifacts: 'reports/**,logs/**,screenshots/**,allure-results/**', allowEmptyArchive: true
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}
