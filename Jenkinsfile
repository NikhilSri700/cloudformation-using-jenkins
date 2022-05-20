pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                withCredentials([string(credentialsId: 'AWS_SECRET_ID', variable: 'AWS_SECRET_ID'), string(credentialsId: 'AWS_SECRET_KEY', variable: 'AWS_SECRET_KEY')]) {
                    sh 'python3 task_script.py $AWS_SECRET_ID $AWS_SECRET_KEY $STACK_NAME cfn_task.yaml $VPC_CIDR $PUBLIC_SUBNET_CIDR $PRIVATE_SUBNET_CIDR $EMAIL $INSTANCE_TYPE'
                }
            }
        }
    }
}