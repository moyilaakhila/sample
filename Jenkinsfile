pipeline {
    agent { label 'abot-test' }
    parameters {
        string(name: 'ARTIFACTID', defaultValue: 'https://artifactory.magmacore.org/artifactory/debian-test/pool/focal-ci/magma_1.7.0-1637259345-3c88ec27_amd64.deb', description: 'Download URL to the Deb package')
        string(name: 'TestCaseName', defaultValue: 'magma-5g', description: 'Mention the test Case that you want to execute.')
        string(name: 'agwIp', defaultValue: '192.16.3.144', description: 'eth0 IP of your AGW instance.')
    }
    emailext (
        mimeType: 'text/html',
        subject: "[Jenkins] ${subject}",
        body: "${details}",
        to: "${env.mailRecipients}"
    )
}
