"""
invoke_tools.ci.aws.ecr
"""

class ECR:
    """
    AWS Elastic Container Registry
    """

    @staticmethod
    def clean(ecr_client, repository_name):
        """
        Removes untagged images from an ECR repository.
        TODO: Expand to only keep n images (don't ever remove :latest)
        """
        print("#")
        print("# Removing untagged ECR images from {0}".format(repository_name))
        print("#")
        response = ecr_client.list_images(
            repositoryName=repository_name,
            filter={
                'tagStatus': 'UNTAGGED'
            }
        )

        images_to_remove = response['imageIds']

        if len(images_to_remove) < 1:
            print("\tNo images to remove")
            return

        print("\tRemoving {0} images:".format(len(images_to_remove)))
        for image_to_remove in images_to_remove:
            print("\t\t{0}".format(image_to_remove['imageDigest']))

        response = ecr_client.batch_delete_image(
            repositoryName=repository_name,
            imageIds=images_to_remove
        )

        if response['HTTPStatusCode'] == 200:
            print("\tSuccessfully removed {0} images".format(len(images_to_remove)))
        else:
            print("\tFailed with response:")
            print(response)
