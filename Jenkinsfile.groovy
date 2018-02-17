node() {
    checkoutStage()
    testStage()
    buildImageStage()
    deployImageStage()
}


def checkoutStage() {
    stage('Checkout') {
        checkout scm
    }
}


def testStage() {
    docker.image('python:3.6-slim').inside {
        stage('Test') {
            sh('pip3 install -r requirements.txt')
            sh('pip3 install pytest')
            withEnv(['ETH_WALLETS=addr1,addr2']) {
                sh('pytest --junitxml target/results.xml')
            }
            junit 'target/results.xml'
       }
    }
}

def buildImageStage() {
    stage('Build') {
        def img = docker.build('b7w.me/assistant')
        img.push(env.BUILD_ID)
        img.push('latest')
   }
}

def deployImageStage() {
    stage('Deploy') {
        echo('cool')
   }
}
