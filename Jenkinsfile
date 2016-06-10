node {
    stage 'Unit Tests'
    env.CI = "true"
    checkout scm
    wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm', 'defaultFg': 1, 'defaultBg': 2]) {
      sh '''
        set +x
        invoke test
      '''
    }
    publishHTML(target: [allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'coverage', reportFiles: 'index.html', reportName: 'Test Coverage Report'])

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
          sh '''
            set +x
            invoke publish
          '''
        }
    }
}
