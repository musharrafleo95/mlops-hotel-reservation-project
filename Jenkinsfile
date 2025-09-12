pipeline{
    agent any

    environment{
        VENV_DIR = '.venv'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                echo 'Cloning Github repo to Jenkins.............'
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/musharrafleo95/mlops-hotel-reservation-project.git']])
            }
        }

        stage('Setting up our Virtual Enviornment and installing dependencies'){
            steps{
                echo 'Setting up our Virtual Enviornment and installing dependencies.............'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}