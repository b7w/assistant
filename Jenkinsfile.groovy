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
    docker.image('python:3.6-slim').inside {
        stage('Test') {
            sh('pip install3 -r requirements.txt')
            withEnv(['ETH_WALLETS=addr1,addr2']) {
                sh('cd src && python -m unittest')
            }
       }
    }
}
