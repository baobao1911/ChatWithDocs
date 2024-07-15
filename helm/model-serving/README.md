# Deploy model on k8s
### Create Pullsecret
Docker config Secrets
example:

kubectl create secret docker-registry secret-tiger-docker \
  --docker-email=tiger@acme.example \
  --docker-username=tiger \
  --docker-password=pass1234 \
  --docker-server=http://index.docker.io/v1

### Deploy success backend api 
![image](https://github.com/user-attachments/assets/82f94b83-72a3-4cce-b12b-91cdff3da18a)
