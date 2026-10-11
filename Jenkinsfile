pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
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
                    echo "=================================================="
                    echo "ACEest Fitness Build Validation"
                    echo "=================================================="

                    pwd

                    echo ""
                    echo "Repository Contents:"
                    ls -la

                    echo ""
                    echo "Verifying required files..."

                    test -f app.py
                    echo "✓ app.py found"

                    test -f Dockerfile
                    echo "✓ Dockerfile found"

                    test -f requirements.txt
                    echo "✓ requirements.txt found"

                    test -f README.md
                    echo "✓ README.md found"

                    echo ""
                    echo "Source validation completed successfully."
                '''
            }
        }

        stage('Verify Project Structure') {
            steps {
                sh '''
                    echo ""
                    echo "Verifying project structure..."

                    test -d tests
                    echo "✓ tests directory found"

                    test -d .github
                    echo "✓ .github directory found"

                    test -d .github/workflows
                    echo "✓ workflows directory found"

                    test -f .github/workflows/main.yml
                    echo "✓ GitHub Actions workflow found"

                    echo ""
                    echo "Project structure verification completed."
                '''
            }
        }

        stage('Build Validation') {
            steps {
                sh '''
                    echo ""
                    echo "=============================================="
                    echo "ACEest Fitness BUILD Validation Successful"
                    echo "=============================================="

                    echo ""
                    echo "Jenkins successfully:"
                    echo "1. Connected to GitHub"
                    echo "2. Checked out source code"
                    echo "3. Validated required files"
                    echo "4. Validated project structure"
                    echo ""
                    echo "Build completed successfully."
                '''
            }
        }
    }

    post {

        success {
            echo 'ACEest Fitness BUILD completed successfully.'
        }

        failure {
            echo 'ACEest Fitness BUILD failed.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}