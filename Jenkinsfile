pipeline {
    agent { label 'abot-test' }
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
    emailtext (
        mimeType: 'text/html',
        subject: "[Jenkins] ${subject}",
        body: "${details}",
        to: "${env.mailRecipients}"
    )
}
}
