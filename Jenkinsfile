pipeline {
    agent any

    environment {
        image-name = "${env.NEXUS}:5000/language-translation-api:latest",
        container-name = "language-translation-api",
        host-port = "4567",
        container-port = "4567"
    }

    stages {
        stage('Environment Setup') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-login', passwordVariable: 'NEXUS_PASSWORD', usernameVariable: 'NEXUS_USERNAME')]) {
                    withPythonEnv('python3.9') {
                        echo '\n=======================\n[START] Initializing...\n=======================\n'
                        echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL} \n"
                        echo "\n<--------- Installing PyTorch... --------->"
                        sh 'pip3.9 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu'
                        echo "\n<--------- Installing requirements.txt --------->"
                        sh 'pip3.9 install -r requirements.txt --no-cache-dir --index-url http://\$NEXUS_USERNAME:\$NEXUS_PASSWORD@192.168.50.25:8081/repository/Workstation_PyPi/simple --trusted-host ${env.NEXUS}'
                        echo '\n=====================\n[END] Initializing...\n=====================\n'
                    }
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
                script {
                    buildImage = docker.build("tweet_sentiment_api:${env.BUILD_ID}")
                }
                echo '\n=====================\n[END] Docker Build...\n=====================\n'
            }
        }
        stage('Docker Tag and Push to Nexus') {
            steps {
                echo '\n=======================\n[START] Docker Push to Nexus...\n=======================\n'
                echo 'Tagging docker build...'
                script {
                    docker.withRegistry("https://${env.NEXUS}:5000/analytics/", "nexus-login") {
                        buildImage.push("${env.BUILD_NUMBER}")
                        buildImage.push("latest")
                    }
                }
                echo '\n=====================\n[END] Docker Push to Nexus...\n=====================\n'
            }
        }
        stage('Docker Publish') {
            steps {
                echo '\n===========================\n[START] Publishing Build...\n===========================\n'
                echo 'Running docker push...'
                sshagent(credentials: ['docker-login']) {
                    withCredentials([usernamePassword(credentialsId: 'docker-login', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no user@${env.DOCKER} "
                                whoami
                                docker stop ${container-name}
                                docker rm ${container-name}
                                docker pull ${image-name}
                                docker run -d --name ${container-name} --restart=unless-stopped -p ${host-port}:${container-port} --privileged ${image-name}
                                docker system prune -af
                            "
                        """
                    }
                }
                echo '\n=========================\n[END] Publishing Build...\n=========================\n'
            }
        }
        stage('Docker Cleanup') {
            steps {
                echo '\n==============================\n[START] Cleanup and Removal...\n==============================\n'
                echo 'Running docker rm...'
                sh "docker system prune -af"
                echo '\n============================\n[END] Cleanup and Removal...\n============================\n'
            }
        }
    }
}