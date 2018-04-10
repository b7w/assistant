node() {
    checkoutStage()
    testStage()
    buildAndDeployImageStage()
}


def checkoutStage() {
    stage('Checkout') {
        checkout scm
    }
}


def testStage() {
    stage('Test') {
        docker.image('python:3.6-slim').inside {
            withEnv(['XDG_CACHE_HOME=target']) {
                sh('pip3 install -r requirements.txt')
                sh('pip3 install pytest')
            }
            try {
                withEnv(['ETH_WALLETS=addr1,addr2']) {
                    sh('pytest --junitxml target/results.xml')
                }
            } finally {
                junit 'target/results.xml'
            }
       }
    }
}


def buildAndDeployImageStage() {
    stage('Build & Deploy') {
        docker.image('python:3.6-slim').inside {
            withEnv(['XDG_CACHE_HOME=target', 'ANSIBLE_HOST_KEY_CHECKING=False']) {
                sh('pip3 install ansible')

                def key = sshUserPrivateKey(credentialsId: 'dev.loc', keyFileVariable: 'KEY')
                def vault = file(credentialsId: 'ansible_vault', variable: 'VAULT')
                withCredentials([key, vault]) {
                    sh("ansible-playbook --private-key=$KEY --vault-password-file=$VAULT --inventory=ansible/hosts.ini ansible/playbook.yml -e build_id=${env.BUILD_ID}")
                }
            }
        }
   }
}
