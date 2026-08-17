pipeline {
    agent any

    triggers {
        cron('0 12 * * *')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        ALLURE = 'D:\\2345Downloads\\Software\\allure.cmd'
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
                bat ".venv\\Scripts\\python.exe -m scripts.run_tests --junitxml=reports\\junit.xml --clean-alluredir"
            }
            post {
                always {
                    bat "if exist allure-results %ALLURE% generate allure-results -o reports\\allure-report --clean"
                    script {
                        if (fileExists('reports/junit.xml')) {
                            junit testResults: 'reports/junit.xml'
                        }
                    }
                    archiveArtifacts artifacts: 'reports/**/*,logs/**/*,screenshots/**/*,allure-results/**/*', excludes: '**/*element.png', allowEmptyArchive: true
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Test Report'
                    ])
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports/allure-report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report'
                    ])
                    mail to: '3026288915@qq.com',
                        subject: "[${env.JOB_NAME}] Build #${env.BUILD_NUMBER} ${currentBuild.currentResult ?: 'SUCCESS'} - 测试报告",
                        body: """
                            ${env.JOB_NAME} Build #${env.BUILD_NUMBER} ${currentBuild.currentResult ?: 'SUCCESS'}
                            Console: ${env.BUILD_URL}
                            HTML Report: ${env.BUILD_URL}Test_20Report/
                            Allure Report: ${env.BUILD_URL}Allure_20Report/
                        """
                }
            }
        }
    }
}
