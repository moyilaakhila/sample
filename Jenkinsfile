pipeline {
    agent { label 'abot-test' }
    parameters {
        string(name: 'ARTIFACTID', defaultValue: 'https://artifactory.magmacore.org/artifactory/debian-test/pool/focal-ci/magma_1.7.0-1637259345-3c88ec27_amd64.deb', description: 'Download URL to the Deb package')
        string(name: 'TestCaseName', defaultValue: 'magma-5g', description: 'Mention the test Case that you want to execute.')
        string(name: 'agwIp', defaultValue: '192.16.3.144', description: 'eth0 IP of your AGW instance.')
    }
    options {
        buildDiscarder(logRotator(daysToKeepStr: '2'));
        disableConcurrentBuilds();
        timestamps()
    }
    environment {
        abot_ip = "172.16.5.60"
        testAgentIp = "172.16.5.70"
        resVerdict = "True"
        mailRecipients = "akhila.moyila@wavelabs.ai"
    }
    stages {
        stage ('Deploy and upgrade AGW') {
            steps {
                script {
                    try {
                        def ansibleInventory = """{all: {hosts: 172}}"""
                        ansInvData = readYaml text: ansibleInventory
                        ansInvData.all.hosts = params.agwIp
                        sh(returnStdout: true, script: """if [ -f ansible/agw_ansible_hosts ]; then rm -rf ansible/agw_ansible_hosts; fi""")
                        writeYaml charset: '', data: ansInvData, file: 'ansible/agw_ansible_hosts'
                        def packageVersion = parseUrl(params.ARTIFACTID)
                        sh "chmod 0600 terraform/ssh-keys/id_ed25519"
                        notifyBuild('STARTED')
                        dir('ansible') {
                            sh "ansible-playbook agw_deploy.yaml --extra-vars \'magma5gVersion=${packageVersion}\' --skip-tags [baseInstall,setupInterface,addUser]"
                        }
                    } catch (err) {
                        println err
                        currentBuild.result = "FAILED"
                        deleteDir()
                        notifyBuild('FAILED')
                        error err
                    } 
                }
            }
        }
    }
