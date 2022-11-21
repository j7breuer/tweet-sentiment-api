pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                withPythonEnv('python3.9') {
                    echo '\n=======================\n[START] Initializing...\n=======================\n'
                    echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL} \n"
                    echo "\n<--------- Installing PyTorch... --------->"
                    sh 'pip3.9 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu'
                    echo "\n<--------- Installing requirements.txt --------->"
                    sh 'pip3.9 install -r requirements.txt --no-cache-dir --index-url http://admin:admin@192.168.50.25:8081/repository/Workstation_PyPi/simple --trusted-host 192.168.50.25'
                    echo '\n=====================\n[END] Initializing...\n=====================\n'
                }
            }
        }
        stage('PyTest Unit Tests') {
            steps {
                withPythonEnv('python3.9') {
                    echo '\n============================\n[START] PyTest Unit Tests...\n============================\n'
                    echo '\n<--------- Running pytest... --------->'
                    sh 'python3.9 -m pytest --cov . --cov-report xml'
                    echo '\n==========================\n[END] PyTest Unit Tests...\n==========================\n'
                }
            }
        }
        stage('Sonar Scans') {
            environment {
                scannerHome = tool 'SonarQubeScanner-4.7.0'
            }
            steps {
                withSonarQubeEnv('SonarQube-8.3.1') {
                    echo '\n======================\n[START] Sonar Scans...\n======================\n'
                    sh '/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner-4.7.0/bin/sonar-scanner'
                    echo '\n====================\n[END] Sonar Scans...\n====================\n'
                }
            }
        }
        stage('Docker Build') {
            steps {
                echo '\n=======================\n[START] Docker Build...\n=======================\n'
                echo 'Running docker build...'
                sh "docker build -t analytics/tweet_sentiment_api:latest ."
                echo '\n=====================\n[END] Docker Push to Nexus...\n=====================\n'
            }
        }
        stage('Docker Tag and Push to Nexus') {
            steps {
                echo '\n=======================\n[START] Docker Push to Nexus...\n=======================\n'
                echo 'Tagging docker build...'
                sh "docker tag tweet_sentiment_api 192.168.50.25:5000/analytics/tweet_sentiment_api/httpd:version${env.BUILD_ID}"
                sh "docker push 192.168.50.25:5000/analytics/tweet_sentiment_api/httpd:version${env.BUILD_ID}"
                echo '\n=====================\n[END] Docker Push to Nexus...\n=====================\n'
            }
        }
        stage('Docker Publish') {
            steps {
                echo '\n===========================\n[START] Publishing Build...\n===========================\n'
                echo 'Running docker push...'
                echo '\n=========================\n[END] Publishing Build...\n=========================\n'
            }
        }
        stage('Environment Cleanup') {
            steps {
                echo '\n==============================\n[START] Cleanup and Removal...\n==============================\n'
                echo 'Running docker rm...'
                echo '\n============================\n[END] Cleanup and Removal...\n============================\n'
            }
        }
    }
}