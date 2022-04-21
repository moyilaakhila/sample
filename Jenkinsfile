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
