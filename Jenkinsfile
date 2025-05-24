pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp:latest"
        KUBE_DEPLOYMENT = "myapp-deployment"
        KUBE_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/GordeYash/devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    writeFile file: 'deployment.yaml', text: """
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

                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl expose deployment ${KUBE_DEPLOYMENT} --type=NodePort --port=80"
                }
            }
        }
    }
}
