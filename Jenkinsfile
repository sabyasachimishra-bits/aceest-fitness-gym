pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        TEST_IMAGE = 'aceest-fitness:test'
        RUNTIME_IMAGE = "aceest-fitness:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Source') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE:/workspace" \
                        -w /workspace \
                        python:3.12-slim \
                        python -m compileall app.py tests
                '''
            }
        }

        stage('Build Test Image') {
            steps {
                sh '''
                    docker build \
                        --target test \
                        --tag ${TEST_IMAGE} \
                        .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                        ${TEST_IMAGE} \
                        pytest -v \
                        --cov=app \
                        --cov-report=term-missing \
                        --junitxml=test-results.xml
                '''
            }
        }

        stage('Build Runtime Image') {
            steps {
                sh '''
                    docker build \
                        --target runtime \
                        --tag ${RUNTIME_IMAGE} \
                        .
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                    docker rm -f aceest-fitness-jenkins \
                        2>/dev/null || true

                    docker run -d \
                        --name aceest-fitness-jenkins \
                        -p 5001:5000 \
                        ${RUNTIME_IMAGE}

                    SUCCESS=false

                    for attempt in $(seq 1 15); do
                        if curl --fail \
                            http://localhost:5001/health; then
                            SUCCESS=true
                            break
                        fi

                        sleep 2
                    done

                    if [ "$SUCCESS" != "true" ]; then
                        docker logs aceest-fitness-jenkins
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f aceest-fitness-jenkins \
                    2>/dev/null || true
            '''

            junit allowEmptyResults: true,
                  testResults: 'test-results.xml'
        }

        success {
            echo 'ACEest Fitness BUILD completed successfully.'
        }

        failure {
            echo 'ACEest Fitness BUILD failed. Review the stage logs.'
        }
    }
}