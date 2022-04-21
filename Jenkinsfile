pipeline {
    agent { label 'abot-test' }
     options {
        buildDiscarder(logRotator(daysToKeepStr: '0'));
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
    stage ('Run') {
        
    }
    stage ('Build') {
        steps {
                script {
                    try {
                        sh "rm -rf ansible/agw_ansible_hosts"
                        def ansibleInventory = """{all: {hosts: 172}}"""
                        ansInvData = readYaml text: ansibleInventory
                        ansInvData.all.hosts = testAgentIp
                        writeYaml charset: '', data: ansInvData, file: 'ansible/agw_ansible_hosts'
                        dir ('ansible') {
                            sh "ansible-playbook transfer_test_result.yaml"
                        }
                        currentBuild.result = "SUCCESS"
                    } catch (err) {
                        println err
                        deleteDir()
                        notifyBuild('FAILED')
                        error err
                    } finally {
                        notifyBuild(currentBuild.result)
                        deleteDir()
                    }
                }
            }
        }
    } 
    stage ('Date') {
      /
    }
    stage ('Status') {
      
    }
    stage ('Test case ID') {
      
    }
    stage ('Test case name') {
      
    }
    stage ('Test cases status') {
      
    }
    def sendRestReq(def url, def method = 'GET', def data = null, type = null, headerKey = null, headerVal = null) {
    try{
        def response = null
        if (null == url || url.toString().trim().isEmpty()) return response
        method = method.toUpperCase()
        switch (method) {
            case 'GET':
                response = httpRequest quiet: true, httpMode: method, ignoreSslErrors: true,  url: url, wrapAsMultipart: false
                break
            case 'POST':
            case 'PUT':
            case 'DELETE':
                if (null == data) {
                    response = httpRequest quiet: true, httpMode: method, ignoreSslErrors: true, url: url, wrapAsMultipart: false
                } else if (headerKey != null && headerVal != null){
                    // if (null == type || type.toString().trim().isEmpty()) return response
                    response = httpRequest quiet: true, httpMode: method, ignoreSslErrors: true, url: url, requestBody: "${data}", wrapAsMultipart: false, customHeaders: [[maskValue: false, name: 'Content-Type', value: type], [maskValue: false, name: "${headerKey}", value: "${headerVal}"]]
                }
                else {
                    if (null == type || type.toString().trim().isEmpty()) return response
                    response = httpRequest quiet: true, httpMode: method, ignoreSslErrors: true, url: url, requestBody: "${data}", wrapAsMultipart: false, customHeaders: [[maskValue: false, name: 'Content-Type', value: type]]
                }
                break
            default:
                break
                return response
        }
        return response
    } catch(Exception ex) {
        return null
    }
}

def uploadLogsToGit (packageVersion) {
    sh(returnStdout: true, script: """if [ ! -d firebaseagentrepo ]; then mkdir firebaseagentrepo; fi""")
    dir ('firebaseagentrepo') {
        git "https://github.com/wavelabsai/firebaseagentreport.git"
        sh "cp ../testArtifact/logs/sut-logs/magma-epc/AMF1/mme.log mme-${packageVersion}.log"
        sh "cp ../testArtifact/logs/sut-logs/magma-epc/AMF1/syslog syslog-${packageVersion}"
        sh "git config user.email 'tapas.mishra@wavelabs.ai'"
        sh "git config user.name 'Tapas Mishra'"
        sh "git add . && git commit -am 'Adding report files for the version ${packageVersion}'"
        withCredentials([gitUsernamePassword(credentialsId: 'github_token', gitToolName: 'Default')]) {
            sh "git push --set-upstream origin master"
        }
    }
}

def notifyBuild(String buildStatus = 'STARTED') {
    def details = ""
    buildStatus = buildStatus ?: 'SUCCESS'

    def subject = "Job '${env.JOB_NAME}': ${buildStatus} for the AGW artifact ID - ${packageVersion}"
    if (buildStatus == 'STARTED') {
        details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p><p>Check console output at &QUOT;<a href='${env.BUILD_URL}/console'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
    } else if (buildStatus == 'SUCCESS') {
        details = """<p>COMPLETED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p><p>Check console output at &QUOT;<a href='${env.BUILD_URL}/console'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
    } else {
        details = """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p><p>Check console output at &QUOT;<a href='${env.BUILD_URL}/console'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
    }
    emailext (
        mimeType: 'text/html',
        subject: "[Jenkins] ${subject}",
        body: "${details}",
        to: "${env.mailRecipients}"
    )
  }  
}
