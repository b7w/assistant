pipeline {
    agent none

    stages {
        stage('Test') {
            agent {
                docker { image 'python:3.6-slim' }
            }
            test()
        }
    }
}

def test() {
    dir('src') {
        withEnv(['ETH_WALLETS=addr1,addr2']) {
            sh('python -m unittest')
        }
    }
}
