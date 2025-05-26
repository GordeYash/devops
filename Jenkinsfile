pipeline {
    agent any

    environment {
        IMAGE_NAME = "yashgorde/myapp:01"    // full repo name in Docker Hub
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
      sh 'cat demo/deployment.yaml'
      sh 'pwd && ls -l && ls -l demo'

      // Apply deployment
      def status = sh(script: "cd demo && kubectl apply -f deployment.yaml", returnStatus: true)
      if (status != 0) {
          error "kubectl apply failed with exit code ${status}"
      }

      // Expose deployment
      status = sh(script: "kubectl expose deployment ${KUBE_DEPLOYMENT} --type=LoadBalancer --port=8000", returnStatus: true)
      if (status != 0) {
          error "kubectl expose failed with exit code ${status}"
      }
    }
  }
}

    }
}
