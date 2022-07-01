pipeline {
     environment {
       ID_DOCKER = "docker-hub.cgerbaud.fr"
       HUB_USER = "cedric"
       HUB_URL = "docker-hub.cgerbaud.fr"
       IMAGE_NAME = "alpinehelloworld"
       IMAGE_TAG = "latest"
       STAGING = "${ID_DOCKER}-staging"
       PRODUCTION = "${ID_DOCKER}-production"
       DOCKERHUB_PASSWORD = credentials('docker-registry')
     }
     agent none
     stages {
         stage('Build image') {
             agent any
             steps {
                script {
                  sh 'docker build -t ${HUB_URL}/$IMAGE_NAME:$IMAGE_TAG .'
                }
             }
        }
        stage('Run container based on builded image') {
            agent any
            steps {
               script {
                 sh '''
                    docker rm -f $IMAGE_NAME
                    docker run --name $IMAGE_NAME -d -p 8082:5000 -e PORT=5000 ${HUB_URL}/$IMAGE_NAME:$IMAGE_TAG
                    sleep 5
                 '''
               }
            }
       }
       stage('Test image') {
           agent any
           steps {
              script {
                sh '''
                    curl http://172.17.0.1:8082 | grep -q "Hello world!"
                '''
              }
           }
      }
      stage('Clean Container') {
          agent any
          steps {
             script {
               sh '''
                 docker stop $IMAGE_NAME
                 docker rm $IMAGE_NAME
               '''
             }
          }
     }

     stage ('Login and Push Image on docker hub') {
          agent any
          steps {
             script {
               sh '''
                   echo $DOCKERHUB_PASSWORD_PWD | docker login $HUB_URL -u $HUB_USER --password-stdin
                   docker push ${HUB_URL}/$IMAGE_NAME:$IMAGE_TAG
               '''
             }
          }
      }    
     
     stage('Push image in staging and deploy it') {
       when {
              expression { GIT_BRANCH == 'origin/master' }
            }
      agent any
      environment {
          HEROKU_API_KEY = credentials('heroku_api_key')
      }  
      steps {
          script {
            sh '''
              heroku container:login
              heroku create $STAGING || echo "project already exist"
              heroku container:push -a $STAGING web
              heroku container:release -a $STAGING web
            '''
          }
        }
     }



     stage('Push image in production and deploy it') {
       when {
              expression { GIT_BRANCH == 'origin/master' }
            }
      agent any
      environment {
          HEROKU_API_KEY = credentials('heroku_api_key')
      }  
      steps {
          script {
            sh '''
              heroku container:login
              heroku create $PRODUCTION || echo "project already exist"
              heroku container:push -a $PRODUCTION web
              heroku container:release -a $PRODUCTION web
            '''
          }
        }
     }
  }
}
