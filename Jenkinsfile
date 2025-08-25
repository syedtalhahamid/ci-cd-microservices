pipeline {
    agent any

    environment {
        AUTH_IMAGE = "student/auth-service"
        PROFILE_IMAGE = "student/profile-service"
        CART_IMAGE = "student/cart-service"
        ORDERS_IMAGE = "student/orders-service"
        PAYMENT_IMAGE = "student/payment-service"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/username/microservices-demo.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh "docker build -t $AUTH_IMAGE ./auth"
                sh "docker build -t $PROFILE_IMAGE ./profile"
                sh "docker build -t $CART_IMAGE ./cart"
                sh "docker build -t $ORDERS_IMAGE ./orders"
                sh "docker build -t $PAYMENT_IMAGE ./payment"
            }
        }

        stage('Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker push $AUTH_IMAGE"
                    sh "docker push $PROFILE_IMAGE"
                    sh "docker push $CART_IMAGE"
                    sh "docker push $ORDERS_IMAGE"
                    sh "docker push $PAYMENT_IMAGE"
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no ec2-user@<EC2_PUBLIC_IP> '
                    cd /home/ec2-user/microservices-demo &&
                    docker-compose down &&
                    docker-compose pull &&
                    docker-compose up -d
                '
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
