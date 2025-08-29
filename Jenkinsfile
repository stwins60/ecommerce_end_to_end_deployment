pipeline {
    agent any

    environment {
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_USERNAME = "idrisniyi94"
        DOCKERHUB_CREDENTIALS = credentials("5f8b634a-148a-4067-b996-07b4b3276fba")
    }

    stages {
        stage('Docker Build') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USERNAME}/ecommerce_demo:${IMAGE_TAG} .'
            }
        }

        stage('Docker Login') {
            steps {
                sh '''
                  echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                '''
                echo "Login Succeeded"
            }
        }

        stage('Docker Push') {
            steps {
                sh 'docker push ${DOCKERHUB_USERNAME}/ecommerce_demo:${IMAGE_TAG}'
            }
        }

        stage('Set Namespace') {
            steps {
                script {
                    if (env.GIT_BRANCH == "origin/dev" || env.BRANCH_NAME == "dev") {
                        env.NAMESPACE = "dev"
                        env.ENVIRONMENT="development"
                    } else if (env.GIT_BRANCH == "origin/prod" || env.BRANCH_NAME == "prod") {
                        env.NAMESPACE = "prod"
                        env.ENVIRONMENT = "production"
                    } else {
                        env.NAMESPACE = "staging"
                    }
                }
            }
        }

        stage('K8S Deploy') {
            steps {
                withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: '81721d8d-c77d-4f02-83bc-87a187c20352', namespace: '', restrictKubeConfigAccess: false, serverUrl: '') {
                    dir('k8s') {
                        sh """
                          sed -i 's|environment: .*|environment: ${ENVIRONMENT}|g' postgres.yaml
                          sed -i 's|namespace: .*|namespace: ${NAMESPACE}|g' postgres.yaml
                          sed -i 's|ENV_SUFFIX|${NAMESPACE}|g' postgres.yaml
                          sed -i 's|environment: .*|environment: ${ENVIRONMENT}|g' app_deploy.yaml
                          sed -i 's|namespace: .*|namespace: ${NAMESPACE}|g' app_deploy.yaml
                          sed -i 's|IMAGE_TAG|${IMAGE_TAG}|g' app_deploy.yaml

                          echo "Apply deployment"
                          kubectl apply -f .
                        """
                    }
                }
            }
        }
    }
}
