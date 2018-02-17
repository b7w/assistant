node() {
    checkoutStage()
    testStage()
}


def checkoutStage() {
    stage('Checkout') {
        checkout scm
    }
}


def testStage() {
    stage('Test') {
        agent {
            docker { image 'python:3.6-slim' }
        }
        withEnv(['ETH_WALLETS=addr1,addr2']) {
            sh('cd src && python -m unittest')
        }
    }
}