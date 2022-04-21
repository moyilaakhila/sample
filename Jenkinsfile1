pipeline {
    agent { label 'abot-test' }
     options {
        buildDiscarder(logRotator(daysToKeepStr: '0'));
        disableConcurrentBuilds();
        timestamps()
    }
    stages {
        stage('Send email') {
            def mailRecipients = "akhila.moyila@wavelabs.ai"
            def jobName = currentBuild.fullDisplayName

            emailext body: '''${SCRIPT, template="groovy-html.template"}''',
                mimeType: 'text/html',
                subject: "[Jenkins] ${jobName}",
                to: "${mailRecipients}",
                replyTo: "${mailRecipients}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']]
        }
    }
}
