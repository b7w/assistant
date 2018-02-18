node() {
    checkoutStage()
    testStage()
    buildImageStage()
    deployImageStage(   )
}


def checkoutStage() {
    stage('Checkout') {
        checkout scm
    }
}


def testStage() {
    docker.image('python:3.6-slim').inside {
        stage('Test') {
            withEnv(['XDG_CACHE_HOME=target/pip']) {
                sh('pip3 install -r requirements.txt')
                sh('pip3 install pytest')
            }
            withEnv(['ETH_WALLETS=addr1,addr2']) {
                sh('pytest --junitxml target/results.xml')
            }
            junit 'target/results.xml'
       }
    }
}

def buildImageStage() {
    stage('Build') {
        docker.withRegistry('https://registry.b7w.me') {
            def img = docker.build('b7w/assistant')
            img.push(env.BUILD_ID)
            img.push('latest')
        }
   }
}

def deployImageStage() {
    stage('Deploy') {
        docker.image('python:3.6-slim').inside {
            withEnv(['XDG_CACHE_HOME=target/pip']) {
                sh('pip3 install ansible')
            }
            withCredentials([file(credentialsId: 'dev.loc', variable: 'KEY')]) {
                withCredentials([file(credentialsId: 'ansible_vault', variable: 'VAULT')]) {
                    sh("ansible-playbook --private-key=$KEY --vault-password-file=$VAULT --inventory=ansible/hosts.ini ansible/playbook.yml")
                }
            }
        }
   }
}
