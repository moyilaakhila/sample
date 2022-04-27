pipeline {
    agent any
    /* parameters {
        string(name: 'ARTIFACTID', defaultValue: 'https://artifactory.magmacore.org/artifactory/debian-test/pool/focal-ci/magma_1.7.0-1637259345-3c88ec27_amd64.deb', description: 'Download URL to the Deb package')
        string(name: 'TestCaseName', defaultValue: 'magma-5g', description: 'Mention the test Case that you want to execute.')
        string(name: 'abotIp', defaultValue: '192.16.3.144', description: 'eth0 IP of your AGW instance.')
    } */
    options {
        buildDiscarder(logRotator(daysToKeepStr: '1'));
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
        stage ('Date') {
            steps {
            build job: "Release Helpers/(TEST) Schedule Release Job2",
                parameters: [
                    [$class: 'StringParameterValue', name: 'ReleaseDate', value: "${currentDate}"]
                ]
            }
        }
        stage ('Test case ID,name,status') {
            steps {
                script {
                    try {
                        def lastArtTimeStampurl = "http://${abot_ip}:5000" + '/abot/api/v5/latest_artifact_name'
                        def lastArtTimeStampparams = ""
                        lastArtTimeStamp = sendRestReq(lastArtTimeStampurl, 'GET', lastArtTimeStampparams, 'application/json')
                        lastArtTimeStamp = readJSON text: lastArtTimeStamp.content
                        echo lastArtTimeStamp.data.latest_artifact_timestamp.toString()
                        lastArtTimeStamp = lastArtTimeStamp.data.latest_artifact_timestamp.toString()

                        if (ffArtifactURL (lastArtTimeStamp)) {
                            sleep 10
                        }
                        fileUrl = ffArtifactURL (lastArtTimeStamp)
                        timeout(5) {
                            waitUntil(initialRecurrencePeriod: 15000) {
                                def statusCode = ""
                                try {
                                    statusCode = sh(script: "curl -o /dev/null -s -w '%{http_code}\\n' ${fileUrl}", returnStdout: true).trim()
                                    if ( statusCode == "200" ) {
                                        sh(script: "curl ${fileUrl} -o testArtifact.zip", returnStdout: true)
                                        return true 
                                    } else {
                                        println "Artifact is not ready, http status code is : ${statusCode}"
                                        return false
                                    }
                                } catch (exception) {
                                    println exception
                                    return false
                                }
                            }
                        }
                        //sh(returnStdout: true, script: """curl ${fileUrl} -o testArtifact.zip""")
                        sh(returnStdout: true, script: """if [ ! -d testArtifact ]; then mkdir testArtifact; fi""")
                        sh(script: "unzip testArtifact.zip -d testArtifact", retrunStdout: true)
                        //unzip dir: 'testArtifact', glob: '', zipFile: 'testArtifact.zip'
                        uploadLogsToGit(packageVersion)
                        def getResulturl = "http://${abot_ip}:5000" + "/abot/api/v5/artifacts/execFeatureSummary?foldername=${lastArtTimeStamp}"
                        def getResultparams = ""
                        getResult = sendRestReq(getResulturl, 'GET', getResultparams, 'application/json')
                        getResult = readJSON text: getResult.content
                        for ( res in getResult.feature_summary.result.data) {
                            if (res.features.status == "failed" ) {
                                resVerdict = "False"
                            }
                        }
                        sh(returnStdout: true, script: """if [ ! -d testResult ]; then mkdir testResult; fi""")
                        writeFile file: 'testResult/test_verdict', text: resVerdict
                        def tableBody = readFile("config_files/test_report.html")
                        def headHtml = readFile("config_files/test_report_first_part.html")
                        def ffMappingData = readJSON file: "config_files/tc_mapping.json"
                        createHtmlTableBody (ffMappingData, getResult, tableBody, headHtml, packageVersion)
                    } catch (err) {
                        println err
                        //currentBuild.result = "FAILED"
                        //deleteDir()
                        //notifyBuild('FAILED')
                        //error err
                    } 
                }
            }
        }
    }
    /*
    def sendRestReq(def url, def method = 'GET', def data = null, type = null, headerKey = null, headerVal = null) {
  try {
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
 } */
}

