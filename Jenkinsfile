pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf cloudformation-using-jenkins'
                sh 'git clone https://github.com/NikhilSri700/cloudformation-using-jenkins.git'
            }
        }
        stage('Build') {
            steps {
                withCredentials([string(credentialsId: 'AWS_SECRET_ID', variable: 'AWS_SECRET_ID'), string(credentialsId: 'AWS_SECRET_KEY', variable: 'AWS_SECRET_KEY')]) {
                    sh 'python3 cloudformation-using-jenkins/task_script.py $AWS_SECRET_ID $AWS_SECRET_KEY $STACK_NAME $VPC_CIDR $PUBLIC_SUBNET_CIDR $PRIVATE_SUBNET_CIDR $EMAIL $INSTANCE_TYPE'
                }
            }
        }
    }
}