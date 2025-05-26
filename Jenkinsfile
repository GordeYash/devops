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
      kubeconfig(caCertificate: 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ilc4MzZxNUdHNzc1dkg0WkFSSjZrUTE4ektGU3VWSkRVZnNnU2c2RV9QVkkifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzQ4MjI0MjUxLCJpYXQiOjE3NDgyMjA2NTEsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiYTA2Yzk2ODgtYThhMi00Zjg1LTkxOTItNDEzMzUxMzhmYmVjIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImplbmtpbnMiLCJ1aWQiOiJjMzVlZGFkYS1iNDk3LTQ0MzEtYTZlOC01ZjNhNzIxYjBhN2IifX0sIm5iZiI6MTc0ODIyMDY1MSwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6amVua2lucyJ9.hInTkEV1D4wk0rZ3DjUwAKK69IsP0qKyGayqLbxAg8sOQjUrMGANSnAephUJp1LR8GYddO_TkLD6xlPY2olVBxFIZyGtS_48rBfcObX90a3klTQDdBjSsbuK9fswKDMhE5eNF44nHJ-Fg5aWC6jGNU0yP1ryCKSKoZDSB-lEABxhAPOVpqG1fqStOq2BCIKpnJNuss-sVEpXkTx2pVwEC7PfojgcY8yzAw2VOsMknMiSicYXNBb9Pmuoxwxw5biHNJIQ6w7NbK7DxmkUw4CH7tJw-ydH8DiFzOeDpZtUHyqjZF90Arf0AT1Pyr7YZqcL30ycnzl6Zazz9Ysr7GtO-Q', credentialsId: 'minikube-jenkins-secret', serverUrl: ' https://192.168.49.2:8443') {
    // some block
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
}
