#!/usr/bin/python3

SUPPORTED_FEDORA_VERSIONS = [36, 37]
SUPPORTED_JAVA_VERSIONS = [11, 17]
MANDREL_VERSION = "22.2.0.0-Final"


def main():
    output = """
trigger:
  - master
jobs:"""
    for f in SUPPORTED_FEDORA_VERSIONS:
        for j in SUPPORTED_JAVA_VERSIONS:
            output += f"""
  - job: Building on Fedora {f}, Java {j}
    pool:
    vmImage: ubuntu-latest
    steps:
      - script: |
          echo "Building the images"
          printf "Using %d threads\\n" $(nproc)
          echo "------------------------------------------------------\\n"

          sed "s/__fedora_version__/{f}/g" -i Dockerfile
          sed "s/__mandrel_version__/{MANDREL_VERSION}/g" -i Dockerfile
          sed "s/__java_version__/{j}/g" -i Dockerfile
          cat Dockerfile

          docker build -f Dockerfile -t quarkus-native-builder:f{f}-j{j} .
          
          echo "------------------------------------------------------\\n"

          # echo "$DOCKER_PASSWORD" | docker login -u mercur3 --password-stdin
          # docker push $MEDIUM_36
          # docker push $FULL_36
          # env:
          #   DOCKER_PASSWORD: $(DOCKER_PASSWORD)
"""
    with open("azure-pipelines.yml", "w") as fd:
        output += "\n"
        print(output)
        fd.write(output)


if __name__ == "__main__":
    main()
