pipeline {
    agent none

    stages {
        testStage()
    }
}

def testStage() {
    stage('Test') {
        agent {
            docker { image 'python:3.6-slim' }
        }
        steps {
            withEnv(['ETH_WALLETS=addr1,addr2']) {
                sh('cd src && python -m unittest')
            }
        }
    }
}
