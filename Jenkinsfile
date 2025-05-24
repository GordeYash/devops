pipeline {
    agent any

    environment {
        IMAGE_NAME = "yashgorde/myapp:latest"    // full repo name in Docker Hub
        KUBE_DEPLOYMENT = "myapp-deployment"
        KUBE_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/GordeYash/devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}", "demo")
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_NAME}"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    writeFile file: 'demo/deployment.yaml', text: """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${KUBE_DEPLOYMENT}
  namespace: ${KUBE_NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: ${IMAGE_NAME}
        ports:
        - containerPort: 80
"""
                    sh "kubectl apply -f demo/deployment.yaml"
                    sh "kubectl expose deployment ${KUBE_DEPLOYMENT} --type=NodePort --port=80"
                }
            }
        }
    }
}
