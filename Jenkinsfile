pipeline {
    agent any

    stages {
        stage('Initializing') {
            steps {
                echo '=================\n[START] Initializing...=================\n'
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL} \n"
                echo "Installing PyTorch..."
                sh 'pip3.9 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu'
                echo "Installing requirements.txt"
                sh 'pip3.9 install -r requirements.txt'
                echo '=================\n[END] Initializing...=================\n'
            }
        }
        stage('Test') {
            steps {
                echo '=================\n[START] PyTest Unit Tests...=================\n'
                echo 'Running pytest...'
                sh 'python3.9 -m pytest --cov . --cov-report xml'
                echo '=================\n[END] PyTest Unit Tests...=================\n'
            }
        }
        stage('Build') {
            steps {
                echo '=================\n[START] Docker Build...=================\n'
                echo 'Running docker build...'
                echo '=================\n[END] Docker Build...=================\n'
            }
        }
        stage('Publish') {
            steps {
                echo '=================\n[START] Publishing Build...=================\n'
                echo 'Running docker push...'
                echo '=================\n[END] Publishing Build...=================\n'
            }
        }
        stage('Cleanup') {
            steps {
                echo '=================\n[START] Cleanup and Removal...=================\n'
                echo 'Running docker rm...'
                echo '=================\n[END] Cleanup and Removal...=================\n'
            }
        }
    }
}