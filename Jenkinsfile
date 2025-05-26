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
      kubeconfig(caCertificate: '''-----BEGIN CERTIFICATE-----
MIIDBjCCAe6gAwIBAgIBATANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwptaW5p
a3ViZUNBMB4XDTI1MDQyMjE2NTE0N1oXDTM1MDQyMTE2NTE0N1owFTETMBEGA1UE
AxMKbWluaWt1YmVDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMRa
Qu/khcxMg1E2RPrBOrbLheopZ7vm2nhj3e2zdWlJXv4m8NSrZrs0PtvqNVb1tRDA
7v6Cw8w1A/mwwvHBx+HCXi92nKXMq5y8qXeYSQXTRcdaSkDuPTOMzjy7edEhle/0
BCobLUqz4OXmiy5NoXsyxAvKbEl8E9bovxocGDzpSgouSc5HTRTxEZ9uNxvAdeFQ
nY1Bo+LBG8WPNlzpotDCyp4eB+ppQBeFND1tkNN7LIP+IQA8TUcxZBuTPqx9hnUe
XDVD4+fLrdUe30a4ipM/6Fs0tCZKOAenskC4CnFlW5tHxRGD42iH0X5eRHui+aSp
9j52L3SX+9gnM4nn9SkCAwEAAaNhMF8wDgYDVR0PAQH/BAQDAgKkMB0GA1UdJQQW
MBQGCCsGAQUFBwMCBggrBgEFBQcDATAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW
BBSj+Kpj10getIkYC59CcTg1kRZR+TANBgkqhkiG9w0BAQsFAAOCAQEAkRIquQHz
KrEExOjWyBvEMqrh2L7wVv0IOwMqO4Y+BDFCaCBC0fVSzlFTKgWtu0koekIrgsrY
Nq9X8AmTBBrkpkWRibk4WVVlfQipXLsfvnSIkpOPf5RwbW8uIWV5Btq/hu+hVMT1
YGO0Z9mwFLYbhWdxSJYZsi17Q47d+29jZ9IpjYczkvPbR0A8s2cL3dHc4d1R1SPS
fXX0qYfe8/xq/gkRkIJnA+CfSej10EMU6ssf5+nCzccr8+M7wM8jUXSCN1FuCfF3
6vIQ+C6WYrT5bre/QLtuMFe6+U5/2fWyIu3TODxugFE7vWIR6Cc5LADNWaVCfczq
D+TpGLgymlUU6w==
-----END CERTIFICATE-----
''', credentialsId: 'minikube-jenkins-secret', serverUrl: 'https://192.168.49.2:8443') {
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
