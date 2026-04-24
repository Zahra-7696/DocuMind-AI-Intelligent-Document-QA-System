pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Zahra-7696/DocuMind-AI-Intelligent-Document-QA-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t documind-ai .'
            }
        }

        stage('Run Container') {
            steps {
                bat '''
                docker stop documind-ai-container || exit 0
                docker rm documind-ai-container || exit 0

                docker run -d --name documind-ai-container ^
                -p 7860:7860 ^
                -e GRADIO_HOST=0.0.0.0 ^
                -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ^
                documind-ai
                '''
            }
        }
    }
}