pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS' // Configure in Jenkins Global Tool Configuration
        jdk 'JDK'       // Configure in Jenkins Global Tool Configuration
    }
    
    environment {
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_BACKEND = 'yourdockerhub/ml-backend'
        DOCKER_IMAGE_FRONTEND = 'yourdockerhub/ml-frontend'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Backend Tests') {
            steps {
                dir('backend') {
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                    sh 'python manage.py test'
                }
            }
        }
        
        stage('Frontend Tests') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm test -- --passWithNoTests'
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh 'sonar-scanner'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG} ./backend'
                sh 'docker build -t ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG} ./frontend'
                sh 'docker tag ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG} ${DOCKER_IMAGE_BACKEND}:latest'
                sh 'docker tag ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG} ${DOCKER_IMAGE_FRONTEND}:latest'
            }
        }
        
        stage('Push Docker Images') {
            steps {
                sh 'echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin'
                sh 'docker push ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG}'
                sh 'docker push ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG}'
                sh 'docker push ${DOCKER_IMAGE_BACKEND}:latest'
                sh 'docker push ${DOCKER_IMAGE_FRONTEND}:latest'
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                sh '''
                sed -i "s|image: ${DOCKER_IMAGE_BACKEND}:.*|image: ${DOCKER_IMAGE_BACKEND}:${DOCKER_TAG}|g" kubernetes/backend-deployment.yaml
                sed -i "s|image: ${DOCKER_IMAGE_FRONTEND}:.*|image: ${DOCKER_IMAGE_FRONTEND}:${DOCKER_TAG}|g" kubernetes/frontend-deployment.yaml
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl --kubeconfig=${KUBECONFIG} apply -f kubernetes/'
            }
        }
        
        stage('Verify Deployment') {
            steps {
                sh 'kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/backend -n ml-app'
                sh 'kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/frontend -n ml-app'
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
            slackSend(channel: '#deployments', color: 'good', message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
        failure {
            echo 'Pipeline execution failed!'
            slackSend(channel: '#deployments', color: 'danger', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}