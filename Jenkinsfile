pipeline{
    agent any

    environment {
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_USERNAME = "idrisniyi94"
        DOCKERHUB_CREDENTIALS = credentials("5f8b634a-148a-4067-b996-07b4b3276fba")
    }

    stage('Docker Build'){
        steps{
            sh 'docker build -t ${DOCKERHUB_USERNAME}/ecommerce_demo:${IMAGE_TAG} .'
        }
    }

    stage('Docker Login') {
        steps {
            sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
            echo "Login Succeeded"
        }
    }

    stage ('Docker Push') {
        steps {
            sh "docker push ${DOCKERHUB_USERNAME}/ecommerce_demo:${IMAGE_TAG}"
        }
    }
    stage('Set Namespace') {
        steps {
            script {
                if (env.GIT_BRANCH == "origin/dev" || env.BRANCH_NAME == "dev") {
                    env.NAMESPACE = "dev"
                }
                else if (env.GIT_BRANCH == "origin/prod" || env.BRANCH_NAME == "prod") {
                    env.NAMESPACE = "prod"
                } else {
                    env.NAMESPACE = "staging"
                }
            }
        }
    }
    stage('Terraform Deploy') {
        steps {
            withKubeConfig([credentialsId: '81721d8d-c77d-4f02-83bc-87a187c20352']) {
                dir('terraform') {
                    sh "terraform init"
                    sh "terraform plan"
                    sh 'terraform apply -auto-approve -var="image_tag=${IMAGE_TAG}" -var="namespace=${NAMESPACE}'
                }
            }
        }
    }
}