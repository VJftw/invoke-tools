node {
    stage 'Unit Tests'
    env.CI = "true"
    checkout scm

    withCredentials([
        [
            $class: 'AmazonWebServicesCredentialsBinding',
            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            credentialsId: 'AWSJenkinsCredentials',
            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        ]
    ]) {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm', 'defaultFg': 1, 'defaultBg': 2]) {
            sh 'invoke test'
        }
    }

    stage 'Build'
    env.CI = "true"
    checkout scm
    wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm', 'defaultFg': 1, 'defaultBg': 2]) {
      sh 'invoke build'
    }

    stage 'Publish'
    withCredentials([
    [
        $class: 'UsernamePasswordMultiBinding',
        credentialsId: 'VJftwPyPICredentials',
        passwordVariable: 'PYPI_PASSWORD',
        usernameVariable: 'PYPI_USERNAME'
    ]
    ]) {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm', 'defaultFg': 1, 'defaultBg': 2]) {
          sh 'invoke publish'
        }
    }
}
