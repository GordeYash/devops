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

      sh 'cat demo/deployment.yaml'  // To confirm file content

      // Apply deployment with error output
def status = sh(script: "cd demo && kubectl apply -f deployment.yaml", returnStatus: true)
      if (status != 0) {
          error "kubectl apply failed with exit code ${status}"
      }
        sh 'pwd && ls -l'


      // Expose deployment similarly
      status = sh(script: "kubectl expose deployment ${KUBE_DEPLOYMENT} --type=NodePort --port=80", returnStatus: true)
      if (status != 0) {
          error "kubectl expose failed with exit code ${status}"
      }
    }
  }
}

    }
}
